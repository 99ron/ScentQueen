// This JS file is for functions needed to make certain elements work as intended.

// This is for the bubbly button animations
var animateButton = function(e) {

  e.preventDefault;
  //reset animation
  e.target.classList.remove('animate');
  
  e.target.classList.add('animate');
  setTimeout(function(){
    e.target.classList.remove('animate');
  },700);
};

var bubblyButtons = document.getElementsByClassName("bubbly-button");

for (var i = 0; i < bubblyButtons.length; i++) {
  bubblyButtons[i].addEventListener('click', animateButton, false);
}



$('.owl-carousel').owlCarousel({
        loop:false,
        margin:10,
        nav:true,
        dots:true,
        autoplay:true,
        autoplayHoverPause:true,
        navigation:true,
        items:4,
        responsive:{
          0:{
            items:1
          },
            480:{
        items:2
          },
            768 :{
        items:3  
          },
            991 :{
        items:4
            }
        }
    });
