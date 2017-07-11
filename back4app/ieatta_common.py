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

    def import_all_base_array(self):
        # if len(self.pointer_users) == 0:
        #     raise AttributeError("Import Users and Recipes firstly.")

        # Step2: restaurants with events
        for index, restaurant in enumerate(self.data['restaurants']):
            if index > 0:
                break

            logging.info("     ")
            logging.info("  ** {} ".format('restaurant'))
            logging.info("     {} ".format(index + 1))


def main():
    logging.info("  Start Import IEATTA class rows! ")
    utils = IEATTACommonImporter()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_all_base_array()


if __name__ == '__main__':
    main()
