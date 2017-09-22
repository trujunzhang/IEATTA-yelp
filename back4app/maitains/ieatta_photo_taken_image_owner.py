import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    get_object_unique_id_from_photo, get_table_list


class IEATTPhotoForObjectUniqueId(object):
    def __init__(self):
        super(IEATTPhotoForObjectUniqueId, self).__init__()

    def append_for_who_take_the_photo(self):
        _temp_user = ['u003', 'u001', 'u002', 'u004', 'u005']

        list = get_table_list('photo')

        for index, item in enumerate(list):

            logging.info("     {} for {} ".format('fix @photo', index + 1))

            _photo_type = item.photoType

            if _photo_type == "recipe":
                try:
                    _related_user = item.owner
                except:
                    _item = {'testId': _temp_user[index % 5]}
                    owner_user = ParseUserUtils.get_user(_item, 'testId')
                    item.owner = owner_user
                    item.save()


def main():
    utils = IEATTPhotoForObjectUniqueId()

    utils.append_for_who_take_the_photo()


if __name__ == '__main__':
    main()
