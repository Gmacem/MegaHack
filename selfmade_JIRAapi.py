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
        self.allIssues = []
        self.allUsers = []
        self.notWorkingUsers = []
        self.workingUsers = []
        self.adminUsers = []

    def launchBoard(self):
        self.connectToBoard()
        self.getAllIssues()
        self.getAllProjectUsers()
        self.getWorkingUsers()
        self.getNotWorkingUsers()

    def getAllIssues(self):
        for issue in self.jira.search_issues(jql_str="project="+self.projectKey, maxResults=1000):
            self.allIssues.append(Issue(issue))
        return self.allIssues

    def getAllProjectUsers(self):
        users = self.jira.search_assignable_users_for_projects(username='', projectKeys=[self.projectKey])
        print(users)
        for i in range(len(users)):
            curUser = User(users[i])
            self.allUsers.append(curUser)
            if curUser.name == 'admin':
                self.adminUsers.append(curUser)
        return self.allUsers

    def getWorkingUsers(self):
        workingUsers = set()
        for issue in self.allIssues:
            if issue.status != "Done" and issue.assigneeName is not None and issue.assigneeName != self.jira.myself()['displayName']:
                workingUsers.add(issue.assigneeName)
        for workingUser in workingUsers:
            self.workingUsers.append(User(self.jira.user(workingUser)))
        return self.workingUsers

    def getNotWorkingUsers(self):
        for user in self.allUsers:
            if user.name not in self.workingUsers:
                self.notWorkingUsers.append(user)
        return self.notWorkingUsers

    def createNewIssue(self, summary, description, issueType, assigneeName):
        newIssue = {
                'project': {'id': self.projectId},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issueType},
                'assignee': {'name': assigneeName}
            }
        self.jira.create_issue(fields=newIssue)


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
        self.timeEstimate = issue.raw['fields']['timeestimate']
        self.assignee = issue.raw['fields']['assignee']
        if issue.raw['fields']['assignee'] != None:
            self.assigneeName = issue.raw['fields']['assignee']['displayName']
            self.assigneeKey = issue.raw['fields']['assignee']['key']
            self.assigneeAccountId = issue.raw['fields']['assignee']['accountId']
        else:
            self.assigneeName = None
            self.assigneeKey = None
            self.assigneeAccountId = None

    def setParams(self, summary, description, assigneeKey, labels):
        fileds = {
            'summary': summary,
            'description': description,
            'assignee': {'key': assigneeKey},
            'labels': labels
        }
        print(self)
        self.update(fields=fileds)


class User(object):
    def __init__(self, user):
        self.raw_value = user.raw
        self.key = user.raw['key']
        self.accountId = user.raw['accountId']
        self.name = user.raw['name']
        self.email = user.raw['emailAddress']
        self.displayName = user.raw['displayName']
        self.active = user.raw['active']


if __name__ == "__main__":
    board = Board('https://megatm.atlassian.net', 'mega.7eam@gmail.com', 'satxon-7tinfu-piTpiz', 'MegaTeam', 'MEGAT board')
    board.launchBoard()


    print("Working users:")
    for workingUser in board.workingUsers:
        print(workingUser.displayName)

    print("\nNot working users:")
    for notWorkingUser in board.notWorkingUsers:
        print(notWorkingUser.displayName)

    print("\nAdmins:")
    for admin in board.adminUsers:
        print(admin.displayName)

    # issue.setParams(summary="New Task", description="New task description", assigneeKey=, labels=)

    # board.createNewIssue(summary="New issue3", description="Some description", issueType="Story", assigneeName="dogn2000")
    # print(Issue(board.jira.issue('MEGAT-1')).assigneeName)
    # print(Issue(board.jira.issue('MEGAT-4')).progress)
    # print(Issue(board.jira.issue('MEGAT-4')).progressTotal)

    #Find all issues example
    # for issue in board.allIssues:
    #     print("Key: " + str(issue.key))
    #     print("Summary: " + str(issue.summary))
    #     print("Description: " + str(issue.description))
    #     print("")