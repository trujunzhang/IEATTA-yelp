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

class ParseHelp(object):
    @classmethod
    def save(cls, instance):
        # instance.save()
        return instance


class ParseUserUtils(object):
    @classmethod
    def getCrawlerUser(cls):
        crawler = User.Query.filter(username='crawler').limit(1).get()
        return crawler

    @classmethod
    def signup(cls, user):
        point_user = ParseUserUtils.user_exist(user)
        if not point_user:
            user = User.signup(
                user['displayname'], user['password'],
                email=user['email'], slug=slugify(user['displayname']),
                loginType='email'
            )
            point_user = user

        return point_user

    @classmethod
    def user_exist(cls, user):
        return User.Query.filter(username=user['displayname']).get()


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
class Event(Object):
    pass


class ParseEventUtils(object):
    @classmethod
    def save_event(cls, item):
        _point = ParseEventUtils.event_exist('')
        if not _point:
            instance = Event()

            instance.url = item['url']

            instance.displayname = item['displayname']
            instance.want = item['want']

            instance.start = item['start']
            instance.end = item['end']

            _point = ParseHelp.save(instance)

        return _point

    @classmethod
    def add_restaurant(cls, event, point_restaurant):
        event.add('restaurants', point_restaurant)

        return event

    @classmethod
    def add_user(cls, event, point_user):
        event.add('users', point_user)

        return event

    @classmethod
    def event_exist(cls, href):
        _exist = Event.Query.filter(url=href).get()
        return _exist


# =============================================
#  Web app
# =============================================
class Photo(Object):
    pass


class ParsePhotoUtils(object):
    @classmethod
    def save_photo(cls, url, point_restaurant, point_event=None, point_user=None, point_recipe=None,
                   photo_type='restaurant'):
        _point = ParsePhotoUtils.photo_exist(url)
        if not _point:
            instance = Photo()

            instance.original = ''
            instance.thumbnail = ''
            instance.url = url

            instance.restaurant = point_restaurant
            instance.event = point_event
            instance.user = point_user
            instance.recipe = point_recipe

            instance.photoType = photo_type

            _point = ParseHelp.save(instance)

        return _point

    @classmethod
    def photo_exist(cls, href):
        _point = Photo.Query.filter(url=href).get()
        return _point


# Post is Restaurant
class Post(Object):
    pass


class ParsePostUtils(object):
    @classmethod
    def save_post(cls, item, pointers_photos):
        _point = ParsePostUtils.post_exist(item['url'])
        if not _point:
            _location = item['geoLocation']

            instance = Post()
            instance.url = item['url']

            instance.geoLocation = GeoPoint(_location[0], _location[1])
            instance.address = item['address']

            instance.photos = pointers_photos

            _point = ParseHelp.save(instance)

        return _point

    @classmethod
    def add_event(cls, href, event):
        _point = ParsePostUtils.post_exist(href=href)
        if not _point:
            raise Exception('Not found the restaurant!')

        _point.add('events', event)

        return ParseHelp.save(_point)

    @classmethod
    def post_exist(cls, href):
        return Post.Query.filter(url=href).get()


class Recipe(Object):
    pass


class ParseRecipeUtils(object):
    @classmethod
    def save_recipe(cls, point_restaurant, point_event, point_user, item, photos=None):
        _point = ParseRecipeUtils.recipe_exist(item['url'])
        if not _point:
            instance = Recipe()

            instance.restaurant = point_restaurant
            instance.event = point_event
            instance.user = point_user

            instance.displayname = item['displayname']
            instance.price = item['price']

            instance.photos = photos

            _point = ParseHelp.save(instance)
        return _point

    @classmethod
    def recipe_exist(cls, href):
        return Recipe.Query.filter(url=href).get()


class Comment(Object):
    pass


# =============================================
#  App Notification
# =============================================
class Message(Object):
    pass
