import json

from parse_rest.user import User


class IEATTADemo(object):
    def __init__(self):
        super(IEATTADemo, self).__init__()

        with open('parse_yelp.json') as data_file:
            self.data = json.load(data_file)

    def signup(self):
        pass
        # u = User.signup("dhelmet", "12345", phone="555-555-5555")


def main():
    utils = IEATTADemo()

    utils.signup()


if __name__ == '__main__':
    main()
