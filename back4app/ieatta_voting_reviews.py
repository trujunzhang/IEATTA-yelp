import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from yelp.parse.parse_utils import ParseUserUtils, ParseRestaurantUtils, ParseEventUtils, ParseRecipeUtils, \
    ParsePhotoUtils, ParseReviewUtils, get_object_by_type, Review


class IEATTAVotingReviews(object):
    def __init__(self):
        super(IEATTAVotingReviews, self).__init__()

        self.__get_all_users()

        with open('parse_yelp_voting_reviews.json') as data_file:
            self.data = json.load(data_file)

    def __get_all_users(self):
        with open('parse_yelp_common.json') as data_file:
            _data = json.load(data_file)
            self.user_data = _data['users']

    def __get_voted_user(self, test_id):
        _user = None
        for r_index, item in enumerate(self.user_data):
            if item['testId'] == test_id:
                _user = item

        if _user:
            _p_user = ParseUserUtils.login(_user)
            return _p_user

    def __get_voting_reviews(self, review_voter):
        _voting = review_voter['voting']

        voting_dict = {}
        for r_index, review_type in enumerate(_voting.keys()):
            review_ids = _voting[review_type]

            voted_reviews = []
            for v_index, review_id in enumerate(review_ids):
                _p_review = get_object_by_type(Review.Query, {'testId': review_id})
                voted_reviews.append(_p_review)

            voting_dict[review_type] = voted_reviews

        return voting_dict

    def import_all_base_array(self):
        for r_index, review_voter in enumerate(self.data['userVoting']):
            logging.info("  *** step {} ".format(r_index + 1))
            _p_user = self.__get_voted_user(review_voter['userTestId'])

            voting_dict = self.__get_voting_reviews(review_voter)
            ParseUserUtils.voting_reviews(_p_user, voting_dict)
            pass


def main():
    logging.info("  Start voting IEATTA reviews! ")
    utils = IEATTAVotingReviews()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.import_all_base_array()


if __name__ == '__main__':
    main()
