$(function () {
    

var Data = Backbone.Model.extend({
        defaults: {
    },
    initialize: function () {
    }
});

var BroadcastMainOfferView = Backbone.View.extend({
    el: 'body',
    model: Data,
    

    initialize: function () {
        this.render();
    },

    events: {
        'click #non-prom-msg': 'onNonPromMsgClicked'

    },

    render: function () {
        console.log('Inside render')
        //$('#offer-title-preview-container').html($('#offerTitle').val())
        //$('#offer-text-preview-container').html($('#offerText').val())
    },


    onNonPromMsgClicked: function (ev) {
        console.log('Non Prom button clicked')
        $.get('/admin/non-prom-broadcast/');
    },

    



    

});

var model = new Data();
var view = new BroadcastMainOfferView({ model: model });




});