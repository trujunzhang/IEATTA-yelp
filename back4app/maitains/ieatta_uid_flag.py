import json
import logging

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, ParseRecordUtil, get_table_list


class IEATTAUIDFlag(object):
    def __init__(self):
        super(IEATTAUIDFlag, self).__init__()

    def append_uid_flag(self):
        type_array = [
            "event",
            "peopleInEvent",
            "photo",
            "recipe",
            "record",
            "restaurant",
            "review"
        ]

        for type_key in type_array:
            list = get_table_list(type_key)
            for index, item in enumerate(list):
                item.flag = 1
                item.uniqueId = index + 1
                item.save()
        pass


def main():
    utils = IEATTAUIDFlag()

    utils.append_uid_flag()


if __name__ == '__main__':
    main()
