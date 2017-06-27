import json

from parse_rest.user import User

from yelp.parse.parse_utils import ParseUserUtils


class IEATTADemo(object):
    def __init__(self):
        super(IEATTADemo, self).__init__()

        with open('parse_yelp.json') as data_file:
            self.data = json.load(data_file)

        self.users = self.data['users']

    def signup(self):
        user = self.users[0]
        ParseUserUtils.signup(user)


def main():
    utils = IEATTADemo()

    utils.signup()


if __name__ == '__main__':
    main()
