#!/usr/bin/env python3
"""Check recorded AFK evidence against current repositories; never execute manifest commands."""
import json
from pathlib import Path
import subprocess
import sys

CAPABILITIES = ('tracker', 'publish', 'git_write', 'runtime_start_stop', 'browser')


def git(path, *args):
    return subprocess.check_output(['git', '-C', path, *args], text=True, stderr=subprocess.PIPE).strip()


def check(data):
    errors = []
    projects = data.get('projects', [])
    if not projects:
        errors.append('No projects selected')
    for project in projects:
        path = project['path']
        try:
            head = git(path, 'rev-parse', 'HEAD')
            branch = git(path, 'branch', '--show-current')
            remote = git(path, 'remote', 'get-url', 'origin')
            if git(path, 'status', '--porcelain', '--untracked-files=all'):
                errors.append(f'{path}: tracked changes or untracked files after pinned baseline')
        except subprocess.CalledProcessError:
            errors.append(f'{path}: cannot inspect repository')
            continue
        for name, value in [('head', head), ('branch', branch), ('remote', remote)]:
            if project.get(name) != value:
                errors.append(f'{path}: {name} changed since preparation')
        if project.get('branch_ready') is not True:
            errors.append(f'{path}: branch preparation/push still pending')
        checks = project.get('checks', [])
        if not checks:
            errors.append(f'{path}: no baseline checks recorded')
        for receipt in checks:
            if receipt.get('head') != head or not receipt.get('command') or not receipt.get('log'):
                errors.append(f'{path}: missing or stale check evidence')
            elif not Path(receipt['log']).is_file():
                errors.append(f'{path}: check log does not exist')
            if receipt.get('exit_code') != 0 and not receipt.get('advisory_source'):
                errors.append(f'{path}: blocking check failed: {receipt.get("command")}')
        if not project.get('runtime'):
            errors.append(f'{path}: runtime versions/setup missing')
    capabilities = data.get('capabilities', {})
    for name in CAPABILITIES:
        receipt = capabilities.get(name, {})
        if receipt.get('status') == 'not_required' and receipt.get('reason'):
            continue
        if receipt.get('status') != 'passed' or not receipt.get('evidence'):
            errors.append(f'{name}: capability not verified')
        elif not Path(receipt['evidence']).is_file():
            errors.append(f'{name}: capability receipt does not exist')
        if receipt.get('worker') is not True:
            errors.append(f'{name}: worker context not verified')
    tickets = data.get('tickets', [])
    if not any(t.get('status') == 'ready' for t in tickets):
        errors.append('No runnable tickets')
    for ticket in tickets:
        if ticket.get('status') == 'ready' and ticket.get('project') not in [p['path'] for p in projects]:
            errors.append(f'{ticket.get("key")}: runnable project missing')
        if ticket.get('status') not in ('ready', 'blocked', 'skipped'):
            errors.append(f'{ticket.get("key")}: missing readiness decision')
        if ticket.get('status') != 'ready' and not ticket.get('reason'):
            errors.append(f'{ticket.get("key")}: missing blocker/skip reason')
    if data.get('pending_approvals'):
        errors.append('Approvals still pending')
    if not data.get('scope_evidence'):
        errors.append('Scope authorization not recorded')
    return errors


if __name__ == '__main__':
    try:
        errors = check(json.loads(Path(sys.argv[1]).read_text()))
    except (IndexError, KeyError, TypeError, ValueError, OSError) as exc:
        raise SystemExit(f'Invalid preflight manifest: {exc}')
    print(json.dumps({'ready': not errors, 'blockers': errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))
