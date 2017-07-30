import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil


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
            logging.info("     ")
            logging.info("     {} ".format(r_index + 1))
            logging.info("     ")

            point_restaurant = get_object_by_type(Restaurant.Query, restaurant)
            # Step02: Events
            for e_index, event in enumerate(restaurant['events']):
                point_event = get_object_by_type(Event.Query, event, 'eventTestId')
                # Save the relation(restaurant,event)
                ParseRelationUtil.save_relation_between_restaurant_and_event(point_restaurant, point_event)
                logging.info("     save relation(Event) between restaurant and event, {} ".format(e_index + 1))
                logging.info("     ")

                # Step03: People in the event
                for p_index, people_in_event in enumerate(event['peopleInEvent']):
                    _p_user = ParseUserUtils.get_user(people_in_event, 'userTestId')
                    # then save it.
                    ParsePeopleInEventUtils.save_people_in_event(point_restaurant, point_event,
                                                                 _p_user, people_in_event)
                    logging.info(
                        "     save relation(PeopleInEvent) between restaurant, event and user, {} ".format(p_index + 1))
                    logging.info("     ")

                    for recipe_index, recipe_test_id in enumerate(people_in_event['recipeIds']):
                        ParseRecipeUtils.relate_recipe(recipe_test_id, point_restaurant, point_event, _p_user)
                        logging.info("     save relation(Recipe), {} ".format(recipe_index + 1))


def main():
    logging.info("  Start relate IEATTA between events and users! ")
    utils = IEATTARelation()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_relation()


if __name__ == '__main__':
    main()
