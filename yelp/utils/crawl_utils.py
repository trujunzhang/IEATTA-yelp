import logging
import os

Cache_Folder = 'ieatta'


class CrawlUtils(object):
    def __init__(self):
        super(CrawlUtils, self).__init__()

    @classmethod
    def get_guid(self, _url):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        from hashlib import md5
        # http://www.utf8-chartable.de/unicode-utf8-table.pl?start=128&number=128&utf8=string-literal&unicodeinhtml=hex
        # _url = _url.replace('\xc3\xb3', '')
        # logging.debug("url {} md5.".format(_url))
        _md5 = ''
        try:
            _md5 = md5(_url.encode('utf-8')).hexdigest()
        except Exception as e:
            pass

        return _md5

    @classmethod
    def get_tmp_folder(cls):
        import tempfile, os
        tmp = os.path.join(tempfile.gettempdir(), Cache_Folder)
        if not os.path.exists(tmp):
            os.makedirs(tmp)

        return tmp

    @classmethod
    def get_tmp_file(cls, filename):
        return '{}/{}'.format(CrawlUtils.get_tmp_folder(), filename)

    @classmethod
    def remove_file(cls, path):
        ## delete only if file exists ##
        if os.path.exists(path):
            os.remove(path)
        else:
            logging.debug("Sorry, I can not remove {} file.".format(path))
