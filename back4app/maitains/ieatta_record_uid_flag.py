import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, ParseRecordUtil, get_table_list, get_recorded_parse_instance


class IEATTAUIDFlag(object):
    def __init__(self):
        super(IEATTAUIDFlag, self).__init__()

    def append_uid_flag_for_records(self):
        list = get_table_list('record')
        for index, item in enumerate(list):
            item.flag = "1"
            parse_object = get_recorded_parse_instance(record=item)
            record_uuid = parse_object.uniqueId
            item.recordUniqueId = record_uuid
            item.save()


def main():
    utils = IEATTAUIDFlag()

    utils.append_uid_flag_for_records()


if __name__ == '__main__':
    main()
