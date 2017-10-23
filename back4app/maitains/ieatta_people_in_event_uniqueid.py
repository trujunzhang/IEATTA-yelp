import json
import logging
import uuid

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, ParseRecordUtil, get_table_list, get_recorded_parse_instance


class IEATTPeopleInEventUUID(object):
    def __init__(self):
        super(IEATTPeopleInEventUUID, self).__init__()

    def append_uid_flag_for_records(self):
        list = get_table_list('peopleInEvent')
        for index, item in enumerate(list):
            _event_pointer = item.event
            _user_pointer = item.user

            _new_unique_id = '{}_{}'.format(_event_pointer.uniqueId, _user_pointer.uniqueId)
            item.uniqueId = _new_unique_id

            item.save()


def main():
    utils = IEATTPeopleInEventUUID()

    utils.append_uid_flag_for_records()


if __name__ == '__main__':
    main()
