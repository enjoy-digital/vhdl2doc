function back_to_top() {

$('#backToTop').click(function() {
  var _opt = {
    duration: 800,
    easing: "easeInOutExpo"
  };
$('html, body').animate({
  scrollTop:0,
  },
  _opt
  );
  return false;
  });


}
