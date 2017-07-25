import logging
import os

from yelp.utils.slugify import slugify

os.environ["PARSE_API_ROOT"] = "https://parseapi.back4app.com/"

from parse_rest.user import User
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import register
from parse_rest.datatypes import GeoPoint, Object, Function, Pointer, File

# register( < application_id >, < rest_api_key > [, master_key = None])

PARSE_REGISTER = {
    "APPLICATION_ID": 'YJ60VCiTAD01YOA3LJtHQlhaLjxiHSsv4mkxKvVM',
    "REST_API_KEY": 'gQTEnIKaDWgZ4UiUZGQqN7qkkvtMCOobQEIb1kYy',
    "MASTER_KEY": '87rxX8J0JwaaPSBxY9DdKJEqWXByqE7sShRsX4vg'
}

register(PARSE_REGISTER["APPLICATION_ID"], PARSE_REGISTER["REST_API_KEY"],
         master_key=PARSE_REGISTER["MASTER_KEY"])


def get_object_by_type(query, item, field='testId'):
    if query.filter(testId=item[field]).count() > 0:
        return query.filter(testId=item[field]).get()


class ParseCloudUtil(object):
    @classmethod
    def crop_image_on_cloud(self, pointer_photo):
        crop_image_func = Function("cropMultipleSizesImage")
        # crop_image_func = Function("hello")
        result = crop_image_func(imageURL=pointer_photo.url,
                                 photoId=pointer_photo.objectId)
        # pointer_thumbnail = result['result'][0]
        # pointer_original = result['result'][1]
        return result


class ParseFileUploadUtil(object):
    @classmethod
    def upload_image_as_file(self, local_path, image_type):
        with open(local_path, 'rb') as fh:
            rawdata = fh.read()

        imageFile = File(name=image_type, content=rawdata, mimetype='image/jpeg')
        imageFile.save()

        return imageFile


class ParseRelationUtil(object):
    @classmethod
    def update_as_pointer(cls, point_instance, field, value):
        point_instance.add(field, value)
        _point = ParseHelp.save_and_update_record(point_instance, 'event')

    @classmethod
    def save_relation_between_event_and_users(cls, p_event, p_user):
        if not ParseRelationUtil.__check_in_array(p_event.users, p_user):
            p_event.users.append(p_user)
            p_event = ParseHelp.save_and_update_record(p_event, 'event')
            logging.info("  *** {} ".format('saved @relatation[Event|User]'))
        else:
            logging.info("  *** {} ".format('exist @relatation[Event|User]'))

    @classmethod
    def save_relation_between_restaurant_and_event(cls, p_restaurant, p_event):
        if not ParseRelationUtil.__check_in_array(p_restaurant.events, p_event):
            p_restaurant.events.append(p_event)
            p_restaurant = ParseHelp.save_and_update_record(p_restaurant, 'restaurant')
            logging.info("  *** {} ".format('saved @relatation[Restaurant|Event]'))
        else:
            logging.info("  *** {} ".format('exist @relatation[Restaurant|Event]'))

        p_event.restaurant = p_restaurant
        p_event = ParseHelp.save_and_update_record(p_event, 'event')

    @classmethod
    def __check_in_array(cls, array, item):
        for object in array:
            if object.testId == item.testId:
                return True

        return False


# =============================================
#  App Records
# =============================================
class Record(Object):
    pass


class ParseRecordUtil(object):
    @classmethod
    def save_record(cls, point_instance, item):
        _record_type = item['recordType']
        instance = ParseRecordUtil.record_exist(item['recordId'])
        if not instance:
            instance = Record()

        instance.recordId = item['recordId']
        instance.recordType = _record_type

        instance.save()

        ParseRecordUtil.__set_related(instance, point_instance, _record_type)
        return instance

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
        elif _record_type == 'peopleInEvent':
            point_record.peopleInEvent = point_instance
        else:
            raise Exception('Not found the record type,{}!'.format(_record_type))

        point_record.save()

    @classmethod
    def get_list(cls):
        _list = Record.Query.all()
        for item in _list:
            item.flag = 1
            item.save()

    @classmethod
    def record_exist(cls, recordId):
        if Record.Query.filter(recordId=recordId).count() > 0:
            return Record.Query.filter(recordId=recordId).get()


