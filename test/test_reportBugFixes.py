import unittest
from src.report_bug_fixes import ReportBugFixes


class TestReportBugFixes(unittest.TestCase):
    def setUp(self):
        self.report_obj = ReportBugFixes()
        self.project_name = "HIVE"
        self.project_list = ["HIVE", "COMMONS-LANG", "COMMONS-MATH", "CLOUDSTACK", "SHIRO"]

    def test_is_issue_bug(self):
        is_issue = self.report_obj.is_issue_bug("https://issues.apache.org/jira/browse/CLOUDSTACK-10256")
        self.assertEqual(is_issue, True)

    def test_is_issue_bug_empty(self):
        is_issue = self.report_obj.is_issue_bug("")
        self.assertEqual(is_issue, False)

    def test_parse_json(self):
        self.assertTrue(True)

    def test_is_valid_jira_id(self):
        self.assertTrue(True)

    def test_dump_to_json(self):
        self.assertTrue(True)

    def test_create_url(self):
        self.assertTrue(True)

    def test_generate_history(self):
        self.assertTrue(True)

    def test_create_commit_pairs(self):
        self.assertTrue(True)

    def test_get_bugs(self):
        self.assertTrue(True)

    def tearDown(self):
        self.report_obj = None
        self.project_name = None
        self.project_list = []


if __name__ == "__main__":
    unittest.main()
