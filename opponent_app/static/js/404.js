$(document).mousemove(function (event) {
  $('.torch').css({
    'top': event.pageY,
    'left': event.pageX
  });
});
