from wand.image import Image
from wand.display import display


class CloudinaryImages(object):
    def __init__(self, original_path):
        self.original_path = original_path
        super(CloudinaryImages, self).__init__()

    def __get_crop_size(self, width, height):
        if width > height:
            return height

        return width

    def get_all_images(self):
        images_schemes = [
            {
                'type': 'thumbnail',
                'width': 348,
                'height': 348
            }
        ]

        thumbnail_path = '{}-thumbnail'.format(self.original_path)

        with Image(filename=self.original_path) as img:
            print('width =', img.width)
            print('height =', img.height)

            c_w_h = self.__get_crop_size(img.width, img.height)

            img.format = 'jpg'
            img.crop(width=c_w_h, height=c_w_h, gravity='center')
            img.resize(width=348, height=348)
            img.save(filename=thumbnail_path)

        return {
            'thumbnail': thumbnail_path,
            'original': self.original_path
        }
