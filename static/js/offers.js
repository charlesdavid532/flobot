$(function(){

   // jQuery methods go here...
   $("#redeem-another").click(function(){
        $("#offer-form").trigger("reset");
        $("#offerCode").val('');
        $("#billAmount").val('');
        $("#name").val('');
        $(".flash").html("");
    });


   $("#create-another").click(function(){
        $("#create-offer-form").trigger("reset");
        $("#percentOff").val('');
        $("#minbillAmount").val('');
        $("#startDate").val('');
        $("#expiresAtDate").val('');
        $("#photo").val('');
        $("#offerCode").val('');
        $("#offerTitle").val('');
        $("#offerText").val('');
        $(".flash").html("");
    });

});