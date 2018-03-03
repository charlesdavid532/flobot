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
        this.btnViewList = [];
        this.mainContentViewList = [];
        this.mainContentElement = null;
        this.render();
    },

    events: {
        'change input[type=radio]': 'onMessageTimingBtnClicked',
        'click #non-prom-msg': 'onNonPromMsgClicked',
        'click #offer-submit': 'onBroadcastBtnClicked'

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

    /**


    Text Section
    

    */

    onTextClicked: function (ev) {
        console.log('Text button event detected in main view');
        this.mainContentElement = 'text';
        this.mainContentViewList = [];
        this.generateNewText();
    },

    generateNewText: function generateNewText() {
        var textModel = new TextData();
        textModelId = this.generateRandomNum(1000,10000);
        textModel.setNumId(textModelId);

        this.injectTextHtml(textModelId);

        var textView = new TextView({ model: textModel, el: '#' + textModelId.toString() });

        this.listenTo(textView, 'TEXT_CLOSE_BTN_CLICKED', this.onTextCloseBtnClicked);
        this.mainContentViewList.push(textView);

    },


    injectTextHtml: function injectTextHtml(textId) {
        this.$el.find('.broadcast-builder-content-holder').html(this.createTextHtml(textId));
        var self = this,
            textContainer = this.$el.find('#' + textId);

        textContainer.find('.text-close-button').on("click","", textId, function(ev) {
            self.onTextCloseBtnClicked(ev.data);
        });
    },

    createTextHtml: function createTextHtml(textId) {
        return "<div id='" + textId + "' class='text-elem'><div class='text-text' contentEditable='true'></div><div class='text-close-button'>x</div></div>"
    },


    onTextCloseBtnClicked: function onTextCloseBtnClicked(data) {
        console.log("Inside onTextCloseBtnClicked of main view");
        console.log("Data is::" + data);
        // Destroying the appropriate view
        for (var i = 0; i < this.mainContentViewList.length; i++) {
            var curView = this.mainContentViewList[i];
            if (data == curView.model.getNumId()) {
                curView.remove();
                this.mainContentViewList.splice(i, 1);
                break;
            }
        }
    },


    /**


    Media Section
    

    */

    onMediaClicked: function (ev) {
        console.log('Media button event detected in main view');
        this.mainContentElement = 'media';  
        this.mainContentViewList = [];
    },


    /**


    Card Section
    

    */

    onCardClicked: function (ev) {
        console.log('Card button event detected in main view');
        this.mainContentElement = 'card';
        this.mainContentViewList = [];
    },





    /**


    Button Section
    

    */


    onButtonClicked: function (ev) {
        console.log('Button event detected in main view');
        if (this.btnViewList.length < 3) {
            this.generateNewButton();
        }
        
    },

    generateNewButton: function generateNewButton() {
        var btnModel = new ButtonData();
        btnModelId = this.generateRandomNum(1000,10000);
        btnModel.setNumId(btnModelId);

        this.injectBtnHtml(btnModelId);

        var btnView = new ButtonView({ model: btnModel, el: '#' + btnModelId.toString() });

        this.listenTo(btnView, 'BUTTON_CLOSE_BTN_CLICKED', this.onBtnCloseBtnClicked);
        this.btnViewList.push(btnView);

    },

    injectBtnHtml: function injectBtnHtml(btnId) {
        this.$el.find('.broadcast-builder-buttons-holder').append(this.createBtnHtml(btnId));
        var self = this,
            btnContainer = this.$el.find('#' + btnId);

        btnContainer.find('.btn-close-button').on("click","", btnId, function(ev) {
            self.onBtnCloseBtnClicked(ev.data);
        });
    },

    createBtnHtml: function createBtnHtml(btnId) {
        return "<div id='" + btnId + "' class='btn-elem'><div class='btn-text' contentEditable='true'></div><div class='btn-close-button'>x</div></div>"
    },

    onBtnCloseBtnClicked: function onBtnCloseBtnClicked(data) {
        console.log("Inside onBtnCloseBtnClicked of main view");
        console.log("Data is::" + data);
        // Destroying the appropriate view
        for (var i = 0; i < this.btnViewList.length; i++) {
            var curView = this.btnViewList[i];
            if (data == curView.model.getNumId()) {
                curView.remove();
                this.btnViewList.splice(i, 1);
                break;
            }
        }
    },


    /**


    Quick Reply Section
    

    */





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
    },



    /**
    
    Broadcast section

    */

    onBroadcastBtnClicked: function onBroadcastBtnClicked(ev) {
        //alert('Broadcast button clicked');
        /*
        ev.stopImmediatePropagation();
        ev.stopPropagation();
        ev.preventDefault();
        */
        //$('.message-content-hidden-container').val('abcdefgh');
        //var qrJSONList = this.constructQRJSON();
        //$('.message-content-hidden-container').val(JSON.stringify(qrJSONList));
        var constructedJSON = this.constructJSON();
        console.log("constructed json is::" + JSON.stringify(constructedJSON));
        $('.message-content-hidden-container').val(JSON.stringify(constructedJSON));
    },

    /*
    Checks if the main content is :
    1. Text
        a. If no button - Create sugList
        b. Create button template
    2. Media
    3. Card
    */
    constructJSON: function constructJSON() {
        if (this.mainContentElement == 'text') {
            return this.constructTextJSON();
        } else if(this.mainContentElement == 'media') {
            return this.constructMediaJSON();
        } else if(this.mainContentElement == 'card') {
            return this.constructCardJSON();
        }
    },

    constructTextJSON: function constructTextJSON() {
        if (this.btnViewList.length > 0) {
            return this.constructBtnTemplateJSON();
        } else {
            return this.constructSugListJSON();
        }
    },

    constructSugListJSON: function constructSugListJSON() {
        var sugListJSON = {};
        //sugListJSON["source"] = "phillips-bot";
        //sugListJSON["contextOut"] = [];
        //sugListJSON["speech"] = this.$el.find('.text-text').html();
        //sugListJSON["displayText"] = this.$el.find('.text-text').html();
        //sugListJSON["data"] = {};

        sugListJSON["messages"] = [];


        //dataSugListJSON = sugListJSON["data"];
        dataSugListJSON = sugListJSON["messages"];

        messagesDict = {};
        messagesDict["text"] = this.$el.find('.text-text').html();
        messagesDict["quick_replies"] = this.constructQRJSON();

        dataSugListJSON.push(messagesDict);

        return sugListJSON;
    },

    constructBtnTemplateJSON: function constructBtnTemplateJSON() {
        var sugListJSON = {};
        //sugListJSON["source"] = "phillips-bot";
        //sugListJSON["contextOut"] = [];
        //sugListJSON["speech"] = this.$el.find('.text-text').html();
        //sugListJSON["displayText"] = this.$el.find('.text-text').html();
        //sugListJSON["data"] = {};

        sugListJSON["messages"] = [];


        //dataSugListJSON = sugListJSON["data"];
        dataSugListJSON = sugListJSON["messages"];

        messagesDict = {};
        messagesDict["attachment"] = {};
        attachmentDict = messagesDict["attachment"];

        attachmentDict["type"] = "template";
        attachmentDict["payload"] = {};
        payloadDict = attachmentDict["payload"];
        //facebookDict["facebook"] = {};
        //dataSugListJSON["facebook"] = {};

        //facebookSugListJSON = facebookDict["facebook"];
        payloadDict["template_type"] = "button";
        payloadDict["text"] = this.$el.find('.text-text').html();
        payloadDict["buttons"] = this.constructBtnJSON();

        messagesDict["quick_replies"] = this.constructQRJSON();


        dataSugListJSON.push(messagesDict);

        return sugListJSON;
    },


    constructMediaJSON: function constructMediaJSON() {

    },

    constructCardJSON: function constructCardJSON() {
        var sugListJSON = {};
        //sugListJSON["source"] = "phillips-bot";
        //sugListJSON["contextOut"] = [];
        //sugListJSON["speech"] = this.$el.find('.text-text').html();
        //sugListJSON["displayText"] = this.$el.find('.text-text').html();
        //sugListJSON["data"] = {};

        sugListJSON["messages"] = [];


        //dataSugListJSON = sugListJSON["data"];
        dataSugListJSON = sugListJSON["messages"];

        messagesDict = {};
        messagesDict["attachment"] = {};
        attachmentDict = messagesDict["attachment"];

        attachmentDict["type"] = "template";
        attachmentDict["payload"] = {};
        payloadDict = attachmentDict["payload"];
        //facebookDict["facebook"] = {};
        //dataSugListJSON["facebook"] = {};

        //facebookSugListJSON = facebookDict["facebook"];
        payloadDict["template_type"] = "generic";
        payloadDict["elements"] = [];
        elementsArr = payloadDict["elements"];

        elementsDict = {};
        elementsDict["title"] = this.$el.find('.text-text').html();
        elementsDict["subtitle"] = "Dummy";
        
        elementsArr.push(elementsDict);

        messagesDict["quick_replies"] = this.constructQRJSON();


        dataSugListJSON.push(messagesDict);

        return sugListJSON;
    },

    constructBtnJSON: function constructBtnJSON() {
        var btnJSONList = [];
        for (var i = 0; i < this.btnViewList.length; i++) {
            var curView = this.btnViewList[i];
            btnJSONList.push(curView.getJSON());
        }

        console.log(JSON.stringify(btnJSONList));
        return btnJSONList;

    },

    constructQRJSON: function constructQRJSON() {
        var qrJSONList = [];
        for (var i = 0; i < this.quickReplyViewList.length; i++) {
            var curView = this.quickReplyViewList[i];
            qrJSONList.push(curView.getJSON());
        }

        console.log(JSON.stringify(qrJSONList));
        return qrJSONList;

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
    },

    getJSON: function getJSON() {
        var qrJSON = {};
        qrJSON["content_type"] = "text";
        var title = this.$el.find('.qr-text').html();
        console.log("The title is::" + title);
        qrJSON["title"] = title;
        qrJSON["payload"] = title;
        return qrJSON;
    }

});



