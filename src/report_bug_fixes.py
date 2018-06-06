import os
import json
import re
from bs4 import BeautifulSoup
import urllib.request as urllib2
import argparse
import glob
from src.get_all_projects import GetAllProjects
from src.create_git_commits import CreateGitCommitHistory


class ReportBugFixes(object):
    def __init__(self):
        self.resources = "../resources/"
        self.project_name = str(self.parse_arguments())
        self.data = list()
        self.commit_couples = []

    def parse_arguments(self):
        parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                            help="create git commit pairs for given project")
        parser.add_argument("project_name", type=str, help="name of the project")
        args = parser.parse_args()
        return args.project_name

    def is_issue_bug(self, url):
        if not url:
            return False
        try:
            soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
            file1 = open('httpresponse.txt', 'w')
            file1.write(str(soup))
            file1.close()
            file1 = open('httpresponse.txt', 'r')
            term = "title=\"Bug"
            for line in file1:
                line.strip().split('/n')
                if term in line:
                    file1.close()
                    return True
        except urllib2.HTTPError:
            return False
        return False

    def parse_json(self, current_project):
        all_data = list()
        json_path = os.path.abspath(self.resources + str(current_project))
        for filename in glob.glob(os.path.join(json_path, '*.json')):
            json_file = open(filename, 'r', encoding='utf-8')
            current_json_data = json.load(json_file)
            if "items" in current_json_data:
                all_data.extend(current_json_data["items"])
        # print(len(all_data))
        return all_data

    def is_valid_jira_id(self, jira_id):
        if jira_id is not None:
            return jira_id.group().upper()
        return jira_id

    def dump_to_json(self, commit_pairs, project_name):
        path_to_output_directory = os.path.abspath(
            "../output/" + project_name)
        if not os.path.exists(path_to_output_directory):
            os.mkdir(path_to_output_directory)
        path_to_output = os.path.abspath("../output/"+project_name+"/commit_pairs_"+project_name+".json")
        filewrite = open(path_to_output, 'w', encoding='utf-8')
        json.dump(commit_pairs, filewrite)
        filewrite.close()

    def create_url(self, jira_id):
        url = 'https://issues.apache.org/jira/browse/'
        if jira_id is not None:
            return url + jira_id
        return None

    def generate_history(self, project_name):
        obj = CreateGitCommitHistory()
        obj.create_commit_history(project_name)

    def create_commit_pairs(self, project_name):
        self.data = self.parse_json(project_name)
        self.commit_couples = [{"count": 0, "commit_pairs": {}}]
        for commit_history in self.data:
            if project_name in commit_history["commit"]["message"].lower():
                jira_id = re.search(r"\w*"+project_name+"-\w*", commit_history["commit"]["message"].lower())
                term = self.is_valid_jira_id(jira_id)
                url = self.create_url(term)
                if term and jira_id.group() not in self.commit_couples[0]["commit_pairs"]\
                        and self.is_issue_bug(url):
                    self.commit_couples[0]["count"] += 1
                    self.commit_couples[0]["commit_pairs"][term] = dict()
                    self.commit_couples[0]["commit_pairs"][term]["fixed_bug_sha"] = commit_history["sha"]
                    self.commit_couples[0]["commit_pairs"][term]["parent_bug_sha"] = \
                        commit_history["parents"][0]["sha"]
                    self.commit_couples[0]["commit_pairs"][term]["commit_message"] = \
                        commit_history["commit"]["message"]
        self.dump_to_json(self.commit_couples, project_name.upper())

    def get_bugs(self):
        project_obj = GetAllProjects()
        all_projects = project_obj.read_projects_from_csv()
        if self.project_name in all_projects:
            self.generate_history(self.project_name)
            self.create_commit_pairs(self.project_name.lower())
        elif self.project_name == "ALL":
            for current_project in all_projects:
                self.generate_history(current_project)
                self.create_commit_pairs(current_project.lower())


if __name__ == "__main__":
    report = ReportBugFixes()
    report.get_bugs()
