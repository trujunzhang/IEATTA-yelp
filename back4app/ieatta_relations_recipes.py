import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil


class IEATTARelationRecipes(object):
    def __init__(self):
        super(IEATTARelationRecipes, self).__init__()

        with open('parse_yelp_relations.json') as data_file:
            self.peopleInEvent = ParsePeopleInEventUtils.get_people_in_event_list()

    def import_relation(self):
        # Step01: restaurants
        for r_index, peopleInEvent in enumerate(self.peopleInEvent):
            recipes = peopleInEvent
            pass


def main():
    logging.info("  Start relate IEATTA recipes! ")
    utils = IEATTARelationRecipes()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_relation()


if __name__ == '__main__':
    main()
