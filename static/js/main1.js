console.log("Start main 1");
require(['main2'], function() {
        console.log("After main2 should have loaded")
    });
console.log("End main 1");

/*
require(["jquery-ui"], function (abcd) {
	//$("#container").html("Hellow world");
	console.log("hi1");
});
*/