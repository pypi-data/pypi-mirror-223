from constants import DEFAULT_HEADER, TEST_CYCLE_NAME_TIME_FORMAT, _HTML_LINE_BREAK, _HTML_HYPERLINK_PATTERN, \
    _TIME_FORMAT
from datetime import datetime


def get_headers(authorization):
    """

    Args:
        authorization: str
            Request authorization
    Returns: dict
        Headers
    """
    headers = DEFAULT_HEADER.copy()
    headers['Authorization'] = authorization

    return headers


def get_current_date_test_cycle_name():
    """
    Get the current date
    Returns: str
        current date, e.g: 2022-07-28T11:38
    """
    # Retrieve the date without seconds to compose Zephyr Test Cycle Name
    return datetime.now().strftime(TEST_CYCLE_NAME_TIME_FORMAT)


def parse_description(lines):
    """

    Args:
        lines: tuple
           a html element, e.g: Azure Pipeline: <a href="None" rel="noopener noreferrer" target="_blank">None</a>

    Returns: str
         Returns all line <a> *** </a> with <br /> as a line breaker
    """
    # Removing empty lines and grouping
    return _HTML_LINE_BREAK.join(filter(bool, lines))


def get_hyperlink(url, display_text=None):
    """

    Args:
        url: str
            Url used by the element _HTML_HYPERLINK_PATTERN to inject on href, for example urls: azure_url,
            browserstack_url, report_portal url ...
        display_text: str
            Value that will be displayed through the element returned by _HTML_HYPERLINK_PATTERN below

    Returns: str
        Return the _HTML_HYPERLINK_PATTERN with url and display_text values
    """
    if not display_text:
        display_text = url

    return _HTML_HYPERLINK_PATTERN.format(url=url, display_text=display_text)


def get_current_date():
    """
    Get the current date
    Returns: str
        current date, e.g: 2022-07-28T11:38:59Z
    """
    # Retrieve the date on Zephyr time format
    return datetime.now().strftime(_TIME_FORMAT) + 'Z'

