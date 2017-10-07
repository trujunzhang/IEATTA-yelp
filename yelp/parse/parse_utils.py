import logging
import os

# https://github.com/milesrichardson/ParsePy
import uuid

os.environ["PARSE_API_ROOT"] = "https://ieattaps.herokuapp.com/parse"
# os.environ["PARSE_API_ROOT"] = "http://localhost:1337/parse"

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


def get_query(pointer_type):
    _query = None
    if pointer_type == "restaurant":
        _query = Restaurant.Query
    elif pointer_type == "event":
        _query = Event.Query
    elif pointer_type == "user":
        _query = User.Query
    elif pointer_type == "review":
        _query = Review.Query
    elif pointer_type == "recipe":
        _query = Recipe.Query
    elif pointer_type == "photo":
        _query = Photo.Query
    elif pointer_type == "peopleInEvent":
        _query = PeopleInEvent.Query
    elif pointer_type == "record":
        _query = Record.Query

    return _query


def get_object_unique_id_from_photo(photo):
    photo_type = photo.photoType
    _instance = None
    if photo_type == "restaurant":
        _instance = photo.restaurant
    elif photo_type == "recipe":
        _instance = photo.recipe
    elif photo_type == "user":
        _instance = photo.user

    return _instance.uniqueId


def get_recorded_parse_instance(record):
    record_type = record.recordType
    _instance = None
    if record_type == "restaurant":
        _instance = record.restaurant
    elif record_type == "event":
        _instance = record.event
    elif record_type == "user":
        _instance = record.user
    elif record_type == "review":
        _instance = record.review
    elif record_type == "recipe":
        _instance = record.recipe
    elif record_type == "photo":
        _instance = record.photo
    elif record_type == "peopleInEvent":
        _instance = record.peopleInEvent

    return _instance


def get_table_list(pointer_type):
    _list = []
    _query = get_query(pointer_type)
    if _query:
        _list = _query.all()

    return _list


def get_object_pointer(pointer_type, item, field='testId'):
    _query = get_query(pointer_type)
    if _query:
        if _query.filter(testId=item[field]).count() > 0:
            return _query.filter(testId=item[field]).get()


class ParseCloudUtil(object):
    @classmethod
    def get_address_from_location(cls):
        hello_func = Function("getAddressFromLocation")
        # result = hello_func(lat="38.964835", lng="-77.0883076")  # MaryLand
        # result = hello_func(lat="32.399995", lng="120.555723") # local
        result = hello_func(lat="3.889385", lng="102.460485")  # Pulau,Tawar,Pahang,Malaysia
        return hello_func

    @classmethod
    def hello_method(cls):
        hello_func = Function("hello")
        result = hello_func()
        return hello_func

    @classmethod
    def crop_image_on_cloud(self, pointer_photo):
        crop_image_func = Function("cropMultipleSizesImage")
        # crop_image_func = Function("hello")
        result = crop_image_func(imageURL=pointer_photo.url,
                                 photoId=pointer_photo.objectId)
        # pointer_thumbnail = result['result'][0]
        # pointer_original = result['result'][1]
        return result

    @classmethod
    def user_statistic(cls, user_id):
        crop_image_func = Function("statisticUserState")
        result = crop_image_func(userId=user_id)
        pass


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
    def save_relation_between_restaurant_and_event(cls, p_restaurant, p_event):
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
        instance = ParseRecordUtil.record_exist(_record_type, point_instance)
        if not instance:
            instance = Record()
            logging.info("     {} for {} ".format('save @record', _record_type))
        else:
            pass
            # logging.info("     {} for {} ".format('exist @record', _record_type))

        instance.recordType = _record_type
        instance.flag = "1"

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
        elif _record_type == 'review':
            point_record.review = point_instance
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
    def record_exist(cls, _record_type, point_instance):
        _record_query = Record.Query
        _query_filter = _record_query
        if _record_type == 'restaurant':
            _query_filter = _query_filter.filter(restaurant=point_instance)
        elif _record_type == 'photo':
            _query_filter = _query_filter.filter(photo=point_instance)
        elif _record_type == 'event':
            _query_filter = _query_filter.filter(event=point_instance)
        elif _record_type == 'recipe':
            _query_filter = _query_filter.filter(recipe=point_instance)
        elif _record_type == 'user':
            _query_filter = _query_filter.filter(user=point_instance)
        elif _record_type == 'peopleInEvent':
            _query_filter = _query_filter.filter(peopleInEvent=point_instance)
        elif _record_type == 'review':
            _query_filter = _query_filter.filter(review=point_instance)
        else:
            raise Exception('Not found the record type,{}!'.format(_record_type))

        pass
        if _query_filter.count() > 0:
            pass
            return _query_filter.get()


