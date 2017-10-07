import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    get_object_unique_id_from_photo, get_table_list


class IEATTPhotoForObjectUniqueId(object):
    def __init__(self):
        super(IEATTPhotoForObjectUniqueId, self).__init__()

    def __save_photo_owner(self, photo, item):
        owner_user = ParseUserUtils.get_user(item, 'testId')
        photo.owner = owner_user
        photo.save()

    def append_for_who_take_the_photo(self):
        _temp_user = ['u003', 'u001', 'u002', 'u004', 'u005']

        list = get_table_list('photo')

        for index, photo in enumerate(list):
            _photo_type = photo.photoType

            logging.info("     {} for {}, photoType: {} ".format('fix @photo', index + 1, _photo_type))

            _item = None

            if _photo_type == "recipe":
                try:
                    _item = {"testId": photo.recipe.user.testId}
                except:
                    _item = {'testId': _temp_user[index % 5]}
                finally:
                    # self.__save_photo_owner(photo, _item)
                    pass
            elif _photo_type == "restaurant":
                _item = {'testId': _temp_user[index % 5]}
                self.__save_photo_owner(photo, _item)
            elif _photo_type == "user":
                _item = {'testId': photo.user.testId}
                # self.__save_photo_owner(photo, _item)

    def move_from_own_to_creator(self):
        list = get_table_list('review')
        for index, photo in enumerate(list):
            photo.creator = photo.user
            photo.save()


def main():
    utils = IEATTPhotoForObjectUniqueId()

    # utils.append_for_who_take_the_photo()
    utils.move_from_own_to_creator()


if __name__ == '__main__':
    main()
