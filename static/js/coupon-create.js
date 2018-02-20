$(function () {
    

var Data = Backbone.Model.extend({
        defaults: {
    },
    initialize: function () {
    }
});

var CreateOfferView = Backbone.View.extend({
    el: 'body',
    model: Data,
    

    initialize: function () {
        this.render();
    },

    events: {
        'click #create-offer-preview': 'onOfferPreviewClicked',
        'change #offerImage': 'readURL'

    },

    render: function () {
        console.log('Inside render')
        $('#offer-title-preview-container').html($('#offerTitle').val())
        $('#offer-text-preview-container').html($('#offerText').val())
    },


    onOfferPreviewClicked: function (ev) {
        console.log('Preview button clicked')
        /*
        var selectedImgName = $('#offerImage').val();
        selectedImgName = selectedImgName.replace(/.*[\/\\]/, '');
        imageUrl = "https://s3.amazonaws.com/flobot/coupon-images/" + selectedImgName
        
        $('#top-preview-container').css('background-image', 'url(' + imageUrl + ')');
        */
        $('#top-preview-container').removeClass('hide')
        $('#offer-title-preview-container').html($('#offerTitle').val())
        $('#offer-text-preview-container').html($('#offerText').val())
    },

    readURL: function (event) {
        console.log('inside read url')
        input = event.currentTarget
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                console.log('Showing the reader')
                //$('#blah').attr('src', e.target.result);
                if ($('#top-preview-container').css('background-image') == 'none') {
                    $('#top-preview-container').addClass('hide')
                }
                //$('#top-preview-container').addClass('hide')
                $('#top-preview-container').css('background-image', 'url(' + e.target.result + ')');
            }

            reader.readAsDataURL(input.files[0]);
        }
    }



    

});

var model = new Data();
var view = new CreateOfferView({ model: model });




});