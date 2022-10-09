// Navbar js for closing outside the area
$(document).ready(function () {

  $(document).click(function (event) {
      var click = $(event.target);
      var _open = $(".navbar-collapse").hasClass("show");
      if (_open === true && !click.hasClass("navbar-toggler")) {
          $(".navbar-toggler").click();
      }
  });


// Search toggle js
  $( "#search-toggle" ).click(function() { 
    $(".search-center").toggle();
  });

// hero banner script

  $('#hero-slider').flexslider({
      animation: "slide",
      directionNav: false,
  });

// Package banner script

  $('#package-slider').flexslider({
      animation: "slide",
      itemWidth: 210,
      directionNav: true,
      animationLoop: true,
      minItems: 4,        
      maxItems: 4,
      itemMargin: 20,
      slideshow: true,
  });


// Package banner script

  $('#mobile-package-slider').flexslider({
      animation: "slide",
      itemWidth: 350,
      directionNav: false,
      controlNav: false,
      animationLoop: true,
      minItems: 1,        
      maxItems: 2,
      itemMargin: 20,
      slideshow: true,
  });



});


$(document).ready(function() {
  // Gets the video src from the data-src on each button
  var $videoSrc;
  $(".video-btn").click(function() {
    $videoSrc = $(this).attr("data-src");
    console.log("button clicked" + $videoSrc);
  });

  // when the modal is opened autoplay it
  $("#myModal").on("shown.bs.modal", function(e) {
    console.log("modal opened" + $videoSrc);
    // set the video src to autoplay and not to show related video. Youtube related video is like a box of chocolates... you never know what you're gonna get
    $("#video").attr(
      "src",
      $videoSrc + "?autoplay=1&showinfo=0&modestbranding=1&rel=0&mute=1"
    );
  });

  // stop playing the youtube video when I close the modal
  $("#myModal").on("hide.bs.modal", function(e) {
    // a poor man's stop video
    $("#video").attr("src", $videoSrc);
  });

  
    $('.nav-button').click(function(){
    $('body').toggleClass('nav-open');
    });

    $('.main-menu .dropdown-toggle').click(function(){
      $('.dropdown-menu ').toggleClass('show');
      });

      // Sticky header script 
    jQuery(function() {
    var header = jQuery(".main-top-header");
       jQuery(window).scroll(function() {
            var scroll = jQuery(window).scrollTop();
            if (scroll >= 200) {
                header.addClass("sticky");
            } else {
                header.removeClass("sticky");
            }
        });
    });
  
});

 