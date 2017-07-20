import json

import logging

from yelp.parse.cloudinary_images import CloudinaryImages
from yelp.parse.images_downloader import ImagesDownload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParsePhotoUtils, ParseFileUploadUtil, ParseCloudUtil


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

    def __update_photos_with_local_images(self, pointer_photo, cloudinary_objects):
        # Step1: Get the local images path.
        thumbnail_path = cloudinary_objects['thumbnail']
        original_path = cloudinary_objects['original']
        # Step2: Upload the local images as parse's files.
        pointer_thumbnail = ParseFileUploadUtil.upload_image_as_file(thumbnail_path, 'thumbnail')
        pointer_original = ParseFileUploadUtil.upload_image_as_file(original_path, 'original')
        # Step3: Update the photo instance with the uploaded image files.
        ParsePhotoUtils.upload_with_uploaded_files(pointer_photo, pointer_thumbnail, pointer_original)

    def upload_photos_from_local(self):
        """
        Pending, not used now
        :return:
        """
        # Step01: photos
        for r_index, photo in enumerate(self.instance_photos):
            _url = photo.url
            _local_path = ImagesDownload().write_image_cache(_url)
            if _local_path:
                cloudinary_objects = CloudinaryImages(_local_path).get_all_images()
                self.__update_photos_with_local_images(photo, cloudinary_objects)

    def invoke_cloud_images(self):
        """
        Pending, not used now
        :return:
        """
        for r_index, photo in enumerate(self.instance_photos):
            result = ParseCloudUtil.crop_image_on_cloud(photo)
            # Step3: Update the photo instance with the uploaded image files.
            pointer_thumbnail = result['result'][0]
            pointer_original = result['result'][1]
            ParsePhotoUtils.upload_with_uploaded_files(photo, pointer_thumbnail, pointer_original)

    def save_photos_again(self):
        for r_index, photo in enumerate(self.instance_photos):
            photo.save()
            logging.info("     {} ".format('saved @[photo] again!'))
            x = 0


def main():
    logging.info("  Start Upload IEATTA photos! ")
    utils = IEATTAPhotos()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.save_photos_again()


if __name__ == '__main__':
    main()
