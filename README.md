# BugMiner
New Mining algorithm for identifying the pair of commit ids (one with the bug and the other which resolves it).

This algorithm uses git commit history and the commit ids in JIRA to mine and report bugs.

REQUIREMENTS:
python3.x

USAGE:
python3 report_bug_fixes.py <project_name>

The project names can be found under resources/projects.csv.

For example, to create commit pairs for a specific project, run
python3 report_bug_fixes.py SHIRO

In order to create commit pairs for all projects, run
python3 report_bug_fixes.py ALL
