require(['jquery'], function($) {
		console.log("After jquery should have been loaded");
		$(".container").html("Hellow");
		require(['jqueryUI'], function() {
			console.log("After jquery and jqueryUI should have loaded");
			require(['underscore'], function(_) {
				console.log("After jquery and jqueryUI and underscore should have loaded");
				require(['backbone'], function(Backbone) {
					console.log("After jquery and jqueryUI and underscore and Backbone should have loaded");
					require(['jqueryTimeAddon'], function() {
						console.log("After jquery and jqueryUI and underscore and Backbone and jquery addon should have loaded");
					});
				});
			});
		});
        
    });

/*
define(['jquery'], function ($) {
	$(".container").html("Hellow world");
	console.log("hi");

});
*/