$(function () {
    

var Data = Backbone.Model.extend({
        defaults: {
    },
    initialize: function () {
    }
});

var NonPromBroadcastView = Backbone.View.extend({
    el: 'body',
    model: Data,
    

    initialize: function () {
        this.render();
    },

    events: {
        'change input[type=radio]': 'onMessageTimingBtnClicked',
        'click #non-prom-msg': 'onNonPromMsgClicked'

    },

    render: function () {
        console.log('Inside render');
        $('#message-timing-date-time-widget').datetimepicker();
        
        $("#messageTiming-0").attr('checked', true);
        $(".message-timing-date-time-widget-container").addClass('hidden-container');
        
    },

    onMessageTimingBtnClicked: function(ev) {
        console.log('Radio button change event detected');
        
        if ($($(ev.currentTarget)[0]).attr('id') === "messageTiming-1") {
            $(".message-timing-date-time-widget-container").removeClass('hidden-container');    
        } else {
            $(".message-timing-date-time-widget-container").addClass('hidden-container');
        }
    },

    onNonPromMsgClicked: function (ev) {
        console.log('Non Prom button clicked');
        $.get('/admin/non-prom-broadcast/');
    },

    



    

});

var model = new Data();
var view = new NonPromBroadcastView({ model: model });




});