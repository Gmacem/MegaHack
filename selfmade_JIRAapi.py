from jira import *

class Board(object):
    def __init__(self, serverUrl, username, password, projectName, boardName):
        self.serverUrl = serverUrl
        self.username = username
        self.password = password
        self.projectName = projectName
        self.projectKey = ""
        self.projectId = ""
        self.boardName = boardName
        self.issues = []

    def findAllIssues(self):
        self.issues = self.jira.search_issues(jql_str="project="+self.projectKey, maxResults=1000)

    def connectToBoard(self):
        options = {'server': self.serverUrl}
        authData = (self.username, self.password)
        self.jira = JIRA(server=self.serverUrl, options=options, auth=authData)
        for project in self.jira.projects():
            if project.name == self.projectName:
                self.projectKey = project.key
                self.projectId = project.id


    def checkBoard(self):
        options = {'server': self.serverUrl}
        authData = (self.username, self.password)
        try:
            self.jira = JIRA(server=self.serverUrl, options=options, auth=authData)
        except Exception as e:
            print(e)
            print("Failed to connect to board")
            return False
        return True

    def checkProject(self):
        options = {'server': self.serverUrl}
        authData = (self.username, self.password)
        jira = JIRA(server=self.serverUrl, options=options, auth=authData)
        print(jira.projects()[0].name)
        projects = jira.projects()
        projects_count = len(projects)
        isProjectFinded = False
        if projects_count > 0:
            for project in jira.projects():
                if self.projectName == project.name:
                    isProjectFinded = True
                    break
        else:
            print("Projects count == 0")
            return False
        if isProjectFinded:
            return True
        else:
            print("Failed to find project!")
            return False


    def checkServer(self):
        try:
            JIRA(server=self.serverUrl)
        except Exception as e:
            print(e)
            print("Failed to connect to server")
            return False
        return True


if __name__ == "__main__":
    board = Board('https://megatm.atlassian.net', 'mega.7eam@gmail.com', 'satxon-7tinfu-piTpiz', 'MegaTeam', 'MEGAT board')
    board.connectToBoard()
    print(board.jira.projects())
    board.findAllIssues()
    for issue in board.issues:
        print(issue.raw)