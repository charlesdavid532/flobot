$(function(){

   // jQuery methods go here...
   $("#redeem-another").click(function(){
        $("#offer-form").trigger("reset");
        $("#offerCode").val('');
        $("#billAmount").val('');
        $("#name").val('');
        $(".flash").html("");
    });

});