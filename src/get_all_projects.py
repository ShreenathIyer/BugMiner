"""
Read the projects from projects.csv
"""
import csv


class GetAllProjects:
    def __init__(self):
        pass

    # Return a list of all projects
    def read_projects_from_csv(self):
        reader = csv.DictReader(open('../resources/projects.csv'))
        projects = {}
        for row in reader:
            projects[row['Jira Name of the project']] = row['JiraURL']
        return projects


if __name__ == "__main__":
    pass
    # obj = GetAllProjects()
    # print(obj.read_projects_from_csv())
