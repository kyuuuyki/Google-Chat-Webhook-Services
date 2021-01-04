import re
import sys

from json import dumps
from httplib2 import Http

def isStringBlank(string):
    return not (string and string.strip())

def getThreadKey(applicationName, mergeRequestNumber):
    threadKey = ""

    """Merge Request"""
    if not isStringBlank(mergeRequestNumber):
        threadKey = re.sub('[^A-Za-z0-9]+', '', applicationName) + "-merge-request-" + mergeRequestNumber

    return threadKey

def getConfigurations(configurationString):
    CONFIGURATIONS = []
    if not isStringBlank(configurationString):
        CONFIGURATIONS = re.findall(r"[\w']+", configurationString)
        print(CONFIGURATIONS)
    return CONFIGURATIONS

def getBuildStatusTitle(buildStatus):
    if buildStatus == "0":
        return "Build Succeeded!"
    else:
        return "Build Failed"

def getBuildStatusIcon(buildStatus):
    if buildStatus == "0":
        return "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/144/apple/271/party-popper_1f389.png"
    else:
        return "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/144/apple/271/fire_1f525.png"

def getMergeRequestURL(mergeRequestNumber, repositoryURL):
    PULL_REQUEST_URL = repositoryURL.split("@")
    PULL_REQUEST_URL = PULL_REQUEST_URL[1]
    PULL_REQUEST_URL = PULL_REQUEST_URL.replace(":", "/")
    PULL_REQUEST_URL = PULL_REQUEST_URL.replace(".git", "")

    if "bitbucket" in PULL_REQUEST_URL:
        PULL_REQUEST_URL = PULL_REQUEST_URL + "/pull-requests/" + mergeRequestNumber
    elif "gitlab" in PULL_REQUEST_URL:
        PULL_REQUEST_URL = PULL_REQUEST_URL + "/-/merge_requests/" + mergeRequestNumber

    return PULL_REQUEST_URL

def getJIRAContent(gitMessage, jiraOrganizationName, jiraTeamName):
    jiraContent = ""
    if not isStringBlank(gitMessage) and not isStringBlank(jiraTeamName):
        print("\nExtracted Jira Issue Number (s):")
    
        JIRA_ISSUE_NUMBERS = []
        
        JIRA_ISSUE_NUMBERS_FRAGMENTS = gitMessage.split(jiraTeamName)
        JIRA_ISSUE_NUMBERS_FRAGMENTS = JIRA_ISSUE_NUMBERS_FRAGMENTS[1:]

        for JIRA_ISSUE_NUMBERS_FRAGMENT in JIRA_ISSUE_NUMBERS_FRAGMENTS:
        
            JIRA_ISSUE_NUMBER_FRAGMENTS = re.findall(r"[\w']+", JIRA_ISSUE_NUMBERS_FRAGMENT)
            for JIRA_ISSUE_NUMBER_FRAGMENT in JIRA_ISSUE_NUMBER_FRAGMENTS:
                
                if JIRA_ISSUE_NUMBER_FRAGMENT.isnumeric():

                    if not (JIRA_ISSUE_NUMBER_FRAGMENT in JIRA_ISSUE_NUMBERS):
                        print(JIRA_ISSUE_NUMBER_FRAGMENT)
                        JIRA_ISSUE_NUMBERS.append(JIRA_ISSUE_NUMBER_FRAGMENT)

                    break

        if len(JIRA_ISSUE_NUMBERS) > 0:

            for JIRA_ISSUE_NUMBER in JIRA_ISSUE_NUMBERS:
                JIRA_URL = "https://" + jiraOrganizationName + ".atlassian.net/browse/" + jiraTeamName + "-" + JIRA_ISSUE_NUMBER
                jiraContent = jiraContent + "<a href=" + JIRA_URL + ">" + jiraTeamName + "-" + JIRA_ISSUE_NUMBER + "</a><br>"

    return jiraContent

def getTaggedUsersContent(developerUserIDs, testerUserIDs, mergeRequestNumber, buildInstallURL):
    usersContent = ""
    USER_IDS = []
    
    if (not isStringBlank(developerUserIDs)) and (not isStringBlank(mergeRequestNumber)):
        
        print("\nExtracted Developer UserID (s):")
        
        TEAM_DEVELOPER_IDS = re.findall(r"[\w']+", developerUserIDs)
        for TEAM_DEVELOPER_ID in TEAM_DEVELOPER_IDS:
        
            print(TEAM_DEVELOPER_ID)
            USER_IDS.append(TEAM_DEVELOPER_ID)
    
    if (not isStringBlank(testerUserIDs)) and (not isStringBlank(buildInstallURL)):
        
        print("\nExtracted Tester UserID (s):")
        
        TEAM_TESTER_IDS = re.findall(r"[\w']+", testerUserIDs)
        for TEAM_TESTER_ID in TEAM_TESTER_IDS:
        
            print(TEAM_TESTER_ID)
            USER_IDS.append(TEAM_TESTER_ID)
            
    if len(USER_IDS) > 0:
        for USER_ID in USER_IDS:
            usersContent = usersContent + "<users/" + USER_ID + "> "

    return usersContent

