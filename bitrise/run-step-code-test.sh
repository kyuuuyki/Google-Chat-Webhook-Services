GOOGLE_CHAT_WEBHOOK_URL='https://chat.googleapis.com/v1/spaces/AAAAhHdpKEc/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=RKLEEqXK4WJWW-Eqa_eyunlMARCopm5LPiUdagxKOxs%3D'
GOOGLE_CHAT_WEBHOOK_SERVICES_REPO='https://bitbucket.org/ascend-kyu/google-chat-webhook-services/raw/develop'

JIRA_ORGANIZATION_NAME='truemoney'
JIRA_TEAM_NAME='COMMOBILE'

TEAM_DEVELOPER_USERIDS='106771966467879575916'
TEAM_TESTER_USERIDS=''

BITRISE_APP_TITLE='Go Eats - iOS'
BITRISE_BUILD_STATUS='0'
BITRISE_BUILD_NUMBER='280'
BITRISE_TRIGGERED_WORKFLOW_TITLE='quality-scan'
BITRISE_BUILD_URL='https://app.bitrise.io/build/d1cf7525ae2dff5f'
BITRISE_PUBLIC_INSTALL_PAGE_URL=''
BITRISE_GIT_BRANCH='version/1.11.1'
BITRISE_GIT_MESSAGE="Version/1.11.1

* \[COMMOBILE-7831\] Recalculate discountPrice for iphone1250 coupon
* \[COMMOBILE-7831\] Update CartView's fetchProfile procedure
* \[COMMOBILE-7831\] Attach promotion object to only first applicable object
* Version 1.11.1"
BITRISE_PULL_REQUEST='11'
BITRISEIO_GIT_BRANCH_DEST='develop'

curl "$GOOGLE_CHAT_WEBHOOK_SERVICES_REPO/bitrise/run-step-code.sh" | bash -

