import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/preflight.py'
spec = importlib.util.spec_from_file_location('preflight', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class GateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        path = self.temp.name
        def git(*args):
            return subprocess.check_output(['git', '-C', path, *args], text=True, stderr=subprocess.DEVNULL).strip()
        git('init', '-b', 'feature/test')
        git('-c', 'user.name=Test', '-c', 'user.email=test@localhost', 'commit', '--allow-empty', '-m', 'base')
        git('remote', 'add', 'origin', 'https://example.invalid/repo.git')
        head = git('rev-parse', 'HEAD')
        receipt = str(Path(path) / '.git/receipt.log')
        Path(receipt).write_text('observed test result')
        self.data = {'scope_evidence': 'user selected this temporary repo', 'pending_approvals': [],
                     'projects': [{'path': path, 'head': head, 'branch': 'feature/test',
                                   'remote': 'https://example.invalid/repo.git', 'branch_ready': True,
                                   'runtime': 'python test fixture', 'checks': [
                                       {'head': head, 'command': 'test', 'exit_code': 0, 'log': receipt}]}],
                     'capabilities': {key: {'status': 'passed', 'evidence': receipt, 'worker': True}
                                      for key in module.CAPABILITIES},
                     'tickets': [{'key': 'TEST-1', 'project': path, 'status': 'ready'}]}

    def tearDown(self):
        self.temp.cleanup()

    def test_ready(self):
        self.assertEqual(module.check(self.data), [])

    def test_collects_all_blockers(self):
        self.data['pending_approvals'] = ['dev push']
        self.data['projects'][0]['branch_ready'] = False
        self.data['projects'][0]['checks'][0]['exit_code'] = 1
        self.data['capabilities']['runtime_start_stop']['worker'] = False
        self.assertEqual(len(module.check(self.data)), 4)

    def test_stale_checks_rejected(self):
        self.data['projects'][0]['checks'][0]['head'] = 'old-head'
        self.assertIn('stale check evidence', '\n'.join(module.check(self.data)))

    def test_changed_head_rejected(self):
        self.data['projects'][0]['head'] = 'old-head'
        self.assertIn('head changed', '\n'.join(module.check(self.data)))

    def test_uncommitted_tracked_changes_rejected(self):
        path = self.data['projects'][0]['path']
        (Path(path) / 'changed.txt').write_text('new content')
        subprocess.check_call(['git', '-C', path, 'add', 'changed.txt'])
        self.assertIn('tracked changes', '\n'.join(module.check(self.data)))

    def test_advisory_needs_recorded_source(self):
        receipt = self.data['projects'][0]['checks'][0]
        receipt['exit_code'] = 1
        self.assertTrue(module.check(self.data))
        receipt['advisory_source'] = 'repo documented non-blocking command'
        self.assertEqual(module.check(self.data), [])

    def test_missing_receipt_and_excluded_project_rejected(self):
        self.data['capabilities']['publish']['evidence'] = '/nonexistent/receipt'
        self.data['tickets'][0]['project'] = '/excluded/project'
        errors = '\n'.join(module.check(self.data))
        self.assertIn('receipt does not exist', errors)
        self.assertIn('runnable project missing', errors)

    def test_untracked_source_rejected(self):
        (Path(self.temp.name) / 'new.py').write_text('changed behavior')
        self.assertIn('untracked files', '\n'.join(module.check(self.data)))


if __name__ == '__main__':
    unittest.main()
