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

def getConfigurationOptions(configurationString):
    configurationOptions = []
    if not isStringBlank(configurationString):
        configurationOptions = re.findall(r"[\w']+", configurationString)
        print(configurationOptions)
    return configurationOptions

def getBuildStatusTitle(buildStatus):
    if buildStatus == "0":
        return "Build Succeeded!"
    else:
        return "Build Failed"

def getBuildStatusIcon(scriptRepositoryURL, buildStatus):
    if buildStatus == "0":
        return scriptRepositoryURL + "/assets/images/check-mark.png"
    else:
        return scriptRepositoryURL + "/assets/images/cross-mark.png"

def getMergeRequestURL(mergeRequestNumber, repositoryURL):
    mergeRequestURL = ""
    try:
        mergeRequestURL = repositoryURL.split("@")
        mergeRequestURL = mergeRequestURL[1]
        mergeRequestURL = mergeRequestURL.replace(":", "/")
        mergeRequestURL = mergeRequestURL.replace(".git", "")

        if "bitbucket" in mergeRequestURL:
            mergeRequestURL = mergeRequestURL + "/pull-requests/" + mergeRequestNumber
        elif "gitlab" in mergeRequestURL:
            mergeRequestURL = mergeRequestURL + "/-/merge_requests/" + mergeRequestNumber
    except:
        print("Could not extract Merge Request URL")

    return mergeRequestURL

def getJIRAContent(gitMessage, jiraOrganizationName, jiraTeamName):
    jiraContent = ""
    if not isStringBlank(gitMessage) and not isStringBlank(jiraTeamName):
        print("\nExtracted Jira Issue Number (s):")
    
        jiraIssueNumbers = []
        
        jiraIssueNumbersFragments = gitMessage.split(jiraTeamName)
        jiraIssueNumbersFragments = jiraIssueNumbersFragments[1:]

        for jiraIssueNumbersFragment in jiraIssueNumbersFragments:
        
            jiraIssueNumberFragments = re.findall(r"[\w']+", jiraIssueNumbersFragment)
            for jiraIssueNumberFragment in jiraIssueNumberFragments:
                
                if jiraIssueNumberFragment.isnumeric():

                    if not (jiraIssueNumberFragment in jiraIssueNumbers):
                        print(jiraIssueNumberFragment)
                        jiraIssueNumbers.append(jiraIssueNumberFragment)

                    break

        if len(jiraIssueNumbers) > 0:
            for jiraIssueNumber in jiraIssueNumbers:
                jiraIssueURL = "https://" + jiraOrganizationName + ".atlassian.net/browse/" + jiraTeamName + "-" + jiraIssueNumber
                jiraContent = jiraContent + "<a href=" + jiraIssueURL + ">" + jiraTeamName + "-" + jiraIssueNumber + "</a><br>"

    return jiraContent

def getTaggedUsersContent(developerUserIDs, testerUserIDs, mergeRequestNumber, buildInstallURL):
    usersContent = ""
    taggedUserIDs = []
    
    if (not isStringBlank(developerUserIDs)) and (not isStringBlank(mergeRequestNumber)):
        print("\nExtracted Developer UserID (s):")
        
        developerIDs = re.findall(r"[\w']+", developerUserIDs)
        for developerID in developerIDs:
        
            print(developerID)
            taggedUserIDs.append(developerID)
    
    if (not isStringBlank(testerUserIDs)) and (not isStringBlank(buildInstallURL)):
        print("\nExtracted Tester UserID (s):")
        
        testerIDs = re.findall(r"[\w']+", testerUserIDs)
        for testerID in testerIDs:
        
            print(testerID)
            taggedUserIDs.append(testerID)
            
    if len(taggedUserIDs) > 0:
        for taggedUserID in taggedUserIDs:
            usersContent = usersContent + "<users/" + taggedUserID + "> "

    return usersContent

def main():

    scriptURL = str(sys.argv[1])
    scriptRepositoryURL = str(sys.argv[2])

    jiraOrganizationName = str(sys.argv[3])
    jiraTeamName = str(sys.argv[4])

    applicationName = str(sys.argv[5])

    buildStatus = str(sys.argv[6])
    buildNumber = str(sys.argv[7])
    buildWorkflowName = str(sys.argv[8])
    buildURL = str(sys.argv[9])
    buildInstallURL = str(sys.argv[10])

    gitBranchName = str(sys.argv[11])
    gitMessage = str(sys.argv[12])
    
    mergeRequestNumber = str(sys.argv[13])
    mergeRequestDestinationBranchName = str(sys.argv[14])

    repositoryURL = str(sys.argv[15])
    
    developerUserIDs = str(sys.argv[16])
    testerUserIDs = str(sys.argv[17])

    buildNote = str(sys.argv[18])

    configurationString = str(sys.argv[19])

    """INTERNAL VARIABLES"""
    threadKey = getThreadKey(applicationName, mergeRequestNumber)
    configurationOptions = getConfigurationOptions(configurationString)

    """Card Header"""
    cardHeaderTitle = "<b>" + getBuildStatusTitle(buildStatus) + "</b>"
    cardHeaderSubtitle = applicationName + " | " + gitBranchName
    cardHeaderImageUrl = getBuildStatusIcon(scriptRepositoryURL, buildStatus)
    cardHeader = {
        "title": cardHeaderTitle, 
        "subtitle": cardHeaderSubtitle,
        "imageUrl": cardHeaderImageUrl,
        "imageStyle": "IMAGE"
    }
    
    cardContents = []
    
    """Merge Request Section"""
    mergeRequestURL = getMergeRequestURL(mergeRequestNumber, repositoryURL)
    mergeRequestIconURL = scriptRepositoryURL + "/assets/images/mr.png"
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
                        "iconUrl": mergeRequestIconURL,
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

    postURL = scriptURL
    if not isStringBlank(threadKey):
        postURL = postURL + "&threadKey=" + threadKey

    response = http_obj.request(
        uri=postURL,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    print(response)

if __name__ == '__main__':
    main()
