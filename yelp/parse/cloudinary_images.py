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

        return {
            'thumbnail': '',
            'original': ''
        }
