import json

from yelp.parse.parse_utils import ParseUserUtils, ParsePostUtils, ParseEventUtils, ParseRecipeUtils, ParsePhotoUtils


class UserImporter(object):
    def __init__(self, point_restaurant, point_event):
        super(UserImporter, self).__init__()

        self.point_restaurant = point_restaurant
        self.point_event = point_event

        self.pointers_photos = []

    def save_photos_for_ordered_uses(self, images):
        for image in images:
            point_photo = ParsePhotoUtils.save_photo(image)
            self.pointers_photos.append(point_photo)
        return self

    def get_user(self, user_in_event):
        self.point_user = ParseUserUtils.user_exist(user_in_event)
        return self

    def save_recipes(self, ordered_recipes):
        for ordered_recipe in ordered_recipes:
            self.point_recipe = ParseRecipeUtils.save_recipe(self.point_restaurant,
                                                             self.point_event,
                                                             self.point_user,
                                                             ordered_recipe,
                                                             self.pointers_photos)


class EventImporter(object):
    def __init__(self, point_restaurant, event, users, recipes):
        super(EventImporter, self).__init__()

        self.point_restaurant = point_restaurant
        self.event = event
        self.users = users
        self.recipes = recipes

    def save_event(self, restaurant_url):
        self.point_event = ParseEventUtils.save_event(self.event)
        point_restaurant = ParsePostUtils.add_event(restaurant_url, self.point_event)

        ParseEventUtils.add_restaurant(self.point_event, point_restaurant)

        return self

    def save_users_in_event(self):
        if not 'test' in self.event.keys():
            return

        if not 'Whoin' in self.event['test'].keys():
            return

        _data = self.event['test']['Whoin']
        for user_in_event in _data:
            ordered_recipes = user_in_event['recipes']
            UserImporter(
                self.point_restaurant,
                self.point_event
            ).get_user(user_in_event).save_recipes(ordered_recipes)


class RestaurantImporter(object):
    def __init__(self, restaurant, users, recipes):
        super(RestaurantImporter, self).__init__()

        self.restaurant = restaurant
        self.users = users
        self.recipes = recipes

        self.pointers_photos = []

        x = 0

    def save_photos_for_restaurant(self, images):
        for image in images:
            point_photo = ParsePhotoUtils.save_photo(image)
            self.pointers_photos.append(point_photo)
        return self

    def save_restaurant(self):
        self.point_restaurant = ParsePostUtils.save_post(self.restaurant, self.pointers_photos)
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

    def signup(self):
        #  Step1: sign up all terms.
        # for user in self.users:
        #     ParseUserUtils.signup(user)

        # Step2: restaurants with events
        for restaurant in self.restaurants:
            images = restaurant['images']
            RestaurantImporter(
                restaurant,
                self.users,
                self.recipes).save_photos_for_restaurant(images).save_restaurant().save_event()


def main():
    utils = IEATTADemo()

    utils.signup()


if __name__ == '__main__':
    main()
