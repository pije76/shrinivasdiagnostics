$('#home-slider').owlCarousel({
    loop:true,
    margin:0,
    nav:false,
    slideSpeed : 100,
    singleItem:true,
    dots:true,
    autoPlay : false,
    navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        },
        1300:{
            items:1
        }
    }
})

$('#list-slider').owlCarousel({
    loop:true,
    margin:15,
    nav:true,
    slideSpeed : 100,
    singleItem:true,
    dots:false,
    autoPlay : false,
    navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:3
        },
        1300:{
            items:4
        }
    }
})

$('.filter-box h4').on('click', function() {
    $(this).closest('.filter-box').toggleClass('filter-closed');
});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

