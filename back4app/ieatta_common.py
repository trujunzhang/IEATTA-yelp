import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils


class IEATTACommonImporter(object):
    def __init__(self):
        super(IEATTACommonImporter, self).__init__()

        with open('parse_yelp_common.json') as data_file:
            self.data = json.load(data_file)

    def __import_array(self):
        pass

    def import_all_base_array(self):
        '''
        "events"
        "recipes"
        "restaurants"
        "users"
        :return:
        '''

        type_array = [
            "restaurants",
            # "events", "users", "recipes"
        ]
        for type_key in type_array:
            logging.info("     ")
            logging.info("  ** {} ".format(type_key))

            items = self.data[type_key]
            for index, item in enumerate(items):
                logging.info("     {} ".format(index + 1))
                if type_key == 'events':
                    ParseEventUtils.save_event(item)
                elif type_key == 'recipes':
                    ParseRecipeUtils.save_recipe(item)
                elif type_key == 'restaurants':
                    ParseRestaurantUtils.save_restaurant(item)
                elif type_key == 'users':
                    ParseUserUtils.signup(item)


def main():
    logging.info("  Start Import IEATTA class rows! ")
    utils = IEATTACommonImporter()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_all_base_array()


if __name__ == '__main__':
    main()
