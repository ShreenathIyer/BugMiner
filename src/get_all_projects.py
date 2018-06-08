import pandas as pd
import csv 

class GetAllProjects:
    def __init__(self):
        pass

    def read_projects_from_csv(self):
        reader = csv.DictReader(open('../resources/projects.csv'))
        projects = {}
        for row in reader:
            projects[row['Jira Name of the project']] = row['JiraURL']
        return projects 

        #print(result)
        #df = pd.read_csv("../resources/projects.csv")
        #print("df is" + df)
        #return df['Jira Name of the project'].tolist()


if __name__ == "__main__":
     obj = GetAllProjects()
     print(obj.read_projects_from_csv())
     pass
