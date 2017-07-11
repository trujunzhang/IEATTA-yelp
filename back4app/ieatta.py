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

        self.point_event = ParseEventUtils.event_exist(event['url'])

        self.point_restaurant = point_restaurant
        self.event = event
        self.users = users
        self.recipes = recipes

    def save_event(self, restaurant_url):
        if not self.point_event:
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

            _importer_recipesUser = OrderedRecipesUserImporter(
                self.point_restaurant,
                self.point_event
            )
            # _importer_recipesUser.get_user(user_in_event)
            # _importer_recipesUser.save_recipes(recipes, ordered_recipes_indexs)
            # _importer_recipesUser.add_recipes_for_ordered_user()


class RestaurantImporter(object):
    def __init__(self, restaurant, users, recipes):
        super(RestaurantImporter, self).__init__()
        # Check whether exist.
        self.point_restaurant = ParseRestaurantUtils.restaurant_exist(restaurant['url'])
        self.photos_count = 0
        if self.point_restaurant and self.point_restaurant.photos:
            self.photos_count = len(self.point_restaurant.photos)

        self.pointers_photos = []

        self.restaurant = restaurant
        self.users = users
        self.recipes = recipes

    def save_photos_for_restaurant(self):
        images = self.restaurant['images']
        if self.photos_count == len(images):
            logging.info("     {} ".format('exist @Array[Photos]'))
        else:
            # Step1: save all photos for the restaurant
            for image in images:
                point_photo = ParsePhotoUtils.save_photo(image, self.point_restaurant)
                self.pointers_photos.append(point_photo)

            # Step2: update the restaurant's photo field.
            ParseRestaurantUtils.add_photos_for_restaurant(self.point_restaurant, self.pointers_photos)
            logging.info("     {} ".format('update @Array[Photos]'))

        return self

    def save_restaurant(self):
        if self.point_restaurant:
            logging.info("     {} ".format('exist @Restaurant'))
        else:
            logging.info("     {} ".format('save @Restaurant'))
            self.point_restaurant = ParseRestaurantUtils.save_restaurant(self.restaurant, [])
        return self

    def save_event(self):
        if 'events' in self.restaurant.keys():
            for event in self.restaurant['events']:
                _importer_event = EventImporter(self.point_restaurant,
                                                event,
                                                self.users,
                                                self.recipes)
                _importer_event.save_event(self.point_restaurant.url)
                # _importer_event.save_users_in_event()

        return self


class IEATTADemo(object):
    def __init__(self):
        super(IEATTADemo, self).__init__()

        self.pointer_users = None
        self.pointer_recipes = None

        with open('parse_yelp.json') as data_file:
            self.data = json.load(data_file)

    def ready(self):
        self.__import_users()
        self.__import_recipes()
        return self

    def __import_users(self):
        self.pointer_users = []
        _users = self.data['users']
        pass

    def __import_recipes(self):
        self.pointer_recipes = []
        _recipes = self.data['recipes']
        pass

    def import_restaurants(self):
        if not self.pointer_users:
            pass

        _restaurants = self.data['restaurants']

        #  Step1: sign up all terms.
        # for user in self.users:
        #     ParseUserUtils.signup(user)

        # Step2: restaurants with events
        for index, restaurant in enumerate(_restaurants):
            if index > 0:
                break

            logging.info("     ")
            logging.info("  ** {} ".format('restaurant'))
            logging.info("     {} ".format(index + 1))

            # _importer_restaurant = RestaurantImporter(restaurant, self.users, self.recipes)
            # _importer_restaurant.save_restaurant()
            # _importer_restaurant.save_photos_for_restaurant()
            # _importer_restaurant.save_event()


def main():
    logging.info("  Start Import IEATTA class rows! ")
    utils = IEATTADemo()

    utils.ready()
    utils.import_restaurants()


if __name__ == '__main__':
    main()
