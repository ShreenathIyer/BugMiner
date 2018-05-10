import os
import json
import re

class ReportBugFixes(object):
    def __init__(self):
        self.json_path = os.path.abspath("../../resources/commits.json")
        self.data = self.parse_json()
        # self.keyword = "fix"
        self.commit_couples = [{"count": 0, "commit_pairs": {}}]
        # self.couple_half = False
        self.need_next = False
        self.prev = 0

    def parse_json(self):
        json_file = open(self.json_path, 'r', encoding='utf-8')
        return json.load(json_file)

    def create_commit_pairs(self):
        for commit_history in self.data["items"]:
            project_name = commit_history["repository"]["name"].lower()
            if self.need_next:
                self.commit_couples[0]["commit_pairs"][self.prev].append(commit_history["sha"])
                self.need_next = False

            if project_name in commit_history["commit"]["message"].lower():
                jira_id = re.search(r"\w*"+project_name+"-\w*", commit_history["commit"]["message"].lower())
                if jira_id is not None and jira_id.group() not in self.commit_couples[0]["commit_pairs"]:
                    self.commit_couples[0]["count"] += 1
                    self.commit_couples[0]["commit_pairs"][jira_id.group().upper()] = list()
                    self.commit_couples[0]["commit_pairs"][jira_id.group().upper()].append(commit_history["sha"])
                    self.need_next = True
                    self.prev = jira_id.group().upper()
        # for commit_history in self.data["items"]:
        #     if re.search(r"\bfix\b|\bfixed\b", commit_history["commit"]["message"].lower()):
        #         self.commit_couples.append(commit_history["sha"].split())
        #         self.couple_half = True
        #     elif self.couple_half:
        #         self.commit_couples[(len(self.commit_couples) - 1)].append(commit_history["sha"])
        #         self.couple_half = False
        return self.commit_couples


if __name__ == "__main__":
    report = ReportBugFixes()
    print(report.create_commit_pairs())