# =============================================
#  App Users
# =============================================

class ParseHelp(object):
    @classmethod
    def save_and_update_record(cls, instance, record_type):
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
        point_user = get_object_by_type(User.Query, user)
        if not point_user:
            point_user = User.signup(
                user['displayName'], user['password'],
                email=user['email'], slug=slugify(user['displayName']),
                loginType='email', testId=user['testId']
            )

        ParseRecordUtil.save_record(point_user, {
            "recordId": point_user.objectId,
            "recordType": 'user'
        })

        return point_user

    @classmethod
    def get_user(cls, testId):
        if User.Query.filter(testId=testId).count() > 0:
            return User.Query.filter(testId=testId).get()

    @classmethod
    def user_exist(cls, user):
        if User.Query.filter(username=user['displayName']).count() > 0:
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
#  Event
# =============================================
class PeopleInEvent(Object):
    pass


class ParsePeopleInEventUtils(object):
    @classmethod
    def save_people_in_event(cls, p_restaurant, p_event, p_user, p_recipes, item):
        instance = ParsePeopleInEventUtils.people_in_event_exist(item['testId'])

        instance.testId = item['testId']

        instance.restaurant = p_restaurant
        instance.event = p_event
        instance.user = p_user
        instance.recipes = p_recipes

        instance = ParseHelp.save_and_update_record(instance, 'peopleInEvent')

        return instance

    @classmethod
    def people_in_event_exist(cls, testId):
        if PeopleInEvent.Query.filter(testId=testId).count() > 0:
            return PeopleInEvent.Query.filter(testId=testId).get()
        return PeopleInEvent()

    @classmethod
    def get_people_in_event_list(cls):
        return PeopleInEvent.Query.all()

    @classmethod
    def get_relation_pointers(cls, restaurant_id, event_id, user_id):
        pointer_restaurant = Restaurant.Query.filter(objectId=restaurant_id).get()
        pointer_event = Event.Query.filter(objectId=event_id).get()
        pointer_user = User.Query.filter(objectId=user_id).get()

        return {
            "pointer_restaurant": pointer_restaurant,
            "pointer_event": pointer_event,
            "pointer_user": pointer_user
        }


class Event(Object):
    pass


class ParseEventUtils(object):
    @classmethod
    def save_event(cls, item):
        instance = get_object_by_type(Event.Query, item)
        if not instance:
            instance = Event()
            instance.restaurant = None
            instance.users = []

        instance.testId = item['testId']

        instance.url = item['url']

        instance.displayName = item['displayName']
        instance.want = item['want']

        instance.start = item['start']
        instance.end = item['end']

        instance = ParseHelp.save_and_update_record(instance, 'event')

        return instance

    @classmethod
    def event_exist(cls, href):
        if Event.Query.filter(url=href).count() > 0:
            return Event.Query.filter(url=href).get()


# =============================================
#  Web app
# =============================================
class Photo(Object):
    pass


