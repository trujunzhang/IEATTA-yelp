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


class IEATTARelation(object):
    def __init__(self):
        super(IEATTARelation, self).__init__()

        with open('parse_yelp_relations.json') as data_file:
            self.data = json.load(data_file)

    def __get_recipes(self, recipeIds):
        p_recipes = []
        for recipeId in recipeIds:
            p_recipes.append(get_object_by_type(Recipe.Query, {'testId': recipeId}))

        return p_recipes

    def import_relation(self):
        # Step01: restaurants
        for r_index, restaurant in enumerate(self.data['restaurants']):
            data = RelationData()
            data.point_restaurant = get_object_by_type(Restaurant.Query, restaurant)
            # Step02: Events
            for e_index, event in enumerate(restaurant['events']):
                data.point_event = get_object_by_type(Event.Query, event, 'eventTestId')
                # Save the relation(restaurant,event)
                ParseRelationUtil.save_relation_between_restaurant_and_event(data.point_restaurant, data.point_event)

                # Step03: People in the event
                for p_index, people_in_event in enumerate(event['peopleInEvent']):
                    _p_user = ParseUserUtils.get_user(people_in_event['userTestId'])
                    _p_recipes = self.__get_recipes(people_in_event['recipeIds'])
                    # then save it.
                    # ParsePeopleInEventUtils.save_people_in_event(data.point_restaurant, data.point_event,
                    #                                              _p_user, _p_recipes,
                    #                                              people_in_event)
                    # Save the relation(event,user)
                    ParseRelationUtil.save_relation_between_event_and_users(data.point_event, _p_user)


def main():
    logging.info("  Start Import IEATTA class rows! ")
    utils = IEATTARelation()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_relation()


if __name__ == '__main__':
    main()
