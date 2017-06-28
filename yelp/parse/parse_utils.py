import logging
import os

from yelp.utils.slugify import slugify

os.environ["PARSE_API_ROOT"] = "https://parseapi.back4app.com/"

from parse_rest.user import User
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import register
from parse_rest.datatypes import GeoPoint, Object, Function, Pointer

# register( < application_id >, < rest_api_key > [, master_key = None])

PARSE_REGISTER = {
    "APPLICATION_ID": 'YJ60VCiTAD01YOA3LJtHQlhaLjxiHSsv4mkxKvVM',
    "REST_API_KEY": 'gQTEnIKaDWgZ4UiUZGQqN7qkkvtMCOobQEIb1kYy',
    "MASTER_KEY": '87rxX8J0JwaaPSBxY9DdKJEqWXByqE7sShRsX4vg'
}

register(PARSE_REGISTER["APPLICATION_ID"], PARSE_REGISTER["REST_API_KEY"],
         master_key=PARSE_REGISTER["MASTER_KEY"])


# =============================================
#  App Users
# =============================================


class ParseUserUtils(object):
    @classmethod
    def getCrawlerUser(cls):
        crawler = User.Query.filter(username='crawler').limit(1).get()
        return crawler

    @classmethod
    def signup(cls, user):
        if not ParseUserUtils.user_exist(user):
            user = User.signup(
                user['displayname'], user['password'],
                email=user['email'], slug=slugify(user['displayname']),
                loginType='email'
            )
            return user

    @classmethod
    def user_exist(cls, user):
        count = User.Query.filter(email=user['email']).count()
        return count > 0


# =============================================
#  App Settings
# =============================================
class Setting(Object):
    pass


# =============================================
#  User's profile
# =============================================
class Profile(Object):
    pass


# =============================================
#  Python scrapy
# =============================================
class Cache(Object):
    pass


class ParseCacheUtils(object):
    @classmethod
    def save(cls, item):
        instance = Cache()
        instance.url = item['url']
        instance.sourceFrom = item['url_from']
        instance.thumbnailUrl = item['thumbnail_url']
        # instance.post = ""

        instance.save()

    @classmethod
    def get_last_cache(self, _last, url_from):
        logging.debug("Get the oldest row")
        if _last:
            cache_count = Cache.Query.filter(url=_last).count()
            logging.debug(
                "  1. query the last cache length: {},[{}]".format(_last.encode('utf-8'), cache_count))
            if cache_count:
                Cache.Query.get(url=_last).delete()

            check_exist_count = Cache.Query.filter(url=_last).count()
            logging.debug(
                "  2. after delete the last cache: {},[{}]-[{}]".format(
                    _last.encode('utf-8'), cache_count, check_exist_count))

        item = Cache.Query.all().order_by("createdAt").limit(1).get()

        return {"url": item.url, 'url_from': item.sourceFrom, 'thumbnail_url': item.thumbnailUrl}


# =============================================
#  Web app
# =============================================
class Photo(Object):
    pass


class ParsePhotoUtils(object):
    @classmethod
    def save(cls, url):
        _exist = ParsePhotoUtils.photo_exist(url)
        if not _exist:
            instance = Photo()

            instance.original = ''
            instance.thumbnail = ''
            instance.url = url

            instance.save()
            _exist = instance

        return _exist

    @classmethod
    def photo_exist(cls, href):
        _exist = Photo.Query.filter(url=href).get()
        return _exist


# Post is Restaurant
class Post(Object):
    pass


class ParsePostUtils(object):
    @classmethod
    def save(cls, item, photos):
        _exist = ParsePostUtils.post_exist(item['url'])
        if not _exist:
            _location = item['geoLocation']

            instance = Post()
            instance.url = item['url']

            instance.geoLocation = GeoPoint(_location[0], _location[1])
            instance.address = item['address']

            instance.photos = photos

            instance.save()

            _exist = instance
        return _exist

    @classmethod
    def post_exist(cls, href):
        return Post.Query.filter(url=href).get()


class Comment(Object):
    pass


# =============================================
#  App Notification
# =============================================
class Message(Object):
    pass
