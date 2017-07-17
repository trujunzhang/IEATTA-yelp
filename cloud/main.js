Parse.Cloud.define("hello", function (request, response) {
    // Requires two packages to make this happen.
    var _ = require('underscore.js');
    var Image = require("parse-image");

    response.success("Hello world, trujunzhang!");
});

Parse.Cloud.afterSave("Photoxxx", function (request) {

});

Parse.Cloud.define("crop_multiple_sizes_image.js", function (request, response) {
    var url = request.params.imageURL;
    var returnImagesArray = [];

    // Requires two packages to make this happen.
    var _ = require('underscore.js');
    var Image = require("parse-image");

    // Default images sizes.
    var image_card_2x = [540, 350];
    var image_card_3x = [810, 525];
    var image_featured_2x = [750, 550];
    var image_featured_3x = [1080, 825];
    var image_featured = [348, 348];

    // Throwing them all together to iterate through.
    var large_image_size_array = [
        image_card_2x,
        image_card_3x,
        image_featured_2x,
        image_featured_3x
    ];

    Parse.Cloud.httpRequest({
        url: url
    }).then(function (response) {

        var promise = Parse.Promise.as();

        // Each request becomes a promise, execute each promise and then call success.
        _.each(large_image_size_array, function (arrayElement) {
            promise = promise.then(function () {
                // Create an Image from the data.
                var image = new Image();
                return image.setData(response.buffer);
            }).then(function (image) {
                // Using some math, we maintain aspect ratio of the image but scale the width down.
                return image.scale({
                    width: arrayElement[0],
                    height: Math.floor((image.height() * arrayElement[0]) / image.width())
                });
            }).then(function (image) {
                // Convert Image to JPEG
                return image.setFormat("JPEG");
            }).then(function (image) {
                // Get Data of each image.
                return image.data();
            }).then(function (data) {
                // Save the bytes to a new file.
                var file = new Parse.File(venueID + ".jpg", {
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