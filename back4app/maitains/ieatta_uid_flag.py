import json
import logging

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, ParseRecordUtil, get_table_list


class IEATTAUIDFlag(object):
    def __init__(self):
        super(IEATTAUIDFlag, self).__init__()

    def append_uid_flag(self):
        type_array = [
            # "restaurant",
            # "event",
            # "user",
            "recipe",
            # "review"
        ]

        for type_key in type_array:
            list = get_table_list(type_key)
            pass
        pass


def main():
    utils = IEATTAUIDFlag()

    utils.append_uid_flag()


if __name__ == '__main__':
    main()