def main():

    scriptURL = str(sys.argv[1])

    jiraOrganizationName = str(sys.argv[2])
    jiraTeamName = str(sys.argv[3])

    applicationName = str(sys.argv[4])

    buildStatus = str(sys.argv[5])
    buildNumber = str(sys.argv[6])
    buildWorkflowName = str(sys.argv[7])
    buildURL = str(sys.argv[8])
    buildInstallURL = str(sys.argv[9])

    gitBranchName = str(sys.argv[10])
    gitMessage = str(sys.argv[11])
    
    mergeRequestNumber = str(sys.argv[12])
    mergeRequestDestinationBranchName = str(sys.argv[13])

    repositoryURL = str(sys.argv[14])
    
    developerUserIDs = str(sys.argv[15])
    testerUserIDs = str(sys.argv[16])

    buildNote = str(sys.argv[17])

    configurationString = str(sys.argv[18])

    """INTERNAL VARIABLES"""
    threadKey = getThreadKey(applicationName, mergeRequestNumber)
    configurationOptions = getConfigurations(configurationString)

    """Card Header"""
    cardHeaderTitle = "<b>" + getBuildStatusTitle(buildStatus) + "</b>"
    cardHeaderSubtitle = applicationName + " | " + gitBranchName
    cardHeaderImageUrl = getBuildStatusIcon(buildStatus)
    cardHeader = {
        "title": cardHeaderTitle, 
        "subtitle": cardHeaderSubtitle,
        "imageUrl": cardHeaderImageUrl,
        "imageStyle": "IMAGE"
    }
    
    cardContents = []
    
    """Merge Request Section"""
    mergeRequestURL = getMergeRequestURL(mergeRequestNumber, repositoryURL)
    if not isStringBlank(mergeRequestNumber):
        mergeRequestSection = {
            "widgets": [
                {
                    "keyValue": {
                        "topLabel": "Request to merge into",
                        "content": mergeRequestDestinationBranchName,
                        "contentMultiline": "false",
                        "onClick": {
                            "openLink": {
                                "url": mergeRequestURL
                            }
                        },
                        "iconUrl": "https://www.seekicon.com/free-icon-download/git-pull-request-outline-icon_1.png",
                        "button": {
                            "textButton": {
                                "text": "#" + mergeRequestNumber,
                                "onClick": {
                                    "openLink": {
                                        "url": mergeRequestURL
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }
        cardContents.append(mergeRequestSection)

    """Detail Section"""
    if not ("isBuildDetailDisabled" in configurationOptions):
        detailSectionWidgets = [
            {
                "keyValue": {
                    "topLabel": "Build No.",
                    "content": "#" + buildNumber,
                    "onClick": {
                        "openLink": {
                            "url": buildURL
                        }
                    }
                }
            }
        ]

        if not ("isBuildWorkflowDisabled" in configurationOptions):
            workflowWidget = {
                "keyValue": {
                    "topLabel": "Workflow",
                    "content": buildWorkflowName
                }
            }
            detailSectionWidgets.append(workflowWidget)

        if not isStringBlank(buildNote):
            buildNoteWidget = {
                "keyValue": {
                    "topLabel": "Note",
                    "content": buildNote
                }
            }
            detailSectionWidgets.append(buildNoteWidget)

        detailSection = {
            "header": "Details",
            "widgets": detailSectionWidgets
        }
        cardContents.append(detailSection)

    """Jira Section"""
    jiraContent = getJIRAContent(gitMessage, jiraOrganizationName, jiraTeamName)
    if not isStringBlank(jiraContent):
        jiraContentSection = {
            "header": "Related Issue(s)",
            "widgets": [
                {
                    "textParagraph": {
                        "text": jiraContent
                    }
                }
            ]
        }
        cardContents.append(jiraContentSection)

    """Git Message Section"""
    if (not isStringBlank(gitMessage)) and ("isGitMessageEnabled" in configurationOptions):
        gitMessageSection = {
            "header": "Git Message",
            "widgets": [
                {
                    "textParagraph": {
                        "text": gitMessage
                    }
                }
            ]
        }
        cardContents.append(gitMessageSection)

    """Public Install Page"""
    if not isStringBlank(buildInstallURL):
        buildInstallSection = {
            "widgets": [
                {
                    "buttons": [
                        {
                            "textButton": {
                                "text": "Public Install Page",
                                "onClick": {
                                    "openLink": {
                                        "url": buildInstallURL
                                    }
                                }
                            }
                        }
                    ]
                }
            ]
        }
        cardContents.append(buildInstallSection)

    """Card Data"""
    card = [
        {
            "header": cardHeader,
            "sections": cardContents
        }
    ]

    """Notify Developers"""
    text = getTaggedUsersContent(developerUserIDs, testerUserIDs, mergeRequestNumber, buildInstallURL)
        
    """POST MESSAGE"""
    bot_message = {
        'text': text,
        'cards': card
    }
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    URL = scriptURL
    if not isStringBlank(threadKey):
        URL = URL + "&threadKey=" + threadKey

    response = http_obj.request(
        uri=URL,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    print(response)

if __name__ == '__main__':
    main()
