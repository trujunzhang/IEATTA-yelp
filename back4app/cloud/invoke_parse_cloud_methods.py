import json

import logging

import googlemaps
from datetime import datetime


class InvokeParseCloudMethods(object):
    def __init__(self):
        super(InvokeParseCloudMethods, self).__init__()

        self.gmaps = googlemaps.Client(key='AIzaSyBKOlhF3Qw15YJgnCiyyL1wYI3VOXAeTQU')

    def invoke_hello_method(self):
        pass


def main():
    logging.info("  Start invoke parse cloud methods! ")
    utils = InvokeParseCloudMethods()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    utils.invoke_hello_method()


if __name__ == '__main__':
    main()
