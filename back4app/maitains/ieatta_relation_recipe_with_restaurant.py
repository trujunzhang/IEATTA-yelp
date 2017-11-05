import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, ParseRecordUtil, get_table_list, get_object_by_type, Restaurant


class IEATTPhotoRecipeWithRestaurant(object):
    def __init__(self):
        super(IEATTPhotoRecipeWithRestaurant, self).__init__()

        self.default_restaurant = get_object_by_type(Restaurant.Query, {
            "testId": "s001"
        })

        x = 0

    def fix_photo_recipe_with_restaurant(self):
        list = get_table_list('recipe')
        for recipe_instance in list:
            restaurant_instance = None
            try:
                restaurant_instance = recipe_instance.restaurant
                if restaurant_instance == None:
                    # If recipe's restaurant is empty, give it a default restaurant.
                    recipe_instance.restaurant = self.default_restaurant
                    recipe_instance.save()
            except:
                pass


def main():
    utils = IEATTPhotoRecipeWithRestaurant()

    utils.fix_photo_recipe_with_restaurant()


if __name__ == '__main__':
    main()
