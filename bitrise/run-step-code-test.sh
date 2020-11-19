GOOGLE_CHAT_WEBHOOK_URL='https://chat.googleapis.com/v1/spaces/AAAAhHdpKEc/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=RKLEEqXK4WJWW-Eqa_eyunlMARCopm5LPiUdagxKOxs%3D'
GOOGLE_CHAT_WEBHOOK_SERVICES_REPO='https://bitbucket.org/ascend-kyu/google-chat-webhook-services/raw/develop'

JIRA_ORGANIZATION_NAME='truemoney'
JIRA_TEAM_NAME='COMMOBILE'

TEAM_DEVELOPER_USERIDS='106771966467879575916'
TEAM_TESTER_USERIDS=''

BITRISE_APP_TITLE='Go Eats - iOS'
BITRISE_BUILD_STATUS='0'
BITRISE_BUILD_NUMBER='264'
BITRISE_TRIGGERED_WORKFLOW_TITLE='adhoc-staging'
BITRISE_BUILD_URL='https://app.bitrise.io/build/99f56cd6307e7043'
BITRISE_PUBLIC_INSTALL_PAGE_URL='https://app.bitrise.io/artifact/56442812/p/e108a58974073dd482ba34d4ddb603ff'
BITRISE_GIT_BRANCH='develop'
BITRISE_GIT_MESSAGE='Merged in version/1.11.0 (pull request #9)'
BITRISE_PULL_REQUEST=''

curl "$GOOGLE_CHAT_WEBHOOK_SERVICES_REPO/bitrise/run-step-code.sh" | bash -
