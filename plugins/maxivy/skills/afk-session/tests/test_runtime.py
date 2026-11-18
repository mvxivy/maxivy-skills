import json
import os
import signal
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/runtime.py'


class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='afk-', dir='/tmp')
        self.state = Path(self.temp.name) / 'run'

    def call(self, action, *command):
        return subprocess.run([sys.executable, str(SCRIPT), action, '--state', str(self.state), *command],
                              capture_output=True, text=True, timeout=15)

    def tearDown(self):
        if (self.state / 'control.sock').exists():
            self.call('stop')
        self.temp.cleanup()

    def test_survives_launcher_and_stops_child_listener(self):
        code = ('import socket,time; s=socket.socket(); s.bind(("127.0.0.1",0)); '
                's.listen(); print(s.getsockname()[1],flush=True); time.sleep(300)')
        self.assertEqual(self.call('start', '--', sys.executable, '-u', '-c', code).returncode, 0)
        self.assertEqual(self.call('status').returncode, 0)
        duplicate = self.call('start', '--', sys.executable, '-c', code)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertEqual(self.call('stop').returncode, 0)
        import socket
        port = int((self.state / 'output.log').read_text().splitlines()[0])
        with socket.socket() as client:
            self.assertNotEqual(client.connect_ex(('127.0.0.1', port)), 0)

    def test_kills_child_that_ignores_term(self):
        code = 'import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); print("ready",flush=True); time.sleep(300)'
        self.assertEqual(self.call('start', '--', sys.executable, '-u', '-c', code).returncode, 0)
        for _ in range(50):
            if 'ready' in (self.state / 'output.log').read_text():
                break
            time.sleep(.02)
        self.assertEqual(self.call('stop').returncode, 0)

    def test_missing_executable_reports_failure(self):
        result = self.call('start', '--', '/nonexistent/afk-command')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.state / 'control.sock').exists())

    def test_stale_pid_is_never_signalled(self):
        self.state.mkdir()
        (self.state / 'process.json').write_text(json.dumps({'supervisor': 1, 'process_group': 1}))
        self.assertNotEqual(self.call('stop').returncode, 0)

    def test_dead_supervisor_state_cannot_be_overwritten(self):
        result = self.call('start', '--', sys.executable, '-c', 'import time; time.sleep(300)')
        self.assertEqual(result.returncode, 0, result.stderr)
        record_path = self.state / 'process.json'
        record = record_path.read_text()
        ids = json.loads(record)
        try:
            os.kill(ids['supervisor'], signal.SIGKILL)
            time.sleep(.1)
            restarted = self.call('start', '--', sys.executable, '-c', 'import time; time.sleep(300)')
            self.assertNotEqual(restarted.returncode, 0)
            self.assertEqual(record_path.read_text(), record)
        finally:
            os.killpg(ids['process_group'], signal.SIGKILL)
            (self.state / 'control.sock').unlink(missing_ok=True)

    def test_stops_watcher_descendant(self):
        child = ('import signal,socket,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); '
                 's=socket.socket(); s.bind(("127.0.0.1",0)); s.listen(); '
                 'print(s.getsockname()[1],flush=True); time.sleep(300)')
        parent = f'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",{child!r}]); time.sleep(300)'
        result = self.call('start', '--', sys.executable, '-c', parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        for _ in range(100):
            output = (self.state / 'output.log').read_text().strip()
            if output:
                break
            time.sleep(.02)
        port = int(output)
        self.assertEqual(self.call('stop').returncode, 0)
        import socket
        with socket.socket() as client:
            self.assertNotEqual(client.connect_ex(('127.0.0.1', port)), 0)


if __name__ == '__main__':
    unittest.main()
