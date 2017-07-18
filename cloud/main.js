Parse.Cloud.define("hello", function (request, response) {
    // Requires two packages to make this happen.
    const Image = require("parse-image");

    response.success("Hello world, trujunzhang!");
});


Parse.Cloud.afterSave("Photo", function (request, response) {
    const photo = request.object;

    const photoId = photo.id;

    console.log('(1.) *** log after saving photo ***', photo);
    console.log('(2.) photoId', photoId);

    new Parse.Query("Photo").get(photoId)
        .then(function (object) {

            const url = object.get("url");

            console.log('(3.1) after query photo, url:', url);
            console.log('(3.2) after query photo, original:', object.get('original'));
            console.log('(3.3) after query photo, thumbnail:', object.get('thumbnail'));

            if (!!object.get('original')) {
                console.log('(3.4) after query photo, @Exist[original]:', object.get('original'));
            }

            // const params = {"imageURL": url, "photoId": photoId};
            Parse.Cloud.run('cropMultipleSizesImage', {"imageURL": url, "photoId": photoId}, {
                success: function (result) {
                    console.log('(4.1) callback: crop_multiple_sizes_image', result);
                    console.log(result);

                    console.log('(4.1.1) : List crop sizes Image result');
                    console.log('(4.1.2) : original,', result[0]);
                    console.log('(4.1.3) : thumbnail,', result[1]);

                    object.set("original", result[0]);
                    object.set("thumbnail", result[1]);
                    object.save();

                    response.success(object)
                },
                error: function (error) {
                    console.log('(4.2) callback: crop_multiple_sizes_image', error);
                    console.log(error);
                }
            });

            console.log('(5.) *** found the photo ***', object);

            response.success(object)
        })
        .catch(function (error) {
            console.error("(8.)Got an error " + error.code + " : " + error.message);
        });


    console.log('(10.) invoke crop_multiple_sizes_image', result);

    response.success();
});

Parse.Cloud.afterSave("Photoyyy", function (request, response) {
    const photo = request.object;

    const photoId = photo.id;
    const url = photo.url;

    console.log('(1.) *** log after saving photo ***', photo);
    console.log('(2.) photoId', photoId);


    // const params = {"imageURL": url, "photoId": photoId};
    Parse.Cloud.run('cropMultipleSizesImage', {"imageURL": url, "photoId": photoId}, {
        success: function (result) {
            console.log(result);
        },
        error: function (error) {
            console.log(error);
        }
    });
    console.log('(3.) invoke crop_multiple_sizes_image', result);

    new Parse.Query("Photo").get(photoId)
        .then(function (object) {

            // object.set("photoType", "trujunzhang-720");
            console.log('(4.) *** found the photo ***', object);
            return object.save();
        })
        .catch(function (error) {
            console.error("(8.)Got an error " + error.code + " : " + error.message);
        });

});


Parse.Cloud.afterSave("Photoxxx", function (request, response) {
    const photo = request.object;

    const photoId = photo.id;
    const url = photo.url;

    console.log('*** log after saving photo ***', photo);
    console.log('photoId', photoId);

    // Requires two packages to make this happen.
    var Image = require("parse-image");

    // Default images sizes.
    var image_featured = [{
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

        var promise = Parse.Promise.as();

        // Each request becomes a promise, execute each promise and then call success.
        image_featured.forEach(function (arrayElement) {
            promise = promise.then(function () {
                // Create an Image from the data.
                var image = new Image();
                return image.setData(response.buffer);
            }).then(function (image) { // Crop
                // Using some math, we maintain aspect ratio of the image but scale the width down.
                if (arrayElement["type"] == "original") {
                    return image
                }
                // Crop the image to the smaller of width or height.
                var minSize = Math.min(image.width(), image.height());
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
                if (arrayElement["type"] == "original") {
                    return image
                }
                const scaleWidth = arrayElement["width"]

                // Crop the image to the smaller of width or height.
                var minSize = Math.min(image.width(), image.height());
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
                var file = new Parse.File(photoId + arrayElement["type"] + ".jpg", {
                    base64: data.toString("base64")
                });
                return file.save();
            }).then(function (file) {
                // Push the file to the return array.
                if (arrayElement["type"] == "original") {
                    photo.original = file
                } else {
                    photo.thumbnail = file
                }
                return file;
            });
        });

        return promise;

    }).then(function () {
            photo.save();
            response.success(photo);
        },
        function (error) {
            response.error(error);
        });
});

Parse.Cloud.define("cropMultipleSizesImage", function (request, response) {
    const url = request.params.imageURL;
    const photoId = request.params.photoId;
    const returnImagesArray = [];

    console.log('(101.1) *** log crop multiple sizes image ***', request.params);
    console.log('(101.2) *** log crop multiple sizes image ***, url: ', url);
    console.log('(101.3) *** log crop multiple sizes image ***, photoId: ', photoId);

    // Requires two packages to make this happen.
    var Image = require("parse-image");

    // Default images sizes.
    var image_featured = [{
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

        var promise = Parse.Promise.as();

        // Each request becomes a promise, execute each promise and then call success.
        image_featured.forEach(function (arrayElement) {
            promise = promise.then(function () {
                // Create an Image from the data.
                var image = new Image();
                return image.setData(response.buffer);
            }).then(function (image) { // Crop
                // Using some math, we maintain aspect ratio of the image but scale the width down.
                if (arrayElement["type"] == "original") {
                    return image
                }
                const scaleWidth = arrayElement["width"]

                // Crop the image to the smaller of width or height.
                var minSize = Math.min(image.width(), image.height());
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
                if (arrayElement["type"] == "original") {
                    return image
                }
                const scaleWidth = arrayElement["width"]

                // Crop the image to the smaller of width or height.
                var minSize = Math.min(image.width(), image.height());
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
                var file = new Parse.File(photoId + "-" + arrayElement["type"] + ".jpg", {
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