import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    get_object_unique_id_from_photo, get_table_list


class IEATTPhotoForObjectUniqueId(object):
    def __init__(self):
        super(IEATTPhotoForObjectUniqueId, self).__init__()

    def append_for_object_uniqueid_for_photos(self):
        list = get_table_list('photo')
        for index, item in enumerate(list):
            for_object_unique_id = get_object_unique_id_from_photo(photo=item)

            item.forObjectUniqueId = for_object_unique_id
            item.save()


def main():
    utils = IEATTPhotoForObjectUniqueId()

    utils.append_for_object_uniqueid_for_photos()


if __name__ == '__main__':
    main()
