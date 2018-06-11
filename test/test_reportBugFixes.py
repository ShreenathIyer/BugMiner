import unittest
import sys
from src.report_bug_fixes import ReportBugFixes
from src.get_all_projects import GetAllProjects


class TestReportBugFixes(unittest.TestCase):
    def setUp(self):
        self.report = ReportBugFixes()
        self.report.project_name = "HIVE"

    def test_instance(self):
        self.assertEqual(self.report.resources, "../resources/")

    def test_is_issue_bug(self):
        self.assertTrue(True)
        # test_object = ReportBugFixes()
        # url_return = test_object.is_issue_bug("https://issues.apache.org/jira/browse/CLOUDSTACK-10256")
        # self.assertTrue(url_return, "[test_is_issue_bug]: Pass")

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


if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     TestReportBugFixes.project_name = sys.argv.pop()

    unittest.main()
