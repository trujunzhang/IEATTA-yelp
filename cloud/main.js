Parse.Cloud.define("hello", function (request, response) {
    // Requires two packages to make this happen.
    // const Image = require("parse-image");

    response.success("Hello world, trujunzhang!");
});

Parse.Cloud.afterSave("Restaurant", function (request, response) {
    const restaurant = request.object;

    const restaurantId = restaurant.id;

    new Parse.Query("Restaurant").get(restaurantId)
        .then(function (object) {
            const location = object.get('geoLocation');

            const latitude = location.latitude;
            const longitude = location.longitude;

            if (!!object.get('address')) {
                console.log('(3.4) after query restaurant, @Exist[address]:', object.get('address'));
                response.success(object);
            } else if (!!latitude && !!longitude) {
                Parse.Cloud.run('getAddressFromLocation', {"lat": latitude, 'lng': longitude}, {
                    success: function (result) {

                        object.set('address', result.address);
                        object.set('street_number', result.street_number);
                        object.set('route', result.route);
                        object.set('locality', result.locality);
                        object.set("sublocality", result.sublocality);
                        object.set('country', result.country);
                        object.set('postal_code', result.postal_code);
                        object.set('administrative_area', result.administrative_area);

                        return object.save();
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            }

        })
        .catch(function (error) {
            console.error("(8.)Got an error " + error.code + " : " + error.message);
        });

});

Parse.Cloud.define("getAddressFromLocation", function (request, response) {
    // :param latlng: The latitude/longitude value or place_id for which you wish
    const lat = request.params.lat;
    const lng = request.params.lng;

    const API_KEY = "AIzaSyAyAc4iPiWoC3Qs6u-XnKCV0e4PnFvUXMU"


    // https://developers.google.com/maps/documentation/geocoding/intro#reverse-example
    // https://developers.google.com/maps/documentation/javascript/examples/geocoding-reverse
    // http://maps.googleapis.com/maps/api/geocode/json?latlng=35.1330343,-90.0625056
    Parse.Cloud.httpRequest({
        method: "POST",
        url: 'https://maps.googleapis.com/maps/api/geocode/json',
        params: {
            latlng: lat + "," + lng,
            key: API_KEY
        },
        success: function (httpResponse) {
            let _response = httpResponse.data;
            if (_response.status === "OK") {
                const final = parse_address(_response);
                response.success(final);
            } else {
                response.success("api, failure, " + httpResponse.status);
            }
            // response.success("api, succhttp://maps.googleapis.com/maps/api/geocode/json?latlng=35.1330343,-90.0625056&sensor=trueessfully. lat: " + lat + ", lng: " + lng + ", status: " + _response.status + ", final: " + JSON.stringify(final));
            // response.success("api, successfully. lat: " + lat + ", lng: " + lng + ", status: " + _response.status + ",data: " + country);
        },
        error: function (httpResponse) {
            // console.error('Request failed with response code ' + httpResponse.status);
            response.success("api, failure, " + httpResponse.status);
        }
    });

    // response.success("get Address from Location, lat: " + lat + ", lng: " + lng);
});


function parse_address(response) {
    const results = response.results;

    let final = {// length(7)
        'address': '',
        'street_number': '',
        'route': '',
        'locality': '',
        "sublocality": '',
        'country': '',
        'postal_code': '',
        'administrative_area': ''
    };

    const item = results[0];
    const value = item.formatted_address;
    const component = item.address_components;

    // step1: get the whole address.
    final['address'] = value;

    // step2: get the detailed info.
    component.map((data, index) => {
        const dataTypes = data.types.join(';');

        if (dataTypes.indexOf('street_number') !== -1) {
            final['street_number'] = data.long_name;
        } else if (dataTypes.indexOf('route') !== -1) {
            final['route'] = data.long_name;
        } else if (dataTypes.indexOf('sublocality') !== -1) {
            final['sublocality'] = data.long_name;
        } else if (dataTypes.indexOf('locality') !== -1) {
            final['locality'] = data.long_name;
        } else if (dataTypes.indexOf('country') !== -1) {
            final['country'] = data.short_name;
        } else if (dataTypes.indexOf('postal_code') !== -1) {
            final['postal_code'] = data.short_name;
        } else if (dataTypes.indexOf('administrative_area_level_1') !== -1) {
            final['administrative_area'] = data.short_name;
        }
    });

    return final;
}

Parse.Cloud.afterSave("Photo", function (request, response) {
    const photo = request.object;

    const photoId = photo.id;

    new Parse.Query("Photo").get(photoId)
        .then(function (object) {

            const url = object.get("url");

            if (!!object.get('original')) {
                console.log('(3.4) after query photo, @Exist[original]:', object.get('original'));
                response.success(object);
            } else if (!!url && url !== '') {
                console.log('(3.5)  generating the size images, @New[original]');

                Parse.Cloud.run('cropMultipleSizesImage', {"imageURL": url, "photoId": photoId}, {
                    success: function (result) {
                        console.log('(4.1) callback: crop_multiple_sizes_image', result);
                        console.log(result);

                        console.log('(4.1.1) : List crop sizes Image result');
                        console.log('(4.1.2) : original,', result[0]);
                        console.log('(4.1.3) : thumbnail,', result[1]);

                        object.set("original", result[0]);
                        object.set("thumbnail", result[1]);

                        return object.save();
                    },
                    error: function (error) {
                        console.log('(4.2) callback: crop_multiple_sizes_image', error);
                        console.log(error);
                    }
                });
            }

        })
        .catch(function (error) {
            console.error("(8.)Got an error " + error.code + " : " + error.message);
        });

    console.log('(10.) invoke crop_multiple_sizes_image');
});

Parse.Cloud.define("cropMultipleSizesImage", function (request, response) {
    const url = request.params.imageURL;
    const photoId = request.params.photoId;
    const returnImagesArray = [];

    console.log('(101.1) *** log crop multiple sizes image ***', request.params);
    console.log('(101.2) *** log crop multiple sizes image ***, url: ', url);
    console.log('(101.3) *** log crop multiple sizes image ***, photoId: ', photoId);

    // Requires two packages to make this happen.
    let Image = require("parse-image");

    // Default images sizes.
    let image_featured = [{
        "type": "original"
    }, {
        "type": "thumbnail",
        "width": 348,
        "height": 348
    }];

    // Throwing them all together to iterate through.
    Parse.Cloud.httpRequest({
        url: url
    }).then(function (response) {

        let promise = Parse.Promise.as();

        // Each request becomes a promise, execute each promise and then call success.
        image_featured.forEach(function (arrayElement) {
            promise = promise.then(function () {
                // Create an Image from the data.
                let image = new Image();
                return image.setData(response.buffer);
            }).then(function (image) { // Crop
                // Using some math, we maintain aspect ratio of the image but scale the width down.
                if (arrayElement["type"] === "original") {
                    return image
                }
                const scaleWidth = arrayElement["width"]

                // Crop the image to the smaller of width or height.
                let minSize = Math.min(image.width(), image.height());
                if (minSize === image.width()) {
                    const vertical = (image.height() - image.width()) / 2;
                    return image.crop({
                        left: 0,
                        top: vertical,
                        right: 0,
                        bottom: vertical
                    })
                } else {
                    const horizon = (image.width() - image.height()) / 2;
                    return image.crop({
                        left: horizon,
                        top: 0,
                        right: horizon,
                        bottom: 0
                    })
                }
            }).then(function (image) { // Resize
                // Using some math, we maintain aspect ratio of the image but scale the width down.
                if (arrayElement["type"] === "original") {
                    return image
                }
                const scaleWidth = arrayElement["width"]

                // Crop the image to the smaller of width or height.
                let minSize = Math.min(image.width(), image.height());
                if (minSize === image.width()) {
                    return image.scale({
                        width: scaleWidth,
                        height: scaleWidth * image.height() / image.width()
                    });
                }
                return image.scale({
                    width: scaleWidth * image.width() / image.height(),
                    height: scaleWidth
                });
            }).then(function (image) {
                // Convert Image to JPEG
                return image.setFormat("JPEG");
            }).then(function (image) {
                // Get Data of each image.
                return image.data();
            }).then(function (data) {
                // Save the bytes to a new file.
                let file = new Parse.File(photoId + "-" + arrayElement["type"] + ".jpg", {
                    base64: data.toString("base64")
                });
                return file.save();
            }).then(function (file) {
                // Push the file to the return array.
                returnImagesArray.push(file);
                return file;
            });
        });

        return promise;

    }).then(function () {
            console.log('(102.) *** croped multiple sizes image successfully ***', returnImagesArray);
            response.success(returnImagesArray);
        },
        function (error) {
            response.error(error);
        });
});