var cise_email = "consult@cise.ufl.edu";
var csrftoken = getCookie('csrftoken');
//------------------------------------------------------------------------------
function set_active_menu_tab(active_id) {
    $('.primary-nav').each(function() {
        $(this).removeClass("nav-active");
    });
    $('#' + active_id).addClass("nav-active");
}
//------------------------------------------------------------------------------
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//------------------------------------------------------------------------------
function setup_ajax() {
  // Setup CSRF for AJAX
  $.ajaxSetup({
     beforeSend: function(xhr, settings) {

         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
  });
}
//------------------------------------------------------------------------------
$('.option').mouseover(function() {
    $(this).css({
        "background-color": "#cbe8ff",
    });
    $(this).mouseout(function() {
        $(this).css({
            "background-color": "white",
        });
    });
});
//------------------------------------------------------------------------------
function moveScroller() {
    var $anchor = $("#scroller-anchor");
    var $scroller = $('#scroller');
    var move = function() {
      var st = $(window).scrollTop();
      var ot = $anchor.offset().top;
      if(st > ot) {
          $scroller.css({
              position: "fixed",
              top: "0px",
          });
      } else {
          $scroller.css({
              position: "relative",
              top: ""
          });
      }
    };
    $(window).scroll(move);
    move();
}
//------------------------------------------------------------------------------
function direct_to_href(element) {
  window.location.href = element.attr('href');
}
//------------------------------------------------------------------------------
