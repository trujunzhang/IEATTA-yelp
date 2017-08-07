import json

import logging


class LocationToAddress(object):
    def __init__(self):
        super(LocationToAddress, self).__init__()

    def to_address(self):
        pass


def main():
    logging.info("  Start convert location to address! ")
    utils = LocationToAddress()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.to_address()


if __name__ == '__main__':
    main()
