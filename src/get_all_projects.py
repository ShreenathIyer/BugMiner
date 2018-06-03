import pandas as pd

class GetAllProjects:
    def __init__(self):
        pass

    def read_projects_from_csv(self):
        df = pd.read_csv("../resources/projects.csv")
        return df['Jira Name of the project'].tolist()


if __name__ == "__main__":
    # obj = GetAllProjects()
    # print(obj.read_projects_from_csv())
    pass