# =============================================
#  App Users
# =============================================

class ParseHelp(object):
    @classmethod
    def save_and_update_record(cls, instance, record_type):

        try:
            _object_uniqueId = instance.uniqueId
        except:
            instance.uniqueId = str(uuid.uuid4())

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
                email=user['email'],
                loginType='email', testId=user['testId'],
                uniqueId=str(uuid.uuid4())
            )
        else:
            point_user = ParseUserUtils.login(user)

        ParseRecordUtil.save_record(point_user, {
            "recordId": point_user.objectId,
            "recordType": 'user'
        })

        return point_user

    @classmethod
    def login(cls, user):
        logged_user = User.login(user['displayName'], user['password'])
        return logged_user

    @classmethod
    def voting_reviews(cls, p_user, voting_dict):
        if p_user:
            p_user.useful = voting_dict['useful']
            p_user.funny = voting_dict['funny']
            p_user.cool = voting_dict['cool']

            ParseHelp.save_and_update_record(p_user, 'user')
        else:
            raise Exception("  *** not found user")

    @classmethod
    def get_user(cls, item, field):
        return get_object_by_type(User.Query, item, field)

    @classmethod
    def get_random_user(cls):
        _temp_user = ['u003', 'u001', 'u002', 'u004', 'u005']

        import random
        index = random.randint(1, 100)
        _item = {'testId': _temp_user[index % 5]}

        return get_object_by_type(User.Query, _item)

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
#  Review
# =============================================
class Review(Object):
    pass


class ParseReviewUtils(object):
    @classmethod
    def save_review(cls, item):
        instance = get_object_by_type(Review.Query, item)
        if not instance:
            instance = Review()

            instance.reviewType = ''
            instance.user = None

            instance.restaurant = None
            instance.event = None
            instance.recipe = None

        instance.testId = item['testId']

        instance.rate = item['rate']
        instance.body = '\n\r'.join(item['body'])

        instance = ParseHelp.save_and_update_record(instance, 'review')

        return instance

    @classmethod
    def get_relation_pointers(cls, restaurant_id=None, event_id=None, user_id=None):
        relation_pointer = {
            "pointer_restaurant": None,
            "pointer_event": None,
            "pointer_user": None
        }
        if restaurant_id:
            relation_pointer["pointer_restaurant"] = Restaurant.Query.filter(objectId=restaurant_id).get()

        if event_id:
            relation_pointer["pointer_event"] = Event.Query.filter(objectId=event_id).get()

        if user_id:
            relation_pointer["pointer_user"] = User.Query.filter(objectId=user_id).get()

        return relation_pointer

    @classmethod
    def update_relation(cls, pointer, review_type,
                        pointer_user=None,
                        pointer_restaurant=None, pointer_event=None, pointer_recipe=None):
        pointer_review = get_object_pointer("review", pointer, "reviewTestId")

        if pointer_review:
            if pointer_review.reviewType == review_type:
                logging.info("  *** exist review, for type: {}".format(review_type))
            else:
                pointer_review.reviewType = review_type
                pointer_review.user = pointer_user

                pointer_review.restaurant = pointer_restaurant
                pointer_review.event = pointer_event
                pointer_review.recipe = pointer_recipe

                pointer_review = ParseHelp.save_and_update_record(pointer_review, 'review')

                logging.info("  *** saved review, for type: {}".format(review_type))
        else:
            raise Exception("  *** not found review,{} for type: {}".format(pointer['reviewTestId'], review_type))


# =============================================
#  Event
# =============================================
class PeopleInEvent(Object):
    pass


