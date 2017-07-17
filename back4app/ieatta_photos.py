import json

import logging

from yelp.parse.cloudinary_images import CloudinaryImages
from yelp.parse.images_downloader import ImagesDownload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil

from parse_rest.datatypes import Object, File


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

    def __upload_image_as_file(self, local_path, image_type):
        with open(local_path, 'rb') as fh:
            rawdata = fh.read()

        imageFile = File(image_type, rawdata, 'image/png')
        imageFile.save()

        return imageFile

    def __update_photos_with_images(self, pointer_photo, cloudinary_objects):
        thumbnail_path = cloudinary_objects['thumbnail']
        original_path = cloudinary_objects['original']
        pointer_thumbnail = self.__upload_image_as_file(thumbnail_path, 'thumbnail')
        pointer_original = self.__upload_image_as_file(original_path, 'original')
        ParsePhotoUtils.upload_with_uploaded_files(pointer_photo, pointer_thumbnail, pointer_original)

    def upload_photos(self):
        # Step01: photos
        for r_index, photo in enumerate(self.instance_photos):
            _url = photo.url
            _local_path = ImagesDownload().write_image_cache(_url)
            if _local_path:
                cloudinary_objects = CloudinaryImages(_local_path).get_all_images()
                self.__update_photos_with_images(photo, cloudinary_objects)


def main():
    logging.info("  Start Upload IEATTA photos! ")
    utils = IEATTAPhotos()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.upload_photos()


if __name__ == '__main__':
    main()
