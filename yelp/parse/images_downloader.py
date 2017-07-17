import logging
import os

from yelp.utils.crawl_utils import CrawlUtils


class ImagesDownload(object):
    def __init__(self, logs_db=None):
        self.logs_db = logs_db
        self.gif_downloader = None
        super(ImagesDownload, self).__init__()

    @classmethod
    def get_image_location(cls, image_link):
        return CrawlUtils.get_tmp_file(ImagesDownload.get_image_uuid(image_link))

    @classmethod
    def get_image_uuid(cls, image_link):
        return CrawlUtils.get_guid(image_link)

    @classmethod
    def get_image_extension(cls, local_image_path):
        import imghdr
        what_type = imghdr.what(local_image_path)
        if what_type:
            return what_type

        return 'jpeg'

    @classmethod
    def get_image_type(cls, local_image_path):
        return 'image/{}'.format(ImagesDownload.get_image_extension(local_image_path))

    def write_image_cache(self, image_link):

        if image_link:
            logging.debug("  Downloaded image url, {}".format(image_link))
            """
            local_file: 'xxxxx'
            new_file:'xxxxx.jpg'
            """
            local_file = ImagesDownload.get_image_location(image_link)
            if not os.path.exists(local_file):
                self.__download_photo(image_link, local_file)

            if os.path.exists(local_file):
                return self.__adjust_extensition(path=local_file)

    def __adjust_extensition(self, path):
        """
        add extension to the path.
        for example: path: XXXXXX
                     extension: jpg
        new file name: XXXXXX.jpg
        :param path:
        :return:
        """
        file_extension = ImagesDownload.get_image_extension(path)
        new_file = "{}.{}".format(path, file_extension)
        new_file = new_file.replace('png.png', 'jpg')

        from wand.image import Image

        with Image(filename=path) as img:
            img.format = 'jpeg'
            img.save(filename=new_file)

        if os.path.exists(new_file):
            return new_file

    def __download_photo(self, image_link, image_location):
        import urllib.request

        # Download the file from `url` and save it locally under `file_name`:
        with urllib.request.urlopen(image_link) as response, open(image_location, 'wb') as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)

    def remove_tmp_image(self, item):
        relevant_path = CrawlUtils.get_tmp_folder()
        list = os.listdir(relevant_path)
        uuid = ImagesDownload.get_image_uuid(item)
        for file in list:
            if uuid in file:
                path = '{}/{}'.format(relevant_path, file)
                if os.path.exists(path):
                    os.remove(path)

    @classmethod
    def get_new_file_path(cls, path):
        return '{}.jpg'.format(path)
