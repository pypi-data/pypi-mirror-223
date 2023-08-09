""" Common Zephyr Constants """
from enum import Enum


class Environment(Enum):
    """ Environment """

    UAT = 'uat'
    SIT = 'sit'
    PROD = 'prod'
    QA = 'qa'
    DEV = 'dev'


class Zone(Enum):
    """The country zones"""

    AR = 'ar'
    BE = 'be'
    BO = 'bo'
    BR = 'br'
    CA = 'ca'
    CL = 'cl'
    CO = 'co'
    DE = 'de'
    DO = 'do'
    EC = 'ec'
    IC = 'ic'
    GB = 'gb'
    HN = 'hn'
    MX = 'mx'
    NL = 'nl'
    PA = 'pa'
    PE = 'pe'
    PH = 'ph'
    PY = 'py'
    SV = 'SV'
    TZ = 'tz'
    US = 'us'
    UY = 'uy'
    ZA = 'za'


_ZONE_NAME_MAP = {
    Zone.AR: 'Argentina',
    Zone.BE: 'Belgium',
    Zone.BO: 'Bolivia',
    Zone.BR: 'Brazil',
    Zone.CA: 'Canada',
    Zone.CL: 'Chile',
    Zone.CO: 'Colombia',
    Zone.DE: 'Germany',
    Zone.DO: 'Dominican Republic',
    Zone.EC: 'Ecuador',
    Zone.IC: 'Canary Island',
    Zone.GB: 'United Kingdom',
    Zone.HN: 'Honduras',
    Zone.MX: 'Mexico',
    Zone.NL: 'Netherlands',
    Zone.PA: 'Panama',
    Zone.PE: 'Peru',
    Zone.PY: 'Paraguay',
    Zone.SV: 'El Salvador',
    Zone.TZ: 'Tanzania',
    Zone.US: 'United States',
    Zone.UY: 'Uruguay',
    Zone.ZA: 'South Africa'}

# Update and Up-to-date Message
UPDATE_MSG = 'This scenario was updated! - Scenario Code: "{scenario_key}"'
UP_TO_DATE_MSG = 'This scenario is up to date! - Scenario Code: "{scenario_key}"'

# Zephyr request URLs (More info: https://support.smartbear.com/zephyr-scale-cloud/api-docs/)
FOLDERS_URL = 'https://api.zephyrscale.smartbear.com/v2/' \
              'folders?projectKey={project}&maxResults={max_results}&folderType=TEST_CYCLE'
TEST_EXECUTION_URL = 'https://api.zephyrscale.smartbear.com/v2/testexecutions'
TEST_EXECUTION_ISSUE_URL = 'https://api.zephyrscale.smartbear.com/v2/testexecutions/{key}/links/issues'
TEST_CASE_URL = 'https://api.zephyrscale.smartbear.com/v2/testcases/{key}'
TEST_CYCLE_URL = 'https://api.zephyrscale.smartbear.com/v2/testcycles'
TEST_CASE_SCRIPT_URL = 'https://api.zephyrscale.smartbear.com/v2/testcases/{key}/testscript'
TEST_CASE_STATUS_URL = 'https://api.zephyrscale.smartbear.com/v2/statuses/{status}'
# Zephyr "Automation Status" IDs
AUTOMATED_STATUS_ID = '584918'
NEED_UPDATE_STATUS_ID = '583101'
STATUS_ID_NAME_MAP = {'584918': 'AUTOMATED', '583101': 'NEED UPDATE'}

# BEESQM STATUS
QM_STATUS_ZEPHYR_UPDATE = 'APPROVED'
# Specific for QM
QM_PROJECT = 'BEESQM'
QM_ZONE_FIELD_PATTERN = '[Automated] Zones for testing '
QM_ENV_FIELD_PATTERN = r'\((.*?)\)'

# Test execution status
_STATUS_PASS = 'PASS'
_STATUS_FAIL = 'FAIL'

