import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


PLUGIN = Path(__file__).resolve().parents[2]
HOOK = PLUGIN / 'hooks/context_handoff.py'


class ContextHandoffTests(unittest.TestCase):
    def run_hook(self, event):
        return subprocess.run(
            ['python3', str(HOOK)], input=json.dumps(event),
            text=True, capture_output=True, check=True,
        ).stdout

    def test_configured_command_works_from_another_directory_with_spaces(self):
        config = json.loads((PLUGIN / 'hooks/hooks.json').read_text())
        hook = config['hooks']['SessionStart'][0]
        self.assertEqual(hook['matcher'], '^compact$')
        with tempfile.TemporaryDirectory(prefix='handoff test ') as directory:
            root = Path(directory) / 'plugin with spaces'
            root.symlink_to(PLUGIN, target_is_directory=True)
            result = subprocess.run(
                hook['hooks'][0]['command'], shell=True, cwd=directory,
                env={**os.environ, 'CLAUDE_PLUGIN_ROOT': str(root)},
                input=json.dumps({
                    'hook_event_name': 'SessionStart', 'source': 'compact',
                    'session_id': 'session-1', 'cwd': directory,
                    'transcript_path': '/tmp/transcript with spaces.jsonl',
                    'unrelated_secret': 'must-not-be-forwarded',
                }), text=True, capture_output=True, check=True,
            )
        output = json.loads(result.stdout)['hookSpecificOutput']
        self.assertEqual(output['hookEventName'], 'SessionStart')
        context = output['additionalContext']
        self.assertIn(str(PLUGIN / 'skills/context-handoff/SKILL.md'), context)
        self.assertIn('/tmp/transcript with spaces.jsonl', context)
        self.assertNotIn('must-not-be-forwarded', context)

    def test_other_lifecycle_events_are_silent(self):
        for event in (
            {'hook_event_name': 'SessionStart', 'source': source}
            for source in ('startup', 'resume', 'clear', 'fork')
        ):
            with self.subTest(event=event):
                self.assertEqual(self.run_hook(event), '')
        self.assertEqual(self.run_hook({'hook_event_name': 'PostCompact', 'source': 'compact'}), '')

    def test_transcript_is_optional(self):
        output = self.run_hook({'hook_event_name': 'SessionStart', 'source': 'compact'})
        context = json.loads(output)['hookSpecificOutput']['additionalContext']
        self.assertIsNone(json.loads(context.split('\n', 1)[1])['transcript_path'])

    def test_invalid_event_reports_failure_without_context(self):
        for payload in ('{broken', '[]'):
            result = subprocess.run(
                ['python3', str(HOOK)], input=payload, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, '')
            self.assertIn('context-handoff:', result.stderr)


if __name__ == '__main__':
    unittest.main()
