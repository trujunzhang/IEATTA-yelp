import json

from yelp.parse.parse_utils import ParseUserUtils, ParsePostUtils, ParseEventUtils


class UserImporter(object):
    def __init__(self, restaurant, users, recipes):
        super(UserImporter, self).__init__()

        self.restaurant = restaurant
        self.users = users
        self.recipes = recipes

        x = 0

    def save_user(self):
        self.point_user = ParseUserUtils.save(self.restaurant)
        return self

    def save_recipes(self):
        if not 'events' in self.restaurant.keys():
            return self

        for event in self.restaurant['events']:
            event_importer = EventImporter(event, self.users, self.recipes)
            event_importer.save_event(self.point_restaurant.url).save_users()


class EventImporter(object):
    def __init__(self, event, users, recipes):
        super(EventImporter, self).__init__()

        self.event = event
        self.users = users
        self.recipes = recipes

    def save_event(self, restaurant_url):
        self.point_event = ParseEventUtils.save(self.event)
        point_restaurant = ParsePostUtils.add_event(restaurant_url, self.point_event)

        ParseEventUtils.add_restaurant(self.point_event, point_restaurant)

        return self

    def save_users(self):
        if not 'test' in self.event.keys():
            return

        if not 'Whoin' in self.event['test'].keys():
            return

        _data = self.event['test']['Whoin']
        for user in _data:
            user_importer = UserImporter(restaurant, self.users, self.recipes)
            point_user = ''
            ParseEventUtils.add_user(self.point_event, point_user)


class RestaurantImporter(object):
    def __init__(self, restaurant, users, recipes):
        super(RestaurantImporter, self).__init__()

        self.restaurant = restaurant
        self.users = users
        self.recipes = recipes

        x = 0

    def save_restaurant(self):
        self.point_restaurant = ParsePostUtils.save(self.restaurant)
        return self

    def save_event(self):
        if not 'events' in self.restaurant.keys():
            return self

        for event in self.restaurant['events']:
            event_importer = EventImporter(event, self.users, self.recipes)
            event_importer.save_event(self.point_restaurant.url).save_users()


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
            restaurant_importer = RestaurantImporter(restaurant, self.users, self.recipes)
            restaurant_importer.save_restaurant().save_event()


def main():
    utils = IEATTADemo()

    utils.signup()


if __name__ == '__main__':
    main()
