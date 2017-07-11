import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event


class RelationData(object):
    point_restaurant = None
    point_event = None
    point_people_in_event = None

    def __init__(self):
        super(RelationData, self).__init__()


class IEATTARelation(object):
    def __init__(self):
        super(IEATTARelation, self).__init__()

        with open('parse_yelp_relations.json') as data_file:
            self.data = json.load(data_file)

    def import_relation(self):
        # Step01: restaurants
        for r_index, restaurant in enumerate(self.data['restaurants']):
            data = RelationData()
            data.point_restaurant = get_object_by_type(Restaurant.Query, restaurant)
            # Step02: Events
            for e_index, event in enumerate(restaurant['events']):
                data.point_event = get_object_by_type(Event.Query, event)
                # Step03: People in the event
                for p_index, people_in_event in enumerate(restaurant['peopleInEvent']):
                    x = 0
                    pass


def main():
    logging.info("  Start Import IEATTA class rows! ")
    utils = IEATTARelation()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_relation()


if __name__ == '__main__':
    main()
