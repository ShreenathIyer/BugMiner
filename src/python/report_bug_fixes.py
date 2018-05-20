import os
import json
import re
from bs4 import BeautifulSoup
import urllib.request as urllib2


class ReportBugFixes(object):
    def __init__(self):
        self.json_path = os.path.abspath("../../output/commits.json")
        self.data = self.parse_json()
        self.commit_couples = [{"count": 0, "commit_pairs": {}}]

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

    def parse_json(self):
        json_file = open(self.json_path, 'r', encoding='utf-8')
        return json.load(json_file)

    def is_valid_jira_id(self, jira_id):
        if jira_id is not None:
            return jira_id.group().upper()
        return jira_id

    def create_url(self, jira_id):
        url = 'https://issues.apache.org/jira/browse/'
        if jira_id is not None:
            return url + jira_id
        return None

    def create_commit_pairs(self):
        for commit_history in self.data["items"]:
            project_name = commit_history["repository"]["name"].lower()
            if project_name in commit_history["commit"]["message"].lower():
                jira_id = re.search(r"\w*"+project_name+"-\w*", commit_history["commit"]["message"].lower())
                term = self.is_valid_jira_id(jira_id)
                url = self.create_url(term)
                if term and jira_id.group() not in self.commit_couples[0]["commit_pairs"]\
                        and self.is_issue_bug(url):
                    self.commit_couples[0]["count"] += 1
                    self.commit_couples[0]["commit_pairs"][term] = list()
                    self.commit_couples[0]["commit_pairs"][term].append(commit_history["sha"])
                    self.commit_couples[0]["commit_pairs"][term].\
                        append(commit_history["parents"][0]["sha"])
        return self.commit_couples


if __name__ == "__main__":
    report = ReportBugFixes()
    print(report.create_commit_pairs())
