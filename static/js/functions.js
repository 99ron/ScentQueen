// This JS file is for functions needed to make certain elements work as intended.



// This is for the product page increase/decrease buttons.
function increaseValue() {
  var value = parseInt(document.getElementById('productAmount').value, 10);
  value = isNaN(value) ? 2 : value;
  value++;
  document.getElementById('productAmount').value = value;
}

function decreaseValue() {
  var value = parseInt(document.getElementById('productAmount').value, 10);
  value = isNaN(value) ? 2 : value;
  value < 2 ? value = 2 : '';
  value--;
  document.getElementById('productAmount').value = value;
}


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