var ButtonData = Backbone.Model.extend({
    defaults: function() {
        return {
            "numId": 888
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


var ButtonView = Backbone.View.extend({
    model: ButtonData,
    

    initialize: function () {
        this.render();
    },

    events: {        
        'click .button-close-button': 'onCloseBtnClicked',
        
    },

    render: function () {
        console.log('Inside render of ButtonView');        
    },

    onCloseBtnClicked: function onCloseBtnClicked(ev) {
        console.log("Close button clicked");
        this.trigger('BUTTON_CLOSE_BTN_CLICKED', this.model.get('numId'));
    },

    getJSON: function getJSON() {
        var btnJSON = {};
        btnJSON["type"] = "web_url";
        var title = this.$el.find('.btn-text').html();
        console.log("The title is::" + title);
        btnJSON["title"] = title;
        btnJSON["url"] = "https://www.google.com"
        return btnJSON;
    }

});


var TextData = Backbone.Model.extend({
    defaults: function() {
        return {
            "numId": 777
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


var TextView = Backbone.View.extend({
    model: TextData,
    

    initialize: function () {
        this.render();
    },

    events: {        
        'click .text-close-button': 'onCloseBtnClicked',
        
    },

    render: function () {
        console.log('Inside render of TextView');        
    },

    onCloseBtnClicked: function onCloseBtnClicked(ev) {
        console.log("Close button clicked");
        this.trigger('TEXT_CLOSE_BTN_CLICKED', this.model.get('numId'));
    },

    getJSON: function getJSON() {
        var textJSON = {};
        
        var title = this.$el.find('.text-text').html();
        console.log("The title is::" + title);
        textJSON["text"] = title;
        return textJSON;
    }

});



var model = new Data();
var view = new NonPromBroadcastView({ model: model });




});