class ParsePeopleInEventUtils(object):
    @classmethod
    def save_people_in_event(cls, p_restaurant, p_event, p_user, array_pointer_recipes, item):
        instance = get_object_by_type(PeopleInEvent.Query, item)
        if not instance:
            instance = PeopleInEvent()

        instance.testId = item['testId']

        instance.restaurant = p_restaurant
        instance.event = p_event
        instance.user = p_user
        instance.recipes = array_pointer_recipes

        instance = ParseHelp.save_and_update_record(instance, 'peopleInEvent')

        return instance

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

        instance.testId = item['testId']

        instance.url = item['url']

        instance.displayName = item['displayName']
        instance.want = "\r\n".join(item['want'])

        # Creator
        instance.creator = ParseUserUtils.get_random_user()

        from dateutil import parser
        instance.start = parser.parse(item['start'])
        instance.end = parser.parse(item['end'])

        instance = ParseHelp.save_and_update_record(instance, 'event')

        return instance


# =============================================
#  Web app
# =============================================
class Photo(Object):
    pass


class ParsePhotoUtils(object):
    @classmethod
    def save_photos_for_instance(self, point_instance, item,
                                 record_type,
                                 point_restaurant=None, point_recipe=None, point_user=None):
        '''

        :param point_instance:
        :param item:
        :param record_type: Only three types: 'restaurant', 'recipe', 'user'
        :return:
        '''
        images = item['images']
        _photos_count = 0
        # if point_instance and point_instance.photos:
        #     _photos_count = len(point_instance.photos)

        if _photos_count == len(images):
            logging.info("     {}, length: {} ".format('exist @Array[photos]', _photos_count))
        else:
            # Step1: save all photos for the restaurant
            _pointers_photos = []
            for image_item in images:
                url = None
                user_for_photo_instance = None
                if record_type == 'restaurant':
                    url = image_item["url"]
                    user_for_photo_instance = ParseUserUtils.get_user(image_item, 'userId')
                elif record_type == 'recipe':
                    url = image_item

                    try:
                        user_for_photo_instance = point_instance.user
                    except:
                        pass

                elif record_type == 'user':
                    url = image_item
                    user_for_photo_instance = point_instance

                point_photo = ParsePhotoUtils.save_photo(url=url,
                                                         point_restaurant=point_restaurant,
                                                         point_recipe=point_recipe,
                                                         point_user=user_for_photo_instance,
                                                         photo_type=record_type)
                _pointers_photos.append(point_photo)

            # Step2: update the instance's photo field.
            if len(_pointers_photos) > 0:
                _first_photo = _pointers_photos[0]
                point_instance.listPhoto = _first_photo
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
                   point_user=None,
                   photo_type='restaurant'):
        instance = ParsePhotoUtils.photo_exist(url)
        if not instance:
            instance = Photo()
            instance.original = None
            instance.thumbnail = None
            instance.url = ''
            instance.photoType = ''

        if instance.photoType == photo_type and instance.url == url and instance.original and instance.thumbnail:
            logging.info("     {} for {} ".format('exist @photo', photo_type))
        else:
            instance.url = url

            instance.restaurant = point_restaurant
            instance.recipe = point_recipe
            instance.user = point_user

            instance.photoType = photo_type

            instance = ParseHelp.save_and_update_record(instance, 'photo')
            logging.info("     {} for {} ".format('save @photo', photo_type))

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
            instance.listPhotoUniqueId = None
            instance.address = ''

            logging.info("     {} for {} ".format('save @restaurant', item['testId']))
        else:
            logging.info("     {} for {} ".format('exist @restaurant', item['testId']))

        instance.testId = item['testId']

        instance.displayName = item['displayName']
        instance.url = item['url']

        # Creator
        instance.creator = ParseUserUtils.get_random_user()

        instance.geoLocation = GeoPoint(item['geoLocation'][0], item['geoLocation'][1])

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

            logging.info("     {} for {} ".format('save @recipe', item['testId']))
        else:
            logging.info("     {} for {} ".format('exist @recipe', item['testId']))

        instance.testId = item['testId']

        instance.displayName = item['displayName']
        instance.price = item['price']

        instance = ParseHelp.save_and_update_record(instance, 'recipe')
        return instance

    @classmethod
    def recipe_update_creator(cls, pointer_user, array_pointer_recipes):
        for recipe_instance in array_pointer_recipes:
            recipe_instance.creator = pointer_user

            recipe_instance = ParseHelp.save_and_update_record(recipe_instance, 'recipe')

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
