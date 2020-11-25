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