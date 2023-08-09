from .core_logger import logger
import time
import requests
from requests.adapters import HTTPAdapter, Retry
from .actions import get_headers
import json
import os
from .constants import (AZURE_URL, AZURE_PROJECT, AZURE_BUILD_ID, _HTML_SUCCESS_MESSAGE_PATTERN,
                        _HTML_FAIL_MESSAGE_PATTERN)


def request(method, url, zephyr_token, headers=None, **kwargs):
    """
    Common request

    Args:
        method: function
           request.get, request.put, ...
        url: str
            Request url
        zephyr_token: str
            zephyr credential
        headers: dict
            Request headers
        **kwargs: *
            Request args
    Returns: response
        Response
    """
    request_per_session = 0
    t0 = time.time()
    s = requests.Session()
    retry_total = 5
    retries = Retry(total=retry_total, backoff_factor=0.3, status_forcelist=[502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    logger.info('Starting the request to get some information in Zephyr')
    try:
        if not headers:
            headers = get_headers(authorization=zephyr_token)
        if 'zephyr' in url:
            request_per_session += 1
        response = method(url=url, headers=headers, **kwargs)
        response.raise_for_status()
        return response
    except Exception as e:
        t1 = time.time()
        logger.error(f'Request Error: {e}')
        logger.error(f'url: {url}\nheaders: {headers}\n **kwargs: {kwargs}\n'
                     f' Took {t1 - t0} seconds\n Retries: {retry_total}')
    return None


def load_json_file(json_file):
    logger.info('Loading the Json file data for a variable')
    with open(json_file, 'r', encoding='utf-8') as file:
        # Then we convert the dict for json format and save it in the file
        json_data = json.load(file)
        return json_data


def get_azure_url():
    """ Retrieves the Azure URL if it is an Azure Pipeline execution.

    Returns
    -------
    str
        Azure execution URL

    """
    url = os.getenv(AZURE_URL)
    project = os.getenv(AZURE_PROJECT)
    build_id = os.getenv(AZURE_BUILD_ID)

    if all((url, project, build_id)):
        return f'{url}/{project}/_build/results?buildId={build_id}&view=results'
    return None


def get_test_case_by_id(test_case_id, zephyr_token):
    """
    Request to get the test case id

    Parameters:
        test_case_id: function
           request.get
        zephyr_token: str
            zephyr credential


    Returns: request
        Request

    """

    url = constants.TEST_CASE_URL.format(key=test_case_id)
    return request(requests.get, url, zephyr_token)


def convert_the_msg_in_html_code_format(success_msg, message):
    """

    Args:
        message: str
            The message that will be displayed on Zephyr
        success_msg: str
            The message that will be displayed on Zephyr
    Returns: str
        The message that will be displayed on Zephyr in html format <a>
    """
    if success_msg:
        html_message_pattern = _HTML_SUCCESS_MESSAGE_PATTERN
    else:
        html_message_pattern = _HTML_FAIL_MESSAGE_PATTERN
    return html_message_pattern.format(message=message)
