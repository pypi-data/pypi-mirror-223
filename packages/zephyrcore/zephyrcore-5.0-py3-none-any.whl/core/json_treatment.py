import requests
import re
from constants import TEST_CASE_URL, TEST_CASE_KEY_PATTERN
import json
import os
from atlassian import Jira
from logger import logger
import utils

_MOBILE_PLATFORMS = ['android', 'ios']
_JIRA_BASE_URL = 'https://ab-inbev.atlassian.net'

# QM specific data
_QM_PROJECT = 'BEESQM'


class JsonTreatment:
    def __init__(self, token, jira_token, confluence_user, confluence_password):
        self._token = token
        self._jira_token = jira_token
        self._confluence_user = confluence_user
        self._confluence_password = confluence_password

        # Variables
        self._project = None
        self._json_data = None
        self.new_json_data = None
        self._testcase = None
        self._test_tag = None
        self._test_tag_zephyr_key = None
        self._platform = None
        self._component_test_case = None
        self._test_tag_zephyr_complete = None
        self._component_test_case_key = None
        self._test_result_list = []

    def get_test_case(self, project, scenario_tags, scenario_name, platform):
        """ Fill in all attributes from this class with the executed scenario info """
        logger.info('Trying to get the test case tag on zephyr')
        for tag in scenario_tags:
            if re.match(TEST_CASE_KEY_PATTERN.format(project=project), tag):
                url = TEST_CASE_URL.format(key=tag)
                test_case = utils.request(method=requests.get, url=url, zephyr_token=self._token).json()
                test_case_platform = test_case['customFields']['Technology'].casefold()

                if test_case_platform == platform:
                    return test_case
                else:
                    return test_case
        else:
            logger.error(f'No valid Zephyr test case key found for the scenario '
                         f'"{scenario_name}" and the platform "{platform}".')
            return None

    def _get_the_test_case_component(self, component_id):
        """
        Get the test case component
        Args:
            component_id: str
                Component id from JIRA/Atlassian
        """
        if self._confluence_user and self._confluence_password:
            logger.info("Getting the Zephyr component of the test case")
            base = Jira(url=_JIRA_BASE_URL, username=self._confluence_user, password=self._confluence_password)
            component_test_case = base.component(component_id=component_id)['name']
            return component_test_case
        else:
            return None

    def load_json_file(self, json_file):
        self._json_data = utils.load_json_file(json_file)
        self.populate_new_json()

    def create_new_json(self):
        if not self._test_result_list != []:
            logger.error('The list of result used to create the json file is empty, check it')
        else:
            logger.info('Creating the Json file with the test execution result')
            with open(f'{os.getcwd()}/zephyr_result.json', 'w', encoding='utf-8') as file:
                # Then we convert the dict for json format and save it in the file
                json.dump(self._test_result_list, file, indent=4)

    def populate_new_json(self):
        if not self._json_data:
            logger.error('Json file has not data or was not received')
        else:
            logger.info('Populate the list with the test results')
            start = 0
            count = len(self._json_data)
            # While to populate the list with all test results
            while start < count:
                self._project = self._json_data[start]['projectKey']
                self._testcase = self._json_data[start]['testCase']
                self._platform = self._json_data[start]['customFields']['platform'].casefold()
                self._test_tag = self._json_data[start]['testTags']
                # Verify if _test_tag is a list and try to search the test tag with a unique json request
                if type(self._test_tag) == list:
                    self._test_tag_zephyr_complete = \
                        self.get_test_case(self._project, self._test_tag, self._testcase, self._platform)
                    if not self._test_tag_zephyr_complete['customFields']['Technology'].casefold() == self._platform:
                        self._test_tag_zephyr_key = self._json_data[start]['testTags'][1]
                    else:
                        self._test_tag_zephyr_key = self._test_tag_zephyr_complete['key']
                # if not _test_tag is a list we have just one test tag and can use it to get the component id
                else:
                    self._test_tag_zephyr_key = self._test_tag
                    self._test_tag_zephyr_complete = \
                        self.get_test_case(self._project, self._test_tag, self._testcase, self._platform)
                self._component_test_case = \
                    self._get_the_test_case_component(self._test_tag_zephyr_complete['component']['id'])
                if not self._component_test_case:
                    logger.error("the Zephyr component of the test case was not found")
                self._component_test_case_key = self._test_tag_zephyr_complete['component']['id']

                self.new_json_data = {
                                        "projectKey": self._project,
                                        "testCase": self._testcase,
                                        "testTag": self._test_tag_zephyr_key,
                                        "testComponent": self._component_test_case,
                                        "testComponentKey": self._component_test_case_key,
                                        "statusName": self._json_data[start]['statusName'],
                                        "environmentName": self._json_data[start]['environmentName'],
                                        "actualEndDate": self._json_data[start]['actualEndDate'],
                                        "executionTime": self._json_data[start]['executionTime'],
                                        "customFields": {
                                            "zone": self._json_data[start]['customFields']['zone'],
                                            "platform": self._json_data[start]['customFields']['platform']
                                        }
                                    }
                self._test_result_list.append(self.new_json_data)
                start = start + 1
            self.create_new_json()
