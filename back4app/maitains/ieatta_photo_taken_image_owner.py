import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    get_object_unique_id_from_photo, get_table_list


class IEATTPhotoForObjectUniqueId(object):
    def __init__(self):
        super(IEATTPhotoForObjectUniqueId, self).__init__()

    def append_for_object_uniqueid_for_photos(self):
        _temp_user = ['u003', 'u001', 'u002', 'u004', 'u005']
        list = get_table_list('photo')
        for index, item in enumerate(list):
            _item = {'testId': _temp_user[index % 5]}
            _related_user = item.user
            if _related_user:
                _item = {'testId': item.user.testId}
            else:
                pass

            x = 0
            # owner_user = ParseUserUtils.get_user()
            # item.owner = for_object_unique_id
            # item.save()


def main():
    utils = IEATTPhotoForObjectUniqueId()

    utils.append_for_object_uniqueid_for_photos()


if __name__ == '__main__':
    main()
