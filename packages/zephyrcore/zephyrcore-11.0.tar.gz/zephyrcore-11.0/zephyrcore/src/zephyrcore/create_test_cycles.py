from pathlib import PurePosixPath
import requests
import re
from .constants import (FOLDERS_URL, MAX_FOLDER_RESULTS, Environment, _QM_SUB_FOLDER_MAP,
                        _QM_AUTOMATED_TEST_CYCLE_FOLDER_MAP, _JIRA_VERSION_URL,
                        _JIRA_ACCOUNT_URL,
                        _QM_TEST_CYCLE_TITLE_VERSION_PATTERN,
                        _TEST_COMPONENT_CYCLE_NAME_PATTERN,
                        _TEST_CYCLE_NAME_PATTERN, _TEST_CYCLE_URL_PATTERN, _TEST_CYCLE_URL,
                        _QM_JIRA_VERSION_PATTERN,
                        _BUG_KEY_PATTERN, _JIRA_ISSUE_URL, _PLATFORM_FIELD, _ENVIRONMENT_FIELD,
                        _ZONES_FIELD,
                        _ZONE_NAME_MAP, TEST_EXECUTION_ISSUE_URL, _QM_ENVIRONMENT_NAME_MAP,
                        TEST_EXECUTION_URL)
from .actions import get_headers, get_current_date_test_cycle_name, parse_description, \
    get_hyperlink, get_current_date
import json
from .core_logger import logger
from packaging.version import parse
from . import utils

_MOBILE_PLATFORMS = ['android', 'ios']
_JIRA_BASE_URL = 'https://ab-inbev.atlassian.net'

# QM specific data
_QM_PROJECT = 'BEESQM'


