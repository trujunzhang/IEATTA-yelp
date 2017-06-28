import json

from yelp.parse.parse_utils import ParseUserUtils, ParsePostUtils


class EventImporter(object):
    def __init__(self, restaurant, users, recipes):
        super(EventImporter, self).__init__()

    def save(self):
        pass


class RestaurantImporter(object):
    def __init__(self, restaurant, users, recipes):
        super(RestaurantImporter, self).__init__()

        self.restaurant = restaurant
        self.users = users
        self.recipes = recipes

        x = 0

    def save_restaurant(self):
        self.restaurant_instance = ParsePostUtils.save(self.restaurant)

        return self

    def save_event(self):
        if not 'events' in self.restaurant.keys():
            return self

        self._events = self.restaurant['events']


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
            restaurantImporter = RestaurantImporter(restaurant, self.users, self.recipes)
            restaurantImporter.save_restaurant().save_event()


def main():
    utils = IEATTADemo()

    utils.signup()


if __name__ == '__main__':
    main()
