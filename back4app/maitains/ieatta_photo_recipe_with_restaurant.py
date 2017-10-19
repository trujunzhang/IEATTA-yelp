import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, ParseRecordUtil, get_table_list


class IEATTPhotoRecipeWithRestaurant(object):
    def __init__(self):
        super(IEATTPhotoRecipeWithRestaurant, self).__init__()

    def fix_photo_recipe_with_restaurant(self):
        list = get_table_list('photo')
        for photo_instance in list:
            if photo_instance.photoType == 'recipe':
                photo_instance.restaurant = photo_instance.recipe.restaurant
                photo_instance.save()


def main():
    utils = IEATTPhotoRecipeWithRestaurant()

    utils.fix_photo_recipe_with_restaurant()


if __name__ == '__main__':
    main()
