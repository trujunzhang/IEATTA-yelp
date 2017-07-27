import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil, \
    ParseReviewUtils, get_object_pointer


class IEATTARelationReviews(object):
    def __init__(self):
        super(IEATTARelationReviews, self).__init__()

        with open('parse_yelp_reviews.json') as data_file:
            self.data = json.load(data_file)

    def __relate_review_for_restaurants(self, review):
        _restaurant_test_id = review['restaurantTestId']

        _pointer_restaurant = get_object_pointer("restaurant", review, "restaurantTestId")
        for r_index, pointer in enumerate(review["pointers"]):
            _pointer_user = get_object_pointer("user", pointer, "userTestId")
            ParseReviewUtils.update_relation(pointer, "restaurant",
                                             _pointer_user,
                                             pointer_restaurant=_pointer_restaurant)

    def import_relation(self):
        # Step01: get recipes from peopleInEvent
        for r_index, review in enumerate(self.data['reviews']):
            type = review["type"]

            if type == "restaurant":
                self.__relate_review_for_restaurants(review)


def main():
    logging.info("  Start relate IEATTA reviews! ")
    utils = IEATTARelationReviews()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_relation()


if __name__ == '__main__':
    main()
