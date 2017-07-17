import json

import logging

from yelp.parse.cloudinary_images import CloudinaryImages
from yelp.parse.images_downloader import ImagesDownload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, get_object_by_type, Restaurant, Event, Recipe, ParsePeopleInEventUtils, ParseRelationUtil, \
    ParseFileUploadUtil


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

    def __update_photos_with_images(self, pointer_photo, cloudinary_objects):
        # Step1: Get the local images path.
        thumbnail_path = cloudinary_objects['thumbnail']
        original_path = cloudinary_objects['original']
        # Step2: Upload the local images as parse's files.
        pointer_thumbnail = ParseFileUploadUtil.upload_image_as_file(thumbnail_path, 'thumbnail')
        pointer_original = ParseFileUploadUtil.upload_image_as_file(original_path, 'original')
        # Step3: Update the photo instance with the uploaded image files.
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
