$(function(){
  console.log(":)))))");

  $('input[name="text"]').keypress(function(event) {
    console.log(":)");
    $('.has-error').hide();
  });
});
