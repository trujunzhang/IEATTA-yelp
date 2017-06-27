import logging
import os

from yelp.utils.slugify import slugify

os.environ["PARSE_API_ROOT"] = "https://parseapi.back4app.com/"

from parse_rest.user import User
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import register

# register( < application_id >, < rest_api_key > [, master_key = None])

PARSE_REGISTER = {
    "APPLICATION_ID": 'YJ60VCiTAD01YOA3LJtHQlhaLjxiHSsv4mkxKvVM',
    "REST_API_KEY": 'gQTEnIKaDWgZ4UiUZGQqN7qkkvtMCOobQEIb1kYy',
    "MASTER_KEY": '87rxX8J0JwaaPSBxY9DdKJEqWXByqE7sShRsX4vg'
}

register(PARSE_REGISTER["APPLICATION_ID"], PARSE_REGISTER["REST_API_KEY"],
         master_key=PARSE_REGISTER["MASTER_KEY"])

from parse_rest.datatypes import Object


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


class History(Object):
    pass


class ParseHistoryUtils(object):
    @classmethod
    def save(cls, item):
        instance = History()
        instance.url = item['url']
        # instance.post = ""

        instance.save()

    @classmethod
    def history_exist(cls, href):
        history_count = History.Query.filter(url=href).count()
        return history_count > 0


# =============================================
#  Web app
# =============================================
class Topic(Object):
    pass


class ParseTopicUtils(object):
    @classmethod
    def save(cls, item):
        instance = Topic()
        instance.name = item['name']
        instance.slug = item['slug']
        instance.status = item['status']
        instance.isIgnore = item['is_ignore']
        instance.active = item['active']
        # instance.days = []

        instance.save()

        return instance

    @classmethod
    def get_topic_by_name(cls, name):
        query_count = Topic.Query.filter(name=name).count()
        if query_count:
            return Topic.Query.filter(name=name).get()


class Post(Object):
    pass


class ParsePostUtils(object):
    @classmethod
    def save(cls, item):
        instance = Post()
        instance.url = item['url']

        instance.author = item['author']
        instance.title = item['title']
        instance.slug = item['slug']
        instance.body = item['body']

        instance.sourceFrom = item['sourceFrom']
        instance.thumbnailUrl = item['thumbnailUrl']

        instance.topics = item['topics']
        instance.postAuthor = item['postAuthor']

        instance.cloudinaryId = item['cloudinaryId'],
        instance.cloudinaryVersion = item['cloudinaryVersion'],
        instance.cloudinaryUrls = item['cloudinaryUrls']

        instance.status = item['status']
        instance.postedAt = item['postedAt']

        instance.save()

    @classmethod
    def post_exist(cls, href):
        history_count = Post.Query.filter(url=href).count()
        return history_count > 0


class Folder(Object):
    pass


class Comment(Object):
    pass


# =============================================
#  App Notification
# =============================================
class Message(Object):
    pass
