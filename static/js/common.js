console.log("Common js started loading");
requirejs.config({
	baseUrl: "../../static/js",
	paths: {
		jquery: [
			'//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min',		
			'jquery.min'
		],
		jqueryUI: [
			'//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min',
			'jquery-ui.min'
		],
		underscore: [
			'//ajax.cdnjs.com/ajax/libs/underscore.js/1.1.4/underscore-min',
			'underscore.min'
		],
		backbone: [
			'//ajax.cdnjs.com/ajax/libs/backbone.js/0.3.3/backbone-min',
			'backbone.min'
		],
		jqueryTimeAddon: [
			'//cdnjs.cloudflare.com/ajax/libs/jquery-ui-timepicker-addon/1.6.3/jquery-ui-timepicker-addon.min',
			'jquery-ui-timepicker-addon.min'
		],
		nonPromBroadcast: [
			'non-prom-broadcast'
		]
	}

});
console.log("Common js finished loading");