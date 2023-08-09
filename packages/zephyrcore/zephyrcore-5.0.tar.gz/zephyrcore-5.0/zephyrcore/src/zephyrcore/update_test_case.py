import utils
import json
import requests
from constants import TEST_CASE_URL
from logger import logger


def update_test_case_zone(json_test_case_ids_and_zone, zephyr_token):
    test_case_ids = json_test_case_ids_and_zone['zephyrids']
    test_case_zone = json_test_case_ids_and_zone['zone']

    for test_case_id in test_case_ids:
        zone_is_in_list = False
        response_test_case = utils.get_test_case_by_id(test_case_id, zephyr_token)
        if not response_test_case:
            logger.error('Error getting Test Case!')
            continue
        if response_test_case.status_code != 200:
            logger.error('Test Case not found')
            continue
        test_case_to_update = response_test_case.json()
        logger.info(f'Test Case found! - {test_case_to_update}')

        current_custom_fields = test_case_to_update["customFields"]
        current_zones = current_custom_fields["Zones"]
        for zone in current_zones:
            if zone in test_case_zone:
                zone_is_in_list = True
                break
        if zone_is_in_list:
            logger.info(f'The zone {test_case_zone} is already in test case {test_case_id}!')
            continue
        current_zones.append(test_case_zone)
        current_custom_fields['Zones'] = current_zones

        payload_updated_test_case = {
            'id':  test_case_to_update['id'],
            'key': test_case_to_update['key'],
            'name': test_case_to_update['name'],
            'project': test_case_to_update['project'],
            'priority': test_case_to_update['priority'],
            'status': test_case_to_update['status'],
            'customFields': current_custom_fields
        }

        response_update_test_case = utils.request(requests.put, TEST_CASE_URL.format(
            key=test_case_to_update['key']), zephyr_token, data=json.dumps(payload_updated_test_case))
        logger.info(response_update_test_case)
        logger.info(f'The zone {test_case_zone} was successfully included in test case {test_case_id}!')