class CreateTestCycle:
    def __init__(self, token, jira_token, confluence_user, confluence_password, jira_version,
                 create_zephyr_cycle_per_component, test_suite_type):
        self._token = token
        self._jira_token = jira_token
        self._confluence_user = confluence_user
        self._confluence_password = confluence_password
        self._qm_jira_version = None
        self._jira_user_email = confluence_user
        self._create_zephyr_cycle_per_component = create_zephyr_cycle_per_component
        self._tag = test_suite_type
        self._test_cycle_date = get_current_date_test_cycle_name()
        self._date = get_current_date()
        self._app_version = None
        self._partner = None
        self._test_suite_type = test_suite_type
        self._jira_version = jira_version

        # Headers
        self._headers = get_headers(authorization=self._token)
        self._jira_headers = get_headers(authorization=self._jira_token)

        # Variables
        self._project = None
        self._environment = None
        self._platform = None
        self._json_data = None
        self._zone = None
        self._test_cycle_path = None
        self._test_execution_status = None
        self._component_test_case = None
        self._test_case = None
        self._test_cycle_possible_paths = []
        self._test_case_issues = []
        self._test_cycles_dict = {}
        self._component_list_from_current_test_plan = set()
        self._zephyr_active = True
        self._zephyr_url = None
        self._test_cycle = None
        self._test_cycle_data = None
        self._test_execution = None

    def load_json_file(self, json_file):
        self._json_data = utils.load_json_file(json_file)

    def _manipulate_json(self):
        self._map_of_components = {}
        for data in self._json_data:
            if data['testComponent'] not in self._map_of_components:
                self._map_of_components[data['testComponent']] = []
            self._map_of_components[data['testComponent']].append(data)

    def _parse_qm_jira_version(self):
        """ Fill in the  _qm_jira_version attribute from this class """
        if self._jira_version:
            self._qm_parsed_jira_version = parse(self._jira_version)

            # Versions will always end with micro version 0
            self._qm_jira_version = _QM_JIRA_VERSION_PATTERN.format(major=self._qm_parsed_jira_version.major,
                                                                    minor=self._qm_parsed_jira_version.minor,
                                                                    micro=0)

    def _get_test_cycle_possible_paths(self):
        """ Fill in the  _test_cycle_possible_paths attribute from this class """
        # Priority to the path passed as parameter
        if self._test_cycle_path:
            self._test_cycle_possible_paths.append(PurePosixPath(self._test_cycle_path))

        if self._qm_jira_version:
            # Specific sub folder based on test suite type
            if self._test_suite_type:
                if self._json_data[0]['environmentName'] == Environment.PROD:
                    sub_folder = _QM_SUB_FOLDER_MAP['healthcheck-prod']
                    self._test_cycle_possible_paths.append(PurePosixPath(
                        'BEES Customer' if self._project == 'BEESQM' else self._project, sub_folder))
                else:
                    try:
                        sub_folder = _QM_SUB_FOLDER_MAP[self._test_suite_type]
                        self._test_cycle_possible_paths.append(
                            PurePosixPath('BEES Customer' if self._project == 'BEESQM' else self._project,
                                          self._qm_jira_version,
                                          sub_folder))
                    except KeyError:
                        logger.error(
                            f'Test suite type "{self._test_suite_type}" is not valid. Proceeding with alternative '
                            'Zephyr cycle folder.')

        # Alternative folder in case the release or the test suite type does not exist
        self._test_cycle_possible_paths.append(
            PurePosixPath(_QM_AUTOMATED_TEST_CYCLE_FOLDER_MAP[self._environment])
        )

        if not self._test_cycle_possible_paths:
            error_message = 'Not possible to find any path to create the Zephyr Test Cycle. The parameter ' \
                            '"--zephyr-test-cycle-path" must be provided.'
            logger.error(error_message)

            raise ValueError(error_message)

    def _get_test_cycle_folder(self):
        """ Fill in the  _test_cycle_folder attribute from this class """
        self._get_test_cycle_possible_paths()
        url = FOLDERS_URL.format(project=self._project, max_results=MAX_FOLDER_RESULTS)
        folders = utils.request(method=requests.get, url=url, zephyr_token=self._token).json()['values']
        folder = None

        for test_cycle_possible_path in self._test_cycle_possible_paths:
            parent_id = None  # The previous part of the path is parent of the next one

            for part in test_cycle_possible_path.parts:
                try:
                    folder = list(filter(
                        lambda f: re.match(part, f['name']) and (not parent_id or f['parentId'] == parent_id), folders
                    ))[0]
                except IndexError:
                    logger.error(f'Not possible to find a Zephyr Test Cycle folder that matches the path pattern '
                                 f'"{test_cycle_possible_path}" as the none of the upstream folders match the name '
                                 f'"{part}".')

                    break  # Let's try another possible path
                else:
                    parent_id = folder['id']
            else:
                self._test_cycle_folder = folder

                break  # Test Cycle folder found
        else:
            error_message = 'None of the possible paths to create the Zephyr Test Cycle exist upstream.'
            logger.error(error_message)

            raise ValueError(error_message)

    def _get_jira_project_version(self):
        """ Fill in the  _jira_project_version attribute from this class """
        # If it is a hotfix version, we should set the jira project version as "None", since there is no Jira version
        # created for hotfixes
        if self._qm_parsed_jira_version.micro != 0:
            self._jira_project_version = None
        # For official release versions
        elif self._jira_version:
            # Old app versions will have different project versions (mobile only)
            if self._test_suite_type == 'healthcheck' and self._platform in _MOBILE_PLATFORMS \
                    and self._jira_version != self._app_version:
                self._jira_version = self._app_version
                self._parse_qm_jira_version()

            version = self._qm_jira_version if self._qm_jira_version else self._jira_version
            url = _JIRA_VERSION_URL.format(project=self._project, version=version)

            try:
                self._jira_project_version = utils.request(
                    method=requests.get, url=url, headers=self._jira_headers, zephyr_token=self._token
                ).json()['values'][0]
            except IndexError:
                logger.error(
                    f'Cannot retrieve "version" information from Jira, since version "{self._jira_project_version}" '
                    f'does not exist. Proceeding without this data.')
            except requests.HTTPError:
                logger.error('Cannot retrieve "version" information from Jira. Proceeding without this data.')

    def _get_jira_user_account_id(self):
        """ Fill in the  _jira_user attribute from this class """
        url = _JIRA_ACCOUNT_URL.format(email=self._jira_user_email)

        try:
            self._jira_user = utils.request(
                method=requests.get, url=url, headers=self._jira_headers, zephyr_token=self._token
            ).json()[0]
        except requests.HTTPError:
            logger.error('Cannot retrieve "user" information from Jira, proceeding without this data.')

    def _parse_test_cycle_name(self, component):
        """ Parse test cycle name """
        if self._qm_parsed_jira_version:
            version = _QM_TEST_CYCLE_TITLE_VERSION_PATTERN.format(
                major=self._qm_parsed_jira_version.major,
                minor=self._qm_parsed_jira_version.minor,
                micro=self._qm_parsed_jira_version.micro)
        else:
            version = self._jira_version
        zone = f'{self._partner.upper()}_{self._zone.upper()}' if self._partner \
            else self._zone.upper()
        platform = self._platform.upper()
        environment = self._environment.upper()
        if self._create_zephyr_cycle_per_component:
            self._test_cycle_name = _TEST_COMPONENT_CYCLE_NAME_PATTERN.format(tag=self._tag,
                                                                              env=environment,
                                                                              version=version,
                                                                              component=component,
                                                                              zone=zone,
                                                                              platform=platform,
                                                                              date=self._test_cycle_date)
        else:
            execution_data = (f'{version} - ' if version else '') + f'{zone} {platform} {environment}'
            self._test_cycle_name = _TEST_CYCLE_NAME_PATTERN.format(tag=self._tag,
                                                                    execution_data=execution_data,
                                                                    date=self._test_cycle_date)

    def create_test_cycle(self, json_file):
        """ Create test cycle

        Actions:
            Check if QM project, if true: fill the "_parse_qm_jira_version" attribute, if false: None
            Fill in the _test_cycle_folder attributes in this class -> current method: _get_test_cycle_folder()
            Fill in the _jira_version / _qm_parsed_jira_version  attributes in this class -> \
            current method: _get_jira_project_version()
            Fill in the _jira_user attributes in this class -> current method: _get_jira_user_account_id()
            Fill in the _test_cycle_name attributes in this class -> current method: _parse_test_cycle_name()
            Get azure_url -> get_azure_url()
            Get description -> _parse_description()
            Get test_cycle_data -> Use some attributes from this class
            Fill in the _test_cycle using the response
            Fill in the _session_info.zephyr_url
        """
        # Parsing QM data before starting
        self.load_json_file(json_file)
        self._manipulate_json()
        self._zone = self._json_data[0]['customFields']['zone']
        self._platform = self._json_data[0]['customFields']['platform']
        self._environment = self._json_data[0]['environmentName']
        self._project = self._json_data[0]['projectKey']
        self._parse_qm_jira_version()
        self._get_test_cycle_folder()
        self._get_jira_project_version()
        self._get_jira_user_account_id()
        azure_url = utils.get_azure_url()
        description = parse_description(lines=(
            f'Azure Pipeline: {get_hyperlink(url=azure_url)}' if azure_url else ''
        ))
        for component in self._map_of_components:
            for test in self._map_of_components[component]:
                self._parse_test_cycle_name(component=test['testComponent'])
                self._test_cycle_data = {
                    'projectKey': test['projectKey'],
                    'name': self._test_cycle_name,
                    'description': description,
                    'plannedStartDate': self._date,
                    'plannedEndDate': self._date,
                    'statusName': 'Not executed',
                    'folderId': self._test_cycle_folder['id'],
                    'jiraProjectVersion': self._jira_project_version['id'] if self._jira_project_version else None,
                    'ownerId': self._jira_user['accountId'] if self._jira_user else None
                }
            self._test_cycle = utils.request(method=requests.post,
                                             url=_TEST_CYCLE_URL,
                                             zephyr_token=self._token,
                                             data=json.dumps(self._test_cycle_data)).json()
            self._zephyr_url = _TEST_CYCLE_URL_PATTERN.format(project=self._project,
                                                              key=self._test_cycle['key'])
            self._test_cycles_dict[component] = self._test_cycle
            logger.info('Results will be sent to Zephyr:')
            logger.info(f'\tProject: "{self._project}"')
            logger.info(f'\tTest Cycle Key: "{self._test_cycle["key"]}"')
            logger.info(f'\tTest Cycle Name: "{self._test_cycle_name}"')
            logger.info(f'\tURL: {self._zephyr_url}')
        self._create_test_execution()

    def _get_local_test_case_issues(self, scenario):
        """
        Fill in the class attribute: "_test_case_issues"

        Parameters:
            scenario:
                Pytest BDD scenario
        """
        try:
            for tag in scenario.tags:
                key_match = re.match(_BUG_KEY_PATTERN, tag)

                if key_match:
                    key = key_match.group(1)
                    url = _JIRA_ISSUE_URL.format(key=key)
                    issue = utils.request(method=requests.get,
                                          url=url,
                                          zephyr_token=self._token,
                                          headers=self._jira_headers).json()
                    issue_platform = issue['fields'][_PLATFORM_FIELD]

                    if issue_platform:
                        issue_platform = issue_platform['value'].casefold()

                    issue_environments = issue['fields'][_ENVIRONMENT_FIELD]

                    if issue_environments:
                        issue_environments = list(map(lambda env: env['value'].casefold(), issue_environments))

                    issue_zone_names = issue['fields'][_ZONES_FIELD]

                    if issue_zone_names:
                        issue_zone_names = list(map(lambda zone: zone['value'], issue_zone_names))

                    execution_zone_name = _ZONE_NAME_MAP[self._zone]

                    # Checking if the issue platform and environment match
                    if (not issue_platform or self._platform.casefold() in issue_platform) \
                            and (
                            not issue_environments or self._environment.casefold() in issue_environments) \
                            and (not issue_zone_names or execution_zone_name in issue_zone_names):
                        self._test_case_issues.append(issue)
        except requests.HTTPError:
            logger.error('Cannot retrieve "issues" information from Jira, proceeding without this data.')
        except (KeyError, AttributeError):
            logger.error('Cannot parse "issues" information from Jira, proceeding without this data.')

    def _add_issues_to_test_execution(self):
        """" Add issues to test execution """
        for issue in self._test_case_issues:
            url = TEST_EXECUTION_ISSUE_URL.format(key=self._test_execution['id'])
            issue_data = {
                'issueId': issue['id']
            }
            utils.request(method=requests.post, url=url, zephyr_token=self._token, data=json.dumps(issue_data))

    def _create_test_execution(self):
        """ Actions:
              Get all information related to test execution as: env, jira_user_id, ....
              Make a request (POST) to create the test execution
              Add issues to test execution
           """
        if not self._json_data:
            logger.error('Json file has not data or was not received')
        else:
            logger.info('Populate the list with the test results')
            start = 0
            count = len(self._json_data)
            # While to populate the list with all test results
            while start < count:
                self._project = self._json_data[start]['projectKey']
                self._testcase = self._json_data[start]['testTag']
                self._platform = self._json_data[start]['customFields']['platform']
                self._test_tag = self._json_data[start]['testTag']
                self._test_execution_status = self._json_data[start]['statusName']

                # Test execution time treatment
                hours, minutes, seconds = self._json_data[start]['executionTime'].split(':')
                total_milliseconds = (float(hours) * 3600 + float(minutes) * 60 + float(seconds)) * 1000
                self._test_execution_duration = total_milliseconds

                self._zone = self._json_data[start]['customFields']['zone']
                self._component_test_case = self._json_data[start]['testComponent'] if \
                    self._json_data[start]['testComponentKey'] else None
                self._test_cycle = self._test_cycles_dict[
                    self._component_test_case] if self._create_zephyr_cycle_per_component else \
                    self._test_cycles_dict['common_test_cycle']
                logger.info(f"Creating the test {self._test_tag} in the zephyr cycle {self._test_cycle['key']}...")
                environment = _QM_ENVIRONMENT_NAME_MAP[self._environment]
                jira_user_account_id = self._jira_user['accountId'] if self._jira_user else None
                test_execution_data = {
                    'projectKey': self._project,
                    'testCaseKey': self._test_tag,
                    'testCycleKey': self._test_cycle['key'],
                    'statusName': self._test_execution_status,
                    'environmentName': environment,
                    'actualEndDate': get_current_date(),
                    'executionTime': self._test_execution_duration,
                    'comment': 'Status Pass',
                    'executedById': jira_user_account_id,
                    'assignedToId': jira_user_account_id,
                    'customFields': {
                        'zone': self._zone,
                        'platform': self._platform,
                    }
                }
                start = start + 1
                try:
                    self._test_execution = utils.request(method=requests.post,
                                                         url=TEST_EXECUTION_URL,
                                                         zephyr_token=self._token,
                                                         data=json.dumps(test_execution_data)).json()
                except Exception as e:
                    logger.error('Zephyr error -> Error to the create test cycle on zephyr!'
                                 f'Test Cycle: {self._test_cycle["key"]}\n'
                                 f'Test: {self._test_case}')
                    logger.debug(e)
                self._add_issues_to_test_execution()
