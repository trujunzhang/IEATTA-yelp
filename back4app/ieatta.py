import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils


class OrderedRecipeImporter(object):
    def __init__(self, point_restaurant, point_event, point_user):
        super(OrderedRecipeImporter, self).__init__()

        self.point_restaurant = point_restaurant
        self.point_event = point_event
        self.point_user = point_user

        self.pointers_photos = []

    def __save_photos_for_ordered_recipe(self, images):
        for image in images:
            point_photo = ParsePhotoUtils.save_photo(
                image,
                self.point_restaurant, self.point_event, self.point_recipe,
                photo_type='recipe')
            self.pointers_photos.append(point_photo)
        return self

    def get_user(self, user_in_event):
        self.point_user = ParseUserUtils.user_exist(user_in_event)
        return self

    def save_recipe(self, ordered_recipe):
        self.point_recipe = ParseRecipeUtils.save_recipe(self.point_restaurant,
                                                         self.point_event,
                                                         self.point_user,
                                                         ordered_recipe,
                                                         self.pointers_photos)
        images = ordered_recipe['test']['images']
        self.__save_photos_for_ordered_recipe(images)
        return self

    def get_point_recipe(self):
        return self.point_recipe


class OrderedRecipesUserImporter(object):
    def __init__(self, point_restaurant, point_event):
        super(OrderedRecipesUserImporter, self).__init__()

        self.point_restaurant = point_restaurant
        self.point_event = point_event

        self.pointers_recipes = []

    def get_user(self, user_in_event):
        self.point_user = ParseUserUtils.user_exist(user_in_event)
        return self

    def save_recipes(self, recipes, ordered_recipes_indexs):
        for ordered_recipe_index in ordered_recipes_indexs:
            position = ordered_recipe_index['position']
            ordered_recipe = recipes[position]
            _point_recipe = OrderedRecipeImporter(
                self.point_restaurant,
                self.point_event,
                self.point_user).save_recipe(ordered_recipe).get_point_recipe()

            self.pointers_recipes.append(_point_recipe)
        return self

    def add_recipes_for_ordered_user(self):
        pass


class EventImporter(object):
    def __init__(self, point_restaurant, event, users, recipes):
        super(EventImporter, self).__init__()

        self.point_restaurant = point_restaurant
        self.event = event
        self.users = users
        self.recipes = recipes

    def save_event(self, restaurant_url):
        self.point_event = ParseEventUtils.save_event(self.event)
        point_restaurant = ParseRestaurantUtils.add_event(restaurant_url, self.point_event)

        ParseEventUtils.add_restaurant(self.point_event, point_restaurant)

        return self

    def save_users_in_event(self):
        if not 'test' in self.event.keys():
            return

        if not 'Whoin' in self.event['test'].keys():
            return

        _data = self.event['test']['Whoin']
        for user_in_event in _data:
            ordered_recipes_indexs = user_in_event['recipes']
            OrderedRecipesUserImporter(
                self.point_restaurant,
                self.point_event
            ).get_user(user_in_event).save_recipes(recipes, ordered_recipes_indexs).add_recipes_for_ordered_user()


class RestaurantImporter(object):
    def __init__(self, restaurant, users, recipes):
        super(RestaurantImporter, self).__init__()

        self.point_restaurant = ParseRestaurantUtils.restaurant_exist(self.restaurant[], self.pointers_photos)

        self.restaurant = restaurant
        self.users = users
        self.recipes = recipes

        self.pointers_photos = []

        x = 0

    def save_photos_for_restaurant(self, images):
        # Step1: save all photos for the restaurant
        for image in images:
            point_photo = ParsePhotoUtils.save_photo(image, self.point_restaurant)
            self.pointers_photos.append(point_photo)

        # Step2: update the restaurant's photo field.
        ParseRestaurantUtils.add_photos_for_restaurant(self.point_restaurant, self.pointers_photos)
        logging.info("     {} ".format('save @Array[Photos]'))
        return self

    def save_restaurant(self):
        logging.info("     {} ".format('save @Restaurant'))
        self.point_restaurant = ParseRestaurantUtils.save_restaurant(self.restaurant, self.pointers_photos)
        return self

    def save_event(self):
        if not 'events' in self.restaurant.keys():
            return self

        for event in self.restaurant['events']:
            EventImporter(self.point_restaurant,
                          event,
                          self.users,
                          self.recipes).save_event(self.point_restaurant.url).save_users_in_event()


class IEATTADemo(object):
    def __init__(self):
        super(IEATTADemo, self).__init__()

        with open('parse_yelp.json') as data_file:
            self.data = json.load(data_file)

        self.users = self.data['users']
        self.restaurants = self.data['restaurants']
        self.recipes = self.data['recipes']

    def import_all(self):
        #  Step1: sign up all terms.
        # for user in self.users:
        #     ParseUserUtils.signup(user)

        # Step2: restaurants with events
        for index, restaurant in enumerate(self.restaurants):
            logging.info("     ")
            logging.info("  ** {} ".format('restaurant'))
            logging.info("     {} ".format(index + 1))

            images = restaurant['images']
            _import = RestaurantImporter(restaurant, self.users, self.recipes)
            _import.save_restaurant()
            # _import.save_photos_for_restaurant(images)
            # _import.save_event()


def main():
    logging.info("  Start Import IEATTA class rows! ")
    utils = IEATTADemo()

    utils.import_all()


if __name__ == '__main__':
    main()
