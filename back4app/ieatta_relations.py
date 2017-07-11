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

        with open('parse_yelp.json') as data_file:
            self.data = json.load(data_file)

    def ready(self):
        # self.__import_users()
        self.__import_recipes()
        return self

    def __import_users(self):
        _users = self.data['users']
        for index, user in enumerate(_users):
            # if index > 0:
            #     break

            logging.info("     ")
            logging.info("  ** {} ".format('user'))
            logging.info("     {} ".format(index + 1))

            _point_user = ParseUserUtils.signup(user)
            self.pointer_users.append(_point_user)

    def __import_recipes(self):
        _recipes = self.data['recipes']
        for index, recipe in enumerate(_recipes):
            if index > 0:
                break

            logging.info("     ")
            logging.info("  ** {} ".format('recipe'))
            logging.info("     {} ".format(index + 1))

            _point_recipe = ParseRecipeUtils.save_recipe(recipe)
            self.pointer_recipes.append(_point_recipe)

    def import_restaurants(self):
        # if len(self.pointer_users) == 0:
        #     raise AttributeError("Import Users and Recipes firstly.")

        # Step2: restaurants with events
        for index, restaurant in enumerate(self.data['restaurants']):
            if index > 0:
                break


def main():
    logging.info("  Start Import IEATTA class rows! ")
    utils = IEATTARelation()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.ready()

    # utils.import_restaurants()


if __name__ == '__main__':
    main()
