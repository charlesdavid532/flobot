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
    

    initialize: function initialize() {
        this.quickReplyViewList = [];
        this.render();
    },

    events: {
        'change input[type=radio]': 'onMessageTimingBtnClicked',
        'click #non-prom-msg': 'onNonPromMsgClicked'

    },

    render: function render() {
        console.log('Inside render');
        $('#messageTimingDateTimeWidget').datetimepicker();
        
        $("#messageTiming-0").attr('checked', true);
        $(".message-timing-date-time-widget-container").addClass('hidden-container');

        this.sideBarModel = new SideBarData();
        this.sideBarView = new SideBarView({ model: this.sideBarModel });
        this.listenTo(this.sideBarView, 'TEXT_SIDEBAR_CLICKED', this.onTextClicked);
        this.listenTo(this.sideBarView, 'MEDIA_SIDEBAR_CLICKED', this.onMediaClicked);
        this.listenTo(this.sideBarView, 'CARD_SIDEBAR_CLICKED', this.onCardClicked);
        this.listenTo(this.sideBarView, 'BUTTON_SIDEBAR_CLICKED', this.onButtonClicked);
        this.listenTo(this.sideBarView, 'QUICK_REPLY_SIDEBAR_CLICKED', this.onQuickReplyClicked);
        
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

    onTextClicked: function (ev) {
        console.log('Text button event detected in main view');
        
    },

    onMediaClicked: function (ev) {
        console.log('Media button event detected in main view');
        
    },

    onCardClicked: function (ev) {
        console.log('Card button event detected in main view');
        
    },

    onButtonClicked: function (ev) {
        console.log('Button event detected in main view');
        
    },

    onQuickReplyClicked: function onQuickReplyClicked(ev) {
        console.log('Quick Reply event detected in main view');
        if (this.quickReplyViewList.length < 3) {
            this.generateNewQuickReply();
        }
    },

    generateNewQuickReply: function generateNewQuickReply() {
        var qrModel = new QuickReplyData();
        qrModelId = this.generateRandomNum(1000,10000);
        qrModel.setNumId(qrModelId);

        this.injectQuickReplyHtml(qrModelId);

        var qrView = new QuickReplyView({ model: qrModel, el: '#' + qrModelId.toString() });

        this.listenTo(qrView, 'QUICK_REPLY_CLOSE_BTN_CLICKED', this.onQRCloseBtnClicked);
        this.quickReplyViewList.push(qrView);

    },

    generateRandomNum: function generateRandomNum (x, y) {
        return Math.floor(x + (y - x) * Math.random());
    },

    injectQuickReplyHtml: function injectQuickReplyHtml(qrId) {
        this.$el.find('.broadcast-builder-bottom-container').append(this.createQuickReplyHtml(qrId));
        var self = this,
            quickReplyContainer = this.$el.find('#' + qrId);

        quickReplyContainer.find('.quick-reply-close-button').on("click","", qrId, function(ev) {
            self.onQRCloseBtnClicked(ev.data);
        });
    },

    createQuickReplyHtml: function createQuickReplyHtml(qrId) {
        return "<div id='" + qrId + "' class='qr-elem'><div class='qr-text' contentEditable='true'></div><div class='quick-reply-close-button'>x</div></div>"
    },

    onQRCloseBtnClicked: function onQRCloseBtnClicked(data) {
        console.log("Inside onQRCloseBtnClicked of main view");
        console.log("Data is::" + data);
        // Destroying the appropriate view
        for (var i = 0; i < this.quickReplyViewList.length; i++) {
            var curView = this.quickReplyViewList[i];
            if (data == curView.model.getNumId()) {
                curView.remove();
                this.quickReplyViewList.splice(i, 1);
                break;
            }
        }
    }



    

});


var SideBarData = Backbone.Model.extend({
        defaults: {
    },
    initialize: function () {
    }
});


var SideBarView = Backbone.View.extend({
    el: '#sidebar-container',
    model: SideBarData,
    

    initialize: function () {
        this.render();
    },

    events: {        
        'click #sidebar-text-holder': 'onTextClicked',
        'click #sidebar-media-holder': 'onMediaClicked',
        'click #sidebar-card-holder': 'onCardClicked',
        'click #sidebar-button-holder': 'onButtonClicked',
        'click #sidebar-quick-reply-holder': 'onQuickReplyClicked'
    },

    render: function () {
        console.log('Inside render of SideBarView');        
    },

    onTextClicked: function (ev) {
        console.log('Text button clicked');
        this.trigger('TEXT_SIDEBAR_CLICKED');
    },

    onMediaClicked: function (ev) {
        console.log('Media button clicked');
        this.trigger('MEDIA_SIDEBAR_CLICKED');
    },

    onCardClicked: function (ev) {
        console.log('Card button clicked');
        this.trigger('CARD_SIDEBAR_CLICKED');
    },

    onButtonClicked: function (ev) {
        console.log('Button button clicked');
        this.trigger('BUTTON_SIDEBAR_CLICKED');
    },

    onQuickReplyClicked: function (ev) {
        console.log('Quick Reply button clicked');
        this.trigger('QUICK_REPLY_SIDEBAR_CLICKED');
    }

});




var QuickReplyData = Backbone.Model.extend({
    defaults: function() {
        return {
            "numId": 999
        }
    },

    getNumId: function getNumId() {
        return this.get('numId');
    },

    setNumId: function setNumId(numId) {
        this.set({'numId': numId});
    },

    initialize: function () {
    }
});


var QuickReplyView = Backbone.View.extend({
    model: QuickReplyData,
    

    initialize: function () {
        this.render();
    },

    events: {        
        'click .quick-reply-close-button': 'onCloseBtnClicked',
        
    },

    render: function () {
        console.log('Inside render of QuickReplyView');        
    },

    onCloseBtnClicked: function onCloseBtnClicked(ev) {
        console.log("Close button clicked");
        this.trigger('QUICK_REPLY_CLOSE_BTN_CLICKED', this.model.get('numId'));
    }

});


var model = new Data();
var view = new NonPromBroadcastView({ model: model });




});
