import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils


class IEATTARelation(object):
    def __init__(self):
        super(IEATTARelation, self).__init__()

        self.pointer_users = []
        self.pointer_recipes = []

        with open('parse_yelp_relations.json') as data_file:
            self.data = json.load(data_file)

    def import_relation(self):
        for index, restaurant in enumerate(self.data['restaurants']):
            if index > 0:
                break


def main():
    logging.info("  Start Import IEATTA class rows! ")
    utils = IEATTARelation()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_relation()


if __name__ == '__main__':
    main()
