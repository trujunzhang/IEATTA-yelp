import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, ParseRecordUtil, get_table_list, get_recorded_parse_instance


class IEATTPhotoForObjectUniqueId(object):
    def __init__(self):
        super(IEATTPhotoForObjectUniqueId, self).__init__()

    def append_for_object_uniqueid_for_photos(self):
        list = get_table_list('photo')
        for index, item in enumerate(list):
            parse_object = get_recorded_parse_instance(record=item)
            record_uuid = parse_object.uniqueId
            item.forObjectUniqueId = record_uuid
            item.save()


def main():
    utils = IEATTPhotoForObjectUniqueId()

    utils.append_for_object_uniqueid_for_photos()


if __name__ == '__main__':
    main()