class ParsePhotoUtils(object):
    @classmethod
    def save_photos_for_instance(self, point_instance, item,
                                 record_type='restaurant', point_restaurant=None, point_recipe=None):
        '''

        :param point_instance:
        :param item:
        :param record_type: Only two types: 'restaurant' or 'recipe'
        :return:
        '''
        images = item['images']
        _photos_count = 0
        if point_instance and point_instance.photos:
            _photos_count = len(point_instance.photos)

        if _photos_count == len(images):
            logging.info("     {} ".format('exist @Array[photos]'))
        else:
            # Step1: save all photos for the restaurant
            _pointers_photos = []
            for url in images:
                point_photo = ParsePhotoUtils.save_photo(url=url,
                                                         point_restaurant=point_restaurant,
                                                         point_recipe=point_recipe,
                                                         photo_type=record_type)
                _pointers_photos.append(point_photo)

            # Step2: update the instance's photo field.
            point_instance.photos = _pointers_photos
            ParseHelp.save_and_update_record(point_instance, record_type)
            logging.info("     {} for {} ".format('update @Array[photos]', record_type))

        return self

    @classmethod
    def upload_with_uploaded_files(cls, pointer_photo, pointer_thumbnail, pointer_original):
        pointer_photo.original = pointer_original
        pointer_photo.thumbnail = pointer_thumbnail

        instance = ParseHelp.save_and_update_record(pointer_photo, 'photo')
        return instance

    @classmethod
    def save_photo(cls, url,
                   point_restaurant=None, point_recipe=None,
                   photo_type='restaurant'):
        instance = ParsePhotoUtils.photo_exist(url)
        if not instance:
            instance = Photo()
            instance.original = None
            instance.thumbnail = None

        instance.url = url

        instance.restaurant = point_restaurant
        instance.recipe = point_recipe

        instance.photoType = photo_type

        instance = ParseHelp.save_and_update_record(instance, 'photo')
        return instance

    @classmethod
    def photo_exist(cls, href):
        if Photo.Query.filter(url=href).count() > 0:
            return Photo.Query.filter(url=href).get()

    @classmethod
    def get_photos(cls):
        return Photo.Query.all()


class Restaurant(Object):
    pass


class ParseRestaurantUtils(object):
    @classmethod
    def save_restaurant(cls, item):
        instance = get_object_by_type(Restaurant.Query, item)
        if not instance:
            instance = Restaurant()
            instance.events = []
            instance.photos = []

        instance.testId = item['testId']

        instance.displayName = item['displayName']
        instance.url = item['url']

        instance.geoLocation = GeoPoint(item['geoLocation'][0], item['geoLocation'][1])
        instance.address = item['address']

        instance = ParseHelp.save_and_update_record(instance, 'restaurant')
        return instance

    @classmethod
    def restaurant_exist(cls, href):
        if Restaurant.Query.filter(url=href).count() > 0:
            return Restaurant.Query.filter(url=href).get()


class Recipe(Object):
    pass


class ParseRecipeUtils(object):
    @classmethod
    def save_recipe(cls, item):
        instance = get_object_by_type(Recipe.Query, item)
        if not instance:
            instance = Recipe()
            instance.restaurant = None
            instance.event = None
            instance.user = None
            instance.photos = []

        instance.testId = item['testId']

        instance.displayName = item['displayName']
        instance.price = item['price']

        instance = ParseHelp.save_and_update_record(instance, 'recipe')
        return instance

    @classmethod
    def relate_recipe(cls, recipe_id, relation_pointers):
        pointer_recipe = Recipe.Query.filter(objectId=recipe_id).get()

        pointer_restaurant = relation_pointers['pointer_restaurant']
        pointer_event = relation_pointers['pointer_event']
        pointer_user = relation_pointers['pointer_user']

        if pointer_recipe and pointer_restaurant and pointer_event and pointer_user:
            if pointer_recipe.restaurant and pointer_recipe.event and pointer_recipe.user:
                logging.info("  *** {}, {}".format('exist @relatation[Recipe|Relations]', pointer_recipe.objectId))
            else:
                pointer_recipe.restaurant = pointer_restaurant
                pointer_recipe.event = pointer_event
                pointer_recipe.user = pointer_user

                ParseHelp.save_and_update_record(pointer_recipe, 'recipe')
                logging.info("  *** {}, {}".format('saved @relatation[Recipe|Relations]', pointer_recipe.objectId))
        else:
            raise Exception('Not found the instance on the peopleInEvent!')

    @classmethod
    def recipe_exist(cls, href):
        if Recipe.Query.filter(url=href).count() > 0:
            return Recipe.Query.filter(url=href).get()


class Comment(Object):
    pass


# =============================================
#  App Notification
# =============================================
class Message(Object):
    pass
