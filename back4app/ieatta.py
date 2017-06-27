import json

from parse_rest.user import User


class IEATTADemo(object):
    def __init__(self):
        super(IEATTADemo, self).__init__()

        with open('parse_yelp.json') as data_file:
            self.data = json.load(data_file)

        self.users = self.data['users']

    def signup(self):
        pass
        user = self.users[0]
        u = User.signup(user['displayname'], user['password'], email=user['email'])


def main():
    utils = IEATTADemo()

    utils.signup()


if __name__ == '__main__':
    main()
