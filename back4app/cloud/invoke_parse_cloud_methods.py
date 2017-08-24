import json

import logging

import googlemaps
from datetime import datetime

from yelp.parse.parse_utils import ParseCloudUtil, ParseRestaurantUtils


class InvokeParseCloudMethods(object):
    def __init__(self):
        super(InvokeParseCloudMethods, self).__init__()

        with open('../parse_yelp_common.json') as data_file:
            self.common_data = json.load(data_file)
            pass

    def invoke_hello_method(self):
        # ParseCloudUtil.hello_method()
        ParseCloudUtil.get_address_from_location()
        pass

    def save_restaurant_invoke_aftersave(self):
        item = self.common_data['restaurants'][0]
        _point_instance = ParseRestaurantUtils.save_restaurant(item)
        pass

    def save_photo_invoke_aftersave(self):
        item = self.common_data['restaurants'][0]
        image_item = item['images'][0]

        pass

    def invoke_user_statistic(self):
        ParseCloudUtil.user_statistic('6ip0SOxiTG')  # localhost
        # ParseCloudUtil.user_statistic('aGkde8iuL6')  # back4app.com


def main():
    logging.info("  Start invoke parse cloud methods! ")
    utils = InvokeParseCloudMethods()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.invoke_hello_method()
    # utils.save_restaurant_invoke_aftersave()
    # utils.save_photo_invoke_aftersave()
    # utils.invoke_user_statistic()


if __name__ == '__main__':
    main()
