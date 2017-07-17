import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil


class RelationData(object):
    point_restaurant = None
    point_event = None
    dict_people_in_event = []

    def __init__(self):
        super(RelationData, self).__init__()


class IEATTAPhotos(object):
    def __init__(self):
        super(IEATTAPhotos, self).__init__()

        self.instance_photos = ParsePhotoUtils.get_photos()
        x = 0

    def upload_photos(self):
        # Step01: restaurants
        for r_index, restaurant in enumerate(self.instance_photos):
            pass


def main():
    logging.info("  Start Upload IEATTA photos! ")
    utils = IEATTAPhotos()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.upload_photos()


if __name__ == '__main__':
    main()
