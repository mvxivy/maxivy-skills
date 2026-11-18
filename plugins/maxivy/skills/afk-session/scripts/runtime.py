#!/usr/bin/env python3
"""POSIX local runtime supervisor. No permission grants; use the same host context for start/stop."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time


def request(state, message):
    with socket.socket(socket.AF_UNIX) as client:
        client.settimeout(2)
        client.connect(str(state / 'control.sock'))
        client.sendall(message.encode())
        return client.recv(4096).decode()


def serve(state, command, cwd):
    with (state / 'lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Runtime already active')
        record_path = state / 'process.json'
        if record_path.exists():
            raise SystemExit('Unreconciled runtime state; inspect before recovery')
        endpoint = state / 'control.sock'
        endpoint.unlink(missing_ok=True)
        stopping = False

        def stop(*_):
            nonlocal stopping
            stopping = True

        signal.signal(signal.SIGTERM, stop)
        signal.signal(signal.SIGINT, stop)
        child = None
        with socket.socket(socket.AF_UNIX) as server:
            server.bind(str(endpoint))
            os.chmod(endpoint, 0o600)
            server.listen()
            server.settimeout(0.2)
            try:
                record = {'supervisor': os.getpid(), 'cwd': cwd}
                record_path.write_text(json.dumps(record) + '\n')
                child = subprocess.Popen(command, cwd=cwd, start_new_session=True)
                record = {'supervisor': os.getpid(), 'process_group': child.pid, 'cwd': cwd}
                record_path.write_text(json.dumps(record) + '\n')
                while not stopping and child.poll() is None:
                    try:
                        conn, _ = server.accept()
                    except socket.timeout:
                        continue
                    with conn:
                        conn.settimeout(1)
                        try:
                            action = conn.recv(32).decode()
                            if action == 'stop':
                                stopping = True
                            conn.sendall(json.dumps(record).encode())
                        except (OSError, UnicodeError):
                            pass
            finally:
                if child is not None:
                    # Kill the whole owned group, including watcher children after their parent exits.
                    try:
                        os.killpg(child.pid, signal.SIGTERM)
                        deadline = time.monotonic() + 3
                        while time.monotonic() < deadline:
                            child.poll()
                            try:
                                os.killpg(child.pid, 0)
                            except ProcessLookupError:
                                break
                            time.sleep(0.05)
                        else:
                            os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    child.wait()
                record_path.unlink(missing_ok=True)
                endpoint.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'status', 'stop', '_serve'])
    parser.add_argument('--state', required=True, type=Path)
    parser.add_argument('--cwd', default=os.getcwd())
    argv = sys.argv[1:]
    split = argv.index('--') if '--' in argv else len(argv)
    args = parser.parse_args(argv[:split])
    state = args.state.resolve()
    command = argv[split + 1:]
    if args.action == '_serve':
        serve(state, command, args.cwd)
        return
    if args.action == 'start':
        if not command:
            parser.error('start requires -- command [args]')
        state.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            request(state, 'status')
        except (FileNotFoundError, ConnectionRefusedError):
            if (state / 'process.json').exists():
                raise SystemExit('Unreconciled runtime state; inspect before recovery')
        else:
            raise SystemExit('Runtime already active')
        with (state / 'output.log').open('ab') as log:
            supervisor = subprocess.Popen(
                [sys.executable, __file__, '_serve', '--state', str(state), '--cwd', args.cwd, '--', *command],
                stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True,
            )
        for _ in range(100):
            if supervisor.poll() is not None:
                raise SystemExit(f'Runtime failed; see {state / "output.log"}')
            try:
                print(request(state, 'status'))
                return
            except (FileNotFoundError, ConnectionRefusedError):
                time.sleep(0.05)
        raise SystemExit(f'Start not confirmed; recover with stop --state {state}')
    try:
        print(request(state, args.action))
    except (FileNotFoundError, ConnectionRefusedError):
        # Never signal a PID from an old state file: it may belong to another process.
        raise SystemExit('No reachable supervisor; inspect output.log/process.json before recovery')
    if args.action == 'stop':
        for _ in range(120):
            if not (state / 'control.sock').exists():
                print('Stopped')
                return
            time.sleep(0.05)
        raise SystemExit('Cleanup not confirmed; inspect runtime state')


if __name__ == '__main__':
    main()
