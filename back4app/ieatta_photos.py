import json

import logging

from yelp.parse.images_downloader import ImagesDownload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil


class RelationData(object):
    point_restaurant = None
    point_event = None
    dict_people_in_event = []

    def __init__(self):
        super(RelationData, self).__init__()


class IEATTAPhotos(object):
    def __init__(self):
        super(IEATTAPhotos, self).__init__()

        self.instance_photos = ParsePhotoUtils.get_photos()

    def upload_photos(self):
        # Step01: photos
        for r_index, photo in enumerate(self.instance_photos):
            _url = photo.url
            _local_path = ImagesDownload().write_image_cache(_url)
            pass


def main():
    logging.info("  Start Upload IEATTA photos! ")
    utils = IEATTAPhotos()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.upload_photos()


if __name__ == '__main__':
    main()
