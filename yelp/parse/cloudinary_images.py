from wand.image import Image
from wand.display import display


class CloudinaryImages(object):
    def __init__(self, original_path):
        self.original_path = original_path
        super(CloudinaryImages, self).__init__()

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

            img.crop(width=348, height=348, gravity='center')
            img.save(filename=thumbnail_path)

        return {
            'thumbnail': thumbnail_path,
            'original': self.original_path
        }
