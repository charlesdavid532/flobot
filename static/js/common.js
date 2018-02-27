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
			'//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min',
			'underscore.min'
		],
		backbone: [
			'//cdnjs.cloudflare.com/ajax/libs/backbone.js/1.0.0/backbone-min',
			'backbone.min'
		],
		jqueryTimeAddon: [			
			'jquery-ui-timepicker-addon.min'
		],
		nonPromBroadcast: [
			'non-prom-broadcast'
		]
	}

});
console.log("Common js finished loading");