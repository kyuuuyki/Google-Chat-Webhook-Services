import re
import sys

from json import dumps
from httplib2 import Http

def isStringBlank(string):
    return not (string and string.strip())

def main():

    GOOGLE_CHAT_WEBHOOK_URL = str(sys.argv[1])

    JIRA_ORGANIZATION_NAME = str(sys.argv[2])
    JIRA_TEAM_NAME = str(sys.argv[3])

    BITRISE_APP_TITLE = str(sys.argv[4])
    BITRISE_BUILD_STATUS = str(sys.argv[5])
    BITRISE_BUILD_NUMBER = str(sys.argv[6])
    BITRISE_TRIGGERED_WORKFLOW_TITLE = str(sys.argv[7])
    BITRISE_BUILD_URL = str(sys.argv[8])
    BITRISE_PUBLIC_INSTALL_PAGE_URL = str(sys.argv[9])

    BITRISE_GIT_BRANCH = str(sys.argv[10])
    BITRISE_GIT_MESSAGE = str(sys.argv[11])
    
    BITRISE_PULL_REQUEST = str(sys.argv[12])
    BITRISEIO_GIT_BRANCH_DEST = str(sys.argv[13])
    BITRISEIO_PULL_REQUEST_REPOSITORY_URL = str(sys.argv[14])
    
    TEAM_DEVELOPER_USERIDS = str(sys.argv[15])
    TEAM_TESTER_USERIDS = str(sys.argv[16])

    BUILD_NOTE = str(sys.argv[17])

    """STATUS"""
    if BITRISE_BUILD_STATUS == "0":
        BUILD_STATUS_TEXT = "Build Succeeded!"
    else:
        BUILD_STATUS_TEXT = "Build Failed"
        
    """MERGE STATUS"""
    if not isStringBlank(BITRISE_PULL_REQUEST):

        PULL_REQUEST_URL = BITRISEIO_PULL_REQUEST_REPOSITORY_URL.split("@")
        PULL_REQUEST_URL = PULL_REQUEST_URL[1]
        PULL_REQUEST_URL = PULL_REQUEST_URL.replace(":", "/")
        PULL_REQUEST_URL = PULL_REQUEST_URL.replace(".git", "")

        if "bitbucket" in PULL_REQUEST_URL:
            PULL_REQUEST_URL = PULL_REQUEST_URL + "/pull-requests/" + BITRISE_PULL_REQUEST

        elif "gitlab" in PULL_REQUEST_URL:
            PULL_REQUEST_URL = PULL_REQUEST_URL + "/-/merge_requests/" + BITRISE_PULL_REQUEST

        BUILD_STATUS_TEXT = "Merge Request <https://" + PULL_REQUEST_URL + "|#" + BITRISE_PULL_REQUEST + "> " + BUILD_STATUS_TEXT
            
    CHAT_TEXT = "*" + BITRISE_APP_TITLE + " | " + BUILD_STATUS_TEXT + "*"

    """BUILD NUMBER"""
    CHAT_TEXT = CHAT_TEXT + "\n<" + BITRISE_BUILD_URL + "|#" + BITRISE_BUILD_NUMBER + ">"

    """PUBLIC INSTALL LINK"""
    if not isStringBlank(BITRISE_PUBLIC_INSTALL_PAGE_URL):
        CHAT_TEXT = CHAT_TEXT + " • <" + BITRISE_PUBLIC_INSTALL_PAGE_URL + "|Open public install page>"

    CHAT_TEXT = CHAT_TEXT + "\n"

    """BUILD NOTE"""
    if not isStringBlank(BUILD_NOTE):
        CHAT_TEXT = CHAT_TEXT + "\n" + BUILD_NOTE + "\n"
    
    """BRANCH DATA"""
    BRANCH_DATA_TEXT = "\nBranch: `" + BITRISE_GIT_BRANCH + "`"
    if not isStringBlank(BITRISE_PULL_REQUEST):
        BRANCH_DATA_TEXT = BRANCH_DATA_TEXT + " → `" + BITRISEIO_GIT_BRANCH_DEST + "`"

    """WORKFLOW"""
    CHAT_TEXT = CHAT_TEXT + BRANCH_DATA_TEXT + "\nWorkflow: `" + BITRISE_TRIGGERED_WORKFLOW_TITLE + "`"

    """JIRA LINK"""
    if not isStringBlank(BITRISE_GIT_MESSAGE) and not isStringBlank(JIRA_TEAM_NAME):

        print("\nExtracted Jira Issue Number (s):")
    
        JIRA_ISSUE_NUMBERS = []
        
        JIRA_ISSUE_NUMBERS_FRAGMENTS = BITRISE_GIT_MESSAGE.split(JIRA_TEAM_NAME)
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

            CHAT_TEXT = CHAT_TEXT + "\nJira Task(s): "

            for JIRA_ISSUE_NUMBER in JIRA_ISSUE_NUMBERS:
                JIRA_URL = "https://" + JIRA_ORGANIZATION_NAME + ".atlassian.net/browse/" + JIRA_TEAM_NAME + "-" + JIRA_ISSUE_NUMBER
                CHAT_TEXT = CHAT_TEXT + "<" + JIRA_URL + "|" + JIRA_TEAM_NAME + "-" + JIRA_ISSUE_NUMBER + ">, "

            CHAT_TEXT = CHAT_TEXT[:-2]
        
    """GIT MESSAGE"""
    if not isStringBlank(BITRISE_GIT_MESSAGE):
        CHAT_TEXT = CHAT_TEXT + "\n```" + BITRISE_GIT_MESSAGE + "```"
        
    """NOTIFY DEVELOPERS & TESTERS"""
    USER_IDS = []
    
    if (not isStringBlank(TEAM_DEVELOPER_USERIDS)) and (not isStringBlank(BITRISE_PULL_REQUEST)):
        
        print("\nExtracted Developer UserID (s):")
        
        TEAM_DEVELOPER_IDS = re.findall(r"[\w']+", TEAM_DEVELOPER_USERIDS)
        for TEAM_DEVELOPER_ID in TEAM_DEVELOPER_IDS:
        
            print(TEAM_DEVELOPER_ID)
            USER_IDS.append(TEAM_DEVELOPER_ID)
    
    if (not isStringBlank(TEAM_TESTER_USERIDS)) and (not isStringBlank(BITRISE_PUBLIC_INSTALL_PAGE_URL)):
        
        print("\nExtracted Tester UserID (s):")
        
        TEAM_TESTER_IDS = re.findall(r"[\w']+", TEAM_TESTER_USERIDS)
        for TEAM_TESTER_ID in TEAM_TESTER_IDS:
        
            print(TEAM_TESTER_ID)
            USER_IDS.append(TEAM_TESTER_ID)
            
    if len(USER_IDS) > 0:

        CHAT_TEXT = CHAT_TEXT + "\n"

        for USER_ID in USER_IDS:
            CHAT_TEXT = CHAT_TEXT + "<users/" + USER_ID + "> "
        
    """POST MESSAGE"""
    bot_message = {
        'text' : CHAT_TEXT
    }
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=GOOGLE_CHAT_WEBHOOK_URL,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    print(response)

if __name__ == '__main__':
    main()
