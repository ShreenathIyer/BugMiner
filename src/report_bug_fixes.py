"""
ECS 260 Final Project: BugMiner
Find the commit id pairs which includes a buggy commit and a patch for the bug.
Args:
    Param 1: <project_name>
Returns:
    This script returns the commit id pairs for bugs and its fixes in a given project.
"""
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

    # Argument parser for the script. Returns name of the project.
    def parse_arguments(self):
        parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                            help="create git commit pairs for given project")
        parser.add_argument("project_name", type=str, help="name of the project")
        args = parser.parse_args()
        return args.project_name

    # Returns true if the given URL is for a bug; otherwise returns false
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

    # Parses all json files in resources and returns one json object containing the history of all git commits
    def parse_json(self, current_project):
        all_data = list()
        if current_project == "math" or current_project == "lang":
            current_project = "COMMONS-" + current_project
        json_path = os.path.abspath(self.resources + str(current_project))
        for filename in glob.glob(os.path.join(json_path, '*.json')):
            json_file = open(filename, 'r', encoding='utf-8')
            current_json_data = json.load(json_file)
            if "items" in current_json_data:
                all_data.extend(current_json_data["items"])
        # print(len(all_data))
        return all_data

    # Returns a valid jira id from regex
    def is_valid_jira_id(self, jira_id):
        if jira_id is not None:
            return jira_id.group().upper()
        return jira_id

    # Creates a new directory for every project if it doesn't exist and writes the final output to a json file
    def dump_to_json(self, commit_pairs, project_name):
        path_to_output_directory = os.path.abspath(
            "../output/" + project_name)
        if not os.path.exists(path_to_output_directory):
            os.mkdir(path_to_output_directory)
        path_to_output = os.path.abspath("../output/"+project_name+"/commit_pairs_"+project_name+".json")
        filewrite = open(path_to_output, 'w', encoding='utf-8')
        json.dump(commit_pairs, filewrite)
        filewrite.close()
        print("[%s]: Writing to json file complete \n" % project_name.upper())

    # Returns the jira URL for a project based on its name
    def create_url(self, project_name, urls_dict, jira_id):
        if project_name in urls_dict and jira_id is not None:
            return urls_dict[project_name] + jira_id.group()
        return None

    # Calls the function to generate git commit history after parsing the argument project name
    def generate_history(self, project_name):
        obj = CreateGitCommitHistory()
        if project_name == "MATH" or project_name == "LANG":
            git_project_name = "COMMONS-" + project_name
        else:
            git_project_name = project_name
        obj.create_commit_history(git_project_name)

    # Iterates over the generated resource files to generate the commit pairs containing the bug and the fix
    def create_commit_pairs(self, project_name, jira_urls):
        self.data = self.parse_json(project_name)
        self.commit_couples = [{"count": 0, "commit_pairs": {}}]
        print("[%s]: Creating commit pairs for potential bugs \n" % project_name.upper())
        for commit_history in self.data:
            if project_name in commit_history["commit"]["message"].lower():
                jira_id = re.search(r"\w*"+project_name+"-\w*", commit_history["commit"]["message"].lower())
                term = self.is_valid_jira_id(jira_id)
                url = self.create_url(project_name.upper(), jira_urls, jira_id)
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

    # Gets a list of all projects, and runs the create_commit_pairs depending on the argument
    def get_bugs(self):
        project_obj = GetAllProjects()
        all_projects_dict = project_obj.read_projects_from_csv()
        all_projects = list(all_projects_dict.keys())
        if self.project_name in all_projects:
            self.generate_history(self.project_name)
            self.create_commit_pairs(self.project_name.lower(), all_projects_dict)
        elif self.project_name == "ALL":
            for current_project in all_projects:
                self.generate_history(current_project)
                self.create_commit_pairs(current_project.lower(), all_projects_dict)
        else:
            print("\n Invalid project name. Refer to projects.csv for list of all projects.")


if __name__ == "__main__":
    report = ReportBugFixes()
    report.get_bugs()
