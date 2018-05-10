import os
import json


class ReportBugFixes(object):
    def __init__(self):
        self.json_path = os.path.abspath("../../resources/commits.json")
        self.data = self.parse_json()
        self.keyword = "fix"
        self.commit_couples = list()
        self.couple_half = False

    def parse_json(self):
        json_file = open(self.json_path, 'r', encoding='utf-8')
        return json.load(json_file)

    def create_commit_pairs(self):
        for commit_history in self.data["items"]:
            if self.keyword in commit_history["commit"]["message"].lower().split():
                self.commit_couples.append(commit_history["sha"].split())
                self.couple_half = True
            elif self.couple_half:
                self.commit_couples[(len(self.commit_couples) - 1)].append(commit_history["sha"])
                self.couple_half = False
        return self.commit_couples


if __name__ == "__main__":
    report = ReportBugFixes()
    print(report.create_commit_pairs())
