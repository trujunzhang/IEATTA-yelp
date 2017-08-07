import json

import logging

import googlemaps
from datetime import datetime


class LocationToAddress(object):
    def __init__(self):
        super(LocationToAddress, self).__init__()

        self.gmaps = googlemaps.Client(key='AIzaSyBKOlhF3Qw15YJgnCiyyL1wYI3VOXAeTQU')

    def to_location(self):
        # Geocoding an address
        geocode_result = self.gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

        pass

    def to_address(self):
        # Look up an address with reverse geocoding
        reverse_geocode_result = self.gmaps.reverse_geocode((40.714224, -73.961452))

        pass


def main():
    logging.info("  Start convert location to address! ")
    utils = LocationToAddress()

    logging.info("     ")
    logging.info("  * {} ".format('Ready'))

    # utils.to_location()
    utils.to_address()


if __name__ == '__main__':
    main()
