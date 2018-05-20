import os
import json
import re
from bs4 import BeautifulSoup
import urllib.request as urllib2

class ReportBugFixes(object):
    def __init__(self):
        self.json_path = os.path.abspath("../../resources/commits.json")
        self.data = self.parse_json()
        self.commit_couples = [{"count": 0, "commit_pairs": {}}]

    def is_issue_bug(self, url):
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")

        file1 = open('out2.txt', 'w')
        file1.write(str(soup))
        file1.close()

        file1 = open('out2.txt')
        term = "title=\"Bug"
        file2 = open('out3.txt', 'a')

        for line in file1:
            line.strip().split('/n')
            if term in line:
                myTitle = soup.html.head.title
                file2.write(str(myTitle.contents))
                file2.write("\n")
                break

        file1.close()
        file2.close()



    def parse_json(self):
        json_file = open(self.json_path, 'r', encoding='utf-8')
        return json.load(json_file)

    def create_commit_pairs(self):
        for commit_history in self.data["items"]:
            project_name = commit_history["repository"]["name"].lower()

            if project_name in commit_history["commit"]["message"].lower():
                jira_id = re.search(r"\w*"+project_name+"-\w*", commit_history["commit"]["message"].lower())
                if jira_id is not None and jira_id.group() not in self.commit_couples[0]["commit_pairs"]:
                    self.commit_couples[0]["count"] += 1
                    self.commit_couples[0]["commit_pairs"][jira_id.group().upper()] = list()
                    self.commit_couples[0]["commit_pairs"][jira_id.group().upper()].append(commit_history["sha"])
                    self.commit_couples[0]["commit_pairs"][jira_id.group().upper()].append(commit_history["parents"][0]["sha"])
                    self.prev = jira_id.group().upper()

                    term = jira_id.group().upper()
                    url = 'https://issues.apache.org/jira/browse/' + term
                    self.is_issue_bug(url)
        return self.commit_couples




if __name__ == "__main__":
    report = ReportBugFixes()
    print(report.create_commit_pairs())
    print()
