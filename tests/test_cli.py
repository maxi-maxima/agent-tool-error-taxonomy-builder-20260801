import unittest

from agent_tool_error_taxonomy_builder_20260801.cli import analyze, sarif


class AnalyzeTests(unittest.TestCase):
    def test_classifies_common_agent_errors(self):
        text = 'tool failed: 429 rate limit\nJSONDecodeError invalid json\npermission denied writing file\n'
        report = analyze(text)
        self.assertEqual(report['total_events'], 3)
        self.assertEqual(report['counts']['rate_limit'], 1)
        self.assertEqual(report['counts']['schema'], 1)
        self.assertEqual(report['counts']['auth'], 1)

    def test_sarif_maps_events_to_log_locations(self):
        report = analyze('tool failed: 429 rate limit\nJSONDecodeError invalid json\n')
        payload = sarif(report, 'logs/agent.log')
        self.assertEqual(payload['version'], '2.1.0')
        results = payload['runs'][0]['results']
        self.assertEqual([result['ruleId'] for result in results], ['rate_limit', 'schema'])
        self.assertEqual(results[0]['locations'][0]['physicalLocation']['artifactLocation']['uri'], 'logs/agent.log')
        self.assertEqual(results[1]['locations'][0]['physicalLocation']['region']['startLine'], 2)


if __name__ == '__main__':
    unittest.main()
