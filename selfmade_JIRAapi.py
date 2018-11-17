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
        self.workers = []

    def getAllIssues(self):
        for issue in self.jira.search_issues(jql_str="project="+self.projectKey, maxResults=1000):
            self.allIssues.append(Issue(issue))
        return self.allIssues

    def getAllProjectUsers(self):
        users = board.jira.search_assignable_users_for_projects(username='', projectKeys=[self.projectKey])
        for user in users:
            self.allUsers.append(user.displayName)
        return users

    def getWorkers(self):
        self.getAllIssues()
        workers = set()
        for issue in self.allIssues:
            if issue.status != "Done" and issue.assigneeName != None:
                workers.add(Worker(issue).name)
        self.workers.append(list(workers))
        return list(workers)

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

    #TODO
    # def setParams(self, board, issueId, summary, description):#, assigneeKey, labels):
    #     issue = board.jira.issue(issueId)
    #     issue.fields.summary = summary
    #     issue.fields.description = description
    #     # new_issue.fields.assignee.key = assigneeKey
    #     issue.update()


class Worker(object):
    def __init__(self, issue):
        self.name = issue.assigneeName
        self.key = issue.assigneeKey
        self.accountId = issue.assigneeAccountId


if __name__ == "__main__":
    board = Board('https://megatm.atlassian.net', 'mega.7eam@gmail.com', 'satxon-7tinfu-piTpiz', 'MegaTeam', 'MEGAT board')
    board.connectToBoard()

    workers = board.getWorkers()
    for worker in workers:
        print(worker)

    # board.getAllProjectUsers()
    # print(board.allUsers)

    # print(board.allIssues[0].raw_value)

    # board.createNewIssue(summary="New issue3", description="Some description", issueType="Story", assigneeName="dogn2000")
    # board.findAllIssues()
    # print(Issue(board.jira.issue('MEGAT-1')).assigneeName)
    # print(Issue(board.jira.issue('MEGAT-4')).progress)
    # print(Issue(board.jira.issue('MEGAT-4')).progressTotal)

    # issues = board.findAllIssues()
    # for issue in issues:
    #     print(str(issue.summary) + ':' + str(issue.assigneeName))

    #Find all issues example
    # board.findAllIssues()
    # for issue in board.issues:
    #     print("Key: " + str(issue.key))
    #     print("Summary: " + str(issue.summary))
    #     print("Description: " + str(issue.description))
    #     print("")