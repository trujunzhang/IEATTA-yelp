import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil, \
    ParseReviewUtils


class IEATTARelationReviews(object):
    def __init__(self):
        super(IEATTARelationReviews, self).__init__()

        with open('parse_yelp_reviews.json') as data_file:
            self.data = json.load(data_file)

    def __relate_review_for_restaurants(self, review):

        pass

    def import_relation(self):
        # Step01: get recipes from peopleInEvent
        for r_index, review in enumerate(self.data['reviews']):
            type = review["type"]

            for r_index, pointer in enumerate(review["pointers"]):

                if type == "restaurant":
                    self.__relate_review_for_restaurants(review)

                ParseReviewUtils.get_relation_pointers(restaurant_id=None, event_id=None, user_id=pointer["userTestId"])


def main():
    logging.info("  Start relate IEATTA reviews! ")
    utils = IEATTARelationReviews()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_relation()


if __name__ == '__main__':
    main()