# Others
DEFAULT_HEADER = {'Content-Type': 'application/json', 'Authorization': None}
TEST_CASE_KEY_PATTERN = r'{project}-\w+'
BUG_KEY_PATTERN = r'^bug.*-(\w+-\w+)$'
HTML_HYPERLINK_PATTERN = '<a href="{url}" rel="noopener noreferrer" target="_blank">{display_text}</a>'
HTML_SUCCESS_MESSAGE_PATTERN = '<span style="color:rgb(65, 168, 95)">{message}</span>'
HTML_FAIL_MESSAGE_PATTERN = '<span style="color:rgb(184, 49, 47)">{message}</span>'
HTML_LINE_BREAK = '<br />'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
TEST_CYCLE_NAME_TIME_FORMAT = '%Y-%m-%dT%H:%M'
MAX_FOLDER_RESULTS = 1000
TEST_EXECUTION_PASS_COMMENT = 'The scenario has completed with no failures.'
TEST_EXECUTION_FAILED_COMMENT = 'The scenario has failed.'
TEST_SCRIPT_EXAMPLES_TABULATION_SIZE = 6

AZURE_PROJECT = 'CI_PROJECT'
AZURE_BUILD_ID = 'CI_BUILD_ID'
AZURE_URL = 'CI_URL'

_QM_SUB_FOLDER_MAP = {
    'regression': 'Regression',
    'expansion': 'Expansion',
    'deploy': 'Deploy',
    'healthcheck': 'Healthcheck',
    'healthcheck-prod': 'Healthcheck PROD',
    'segment': 'Segment',
    'smoke': 'Smoke'
}

_QM_AUTOMATED_TEST_CYCLE_FOLDER_MAP = {
    Environment.SIT: 'SIT-Automated Test Cycles',
    Environment.UAT: 'UAT-Automated Test Cycles',
    Environment.PROD: 'PROD-Automated Test Cycles',
    'sit': 'SIT-Automated Test Cycles',
    'uat': 'UAT-Automated Test Cycles',
    'prod': 'PROD-Automated Test Cycles'
}

_QM_ENVIRONMENT_NAME_MAP = {
    Environment.SIT: '[Master Branch] SIT/QA',
    Environment.UAT: '[Release Branch] UAT',
    Environment.PROD: '[Production branch] Prod',
    'sit': '[Master Branch] SIT/QA',
    'uat': '[Release Branch] UAT',
    'prod': '[Production branch] Prod'
}

_JIRA_VERSION_URL = 'https://ab-inbev.atlassian.net/rest/api/3/project/{project}/version?query={version}'
_JIRA_ACCOUNT_URL = 'https://ab-inbev.atlassian.net/rest/api/latest/user/search?query={email}'
_JIRA_ISSUE_URL = 'https://ab-inbev.atlassian.net/rest/api/2/issue/{key}'

_QM_TEST_CYCLE_TITLE_VERSION_PATTERN = '{major}.{minor}.{micro}'
_TEST_COMPONENT_CYCLE_NAME_PATTERN = 'Core Test - {tag} {version} ' \
                                    '{component} {platform} {zone} {env} {date}'
_TEST_CYCLE_NAME_PATTERN = 'Core test - {tag} - {execution_data} - {date}'
_TEST_CYCLE_URL_PATTERN = 'https://ab-inbev.atlassian.net/projects/' \
                         '{project}?selectedItem=com.atlassian.plugins.atlassian-connect-plugin:' \
                         'com.kanoah.test-manager__main-project-page#!/testCycle/{key}'
_TEST_CYCLE_URL = 'https://api.zephyrscale.smartbear.com/v2/testcycles'

_QM_JIRA_VERSION_PATTERN = 'release-{major}-{minor}-{micro}'

_HTML_LINE_BREAK = '<br />'
_HTML_HYPERLINK_PATTERN = '<a href="{url}" rel="noopener noreferrer" target="_blank">{display_text}</a>'
_HTML_SUCCESS_MESSAGE_PATTERN = '<span style="color:rgb(65, 168, 95)">{message}</span>'
_HTML_FAIL_MESSAGE_PATTERN = '<span style="color:rgb(184, 49, 47)">{message}</span>'

_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
_BUG_KEY_PATTERN = r'^bug.*-(\w+-\w+)$'
_PLATFORM_FIELD = 'customfield_13456'
_ENVIRONMENT_FIELD = 'customfield_13464'
_ZONES_FIELD = 'customfield_13365'
_TEST_EXECUTION_PASS_COMMENT = 'The scenario has completed with no failures.'
_TEST_EXECUTION_FAILED_COMMENT = 'The scenario has failed.'
