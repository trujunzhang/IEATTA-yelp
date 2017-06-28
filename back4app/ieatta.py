import json

from yelp.parse.parse_utils import ParseUserUtils


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

        if 'events' in restaurant.keys():
            self._events = restaurant['events']

        x = 0

    def save(self):
        pass


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
        for user in self.users:
            ParseUserUtils.signup(user)

        # Step2: restaurants with events
        for restaurant in self.restaurants:
            restaurantImporter = RestaurantImporter(restaurant, self.users, self.recipes)
            # restaurantImporter.save()


def main():
    utils = IEATTADemo()

    utils.signup()


if __name__ == '__main__':
    main()
