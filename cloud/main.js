Parse.Cloud.define("hello", function (request, response) {
    // Requires two packages to make this happen.
    const Image = require("parse-image");

    response.success("Hello world, trujunzhang!");
});

Parse.Cloud.afterSave("Photo", function (request, response) {
    const photo = request.object;

    const photoId = photo.objectId;
    const url = photo.url;

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

    if (!!url && url !== "") {
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
    }
});

Parse.Cloud.define("crop_multiple_sizes_image", function (request, response) {
    const url = request.params.imageURL;
    const photoId = request.params.photoId;
    const returnImagesArray = [];

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
                var file = new Parse.File(photoId + arrayElement["type"] + ".jpg", {
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
            response.success(returnImagesArray);
        },
        function (error) {
            response.error(error);
        });
});