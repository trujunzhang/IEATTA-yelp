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
#  App Records
# =============================================
class Record(Object):
    pass


class ParseRecordUtil(object):
    @classmethod
    def save_record(cls, point_instance, item):
        _record_type = item['recordType']
        _point = ParseRecordUtil.record_exist(item['recordId'])
        if not _point:
            instance = Record()

            instance.recordId = item['recordId']
            instance.recordType = _record_type

            instance.save()
            _point = instance

        ParseRecordUtil.__set_related(_point, point_instance, _record_type)
        return _point

    @classmethod
    def __set_related(cls, point_record, point_instance, _record_type):

        if _record_type == 'restaurant':
            point_record.restaurant = point_instance
        elif _record_type == 'photo':
            point_record.photo = point_instance
        elif _record_type == 'event':
            point_record.event = point_instance
        elif _record_type == 'recipe':
            point_record.recipe = point_instance
        elif _record_type == 'user':
            point_record.user = point_instance
        else:
            raise Exception('Not found the record type!')

        point_record.save()

        x = 0

    @classmethod
    def get_list(cls):
        _list = Record.Query.all()
        for item in _list:
            item.flag = 1
            item.save()

        x = 0

    @classmethod
    def record_exist(cls, recordId):
        if Record.Query.filter(recordId=recordId).count() > 0:
            _exist = Record.Query.filter(recordId=recordId).get()
            return _exist


# =============================================
#  App Users
# =============================================

class ParseHelp(object):
    @classmethod
    def save(cls, instance, record_type):
        instance.save()

        ParseRecordUtil.save_record(instance, {
            "recordId": instance.objectId,
            "recordType": record_type
        })
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
                user['displayName'], user['password'],
                email=user['email'], slug=slugify(user['displayName']),
                loginType='email'
            )
            point_user = user

        return point_user

    @classmethod
    def user_exist(cls, user):
        return User.Query.filter(username=user['displayName']).get()


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

            instance.displayName = item['displayName']
            instance.want = item['want']

            instance.start = item['start']
            instance.end = item['end']

            _point = ParseHelp.save(instance, 'event')

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
            _point = instance

        _point = ParseHelp.save(_point, 'photo')
        return _point

    @classmethod
    def photo_exist(cls, href):
        if Photo.Query.filter(url=href).count() > 0:
            return Photo.Query.filter(url=href).get()


class Restaurant(Object):
    pass


class ParseRestaurantUtils(object):
    @classmethod
    def save_restaurant(cls, item, pointers_photos):
        _point = ParseRestaurantUtils.restaurant_exist(item['url'])
        if not _point:
            instance = Restaurant()
            instance.displayName = item['displayName']
            instance.url = item['url']

            instance.geoLocation = GeoPoint(item['geoLocation'][0], item['geoLocation'][1])
            instance.address = item['address']

            instance.photos = pointers_photos
            _point = instance

        _point = ParseHelp.save(_point, 'restaurant')
        return _point

    @classmethod
    def add_photos_for_restaurant(cls, point_restaurant, pointers_photos):
        point_restaurant.photos = pointers_photos

        return ParseHelp.save(point_restaurant, 'restaurant')

    @classmethod
    def add_event(cls, point_restaurant, event):
        point_restaurant.add('events', event)

        return ParseHelp.save(point_restaurant, 'event')

    @classmethod
    def restaurant_exist(cls, href):
        if Restaurant.Query.filter(url=href).count() > 0:
            return Restaurant.Query.filter(url=href).get()


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

            instance.displayName = item['displayName']
            instance.price = item['price']

            instance.photos = photos

            _point = ParseHelp.save(instance, 'recipe')
        return _point

    @classmethod
    def add_photo_for_recipe(cls, point_recipe, pointers_recipes):
        point_recipe.add('recipes', point_recipe)

        return ParseHelp.save(point_recipe, 'recipe')

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
