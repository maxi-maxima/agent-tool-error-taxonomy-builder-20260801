import unittest

from agent_tool_error_taxonomy_builder_20260801.cli import analyze


class AnalyzeTests(unittest.TestCase):
    def test_classifies_common_agent_errors(self):
        text = 'tool failed: 429 rate limit\nJSONDecodeError invalid json\npermission denied writing file\n'
        report = analyze(text)
        self.assertEqual(report['total_events'], 3)
        self.assertEqual(report['counts']['rate_limit'], 1)
        self.assertEqual(report['counts']['schema'], 1)
        self.assertEqual(report['counts']['auth'], 1)


if __name__ == '__main__':
    unittest.main()
