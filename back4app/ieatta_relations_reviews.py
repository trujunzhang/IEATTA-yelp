import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil


class IEATTARelationReviews(object):
    def __init__(self):
        super(IEATTARelationReviews, self).__init__()

        with open('parse_yelp_reviews.json') as data_file:
            self.data = json.load(data_file)

    def import_relation(self):
        # Step01: get recipes from peopleInEvent
        for p_index, peopleInEvent in enumerate(self.peopleInEvent):
            logging.info("  *** step{} ".format(p_index + 1))
            logging.info("")

            _restaurant_id = peopleInEvent.restaurant.objectId
            _event_id = peopleInEvent.event.objectId
            _user_id = peopleInEvent.user.objectId

            relation_pointers = ParsePeopleInEventUtils.get_relation_pointers(_restaurant_id, _event_id, _user_id)

            for r_index, recipe in enumerate(peopleInEvent.recipes):
                # step02: rebuild the recipe's information.
                ParseRecipeUtils.relate_recipe(recipe.objectId, relation_pointers)


def main():
    logging.info("  Start relate IEATTA reviews! ")
    utils = IEATTARelationReviews()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_relation()


if __name__ == '__main__':
    main()
