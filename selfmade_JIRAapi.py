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
        for issue in self.jira.search_issues(jql_str="project="+self.projectKey, maxResults=1000):
            self.issues.append(Issue(issue))

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

class Issue(object):
    def __init__(self, issue):
        self.issue = issue
        self.raw_value = issue.raw
        self.id = issue.raw['id']
        self.link = issue.raw['self']
        self.key = issue.raw['key']
        self.typeName = issue.raw['fields']['issuetype']['name']
        self.typeSubtask = issue.raw['fields']['issuetype']['subtask']
        self.timespent = issue.raw['fields']['timespent']
        self.projectId = issue.raw['fields']['project']['id']
        self.projectName = issue.raw['fields']['project']['name']
        self.projectKey = issue.raw['fields']['project']['key']
        self.workRatio = issue.raw['fields']['workratio']
        self.labels = issue.raw['fields']['labels']
        self.status = issue.raw['fields']['status']['statusCategory']['name']
        self.description = issue.raw['fields']['description']
        self.summary = issue.raw['fields']['summary']
        self.creatorName = issue.raw['fields']['creator']['name']
        self.creatorKey = issue.raw['fields']['creator']['key']
        self.creatorAccountId = issue.raw['fields']['creator']['accountId']
        self.creatorDisplayName = issue.raw['fields']['creator']['displayName']
        self.progress = issue.raw['fields']['progress']['progress']
        self.progressTotal = issue.raw['fields']['progress']['total']

if __name__ == "__main__":
    board = Board('https://megatm.atlassian.net', 'mega.7eam@gmail.com', 'satxon-7tinfu-piTpiz', 'MegaTeam', 'MEGAT board')
    board.connectToBoard()
    print(board.jira.projects())

    #Find all issues example
    board.findAllIssues()
    for issue in board.issues:
        print("Key: " + str(issue.key))
        print("Summary: " + str(issue.summary))
        print("Description: " + str(issue.description))
        print("")