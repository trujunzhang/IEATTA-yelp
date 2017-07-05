import json

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils


class IEATTARecord(object):
    def __init__(self):
        super(IEATTARecord, self).__init__()

    def list_records(self):
        pass


def main():
    utils = IEATTARecord()

    utils.list_records()


if __name__ == '__main__':
    main()
