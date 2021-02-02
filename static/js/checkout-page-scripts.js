// This JS file is for the checkout page
/*global paypal*/

// Render the PayPal button into #paypal-button-container

if (shipping == 'False'){
	document.getElementById('shipping-info').innerHTML = '';
}

// if (user != 'AnonymousUser'){
// 	document.getElementById('user-info').innerHTML = '';
// }

if (shipping == 'False' && user != 'AnonymousUser'){
	// Hide entire form if user is logged in and shipping is false
	document.getElementById('form-wrapper').classList.add("hidden");
	// Show payment if logged in user wants to buy an item that does not require shipping
	document.getElementById('payment-info').classList.remove("hidden");
}




var form = document.getElementById('form');

crsftoken = form.getElementsByTagName("input")[0].value;
console.log("NewToken: ", form.getElementsByTagName("input")[0].value);

form.addEventListener('submit', function(e){
	e.preventDefault();
	console.log('Form submitted...');
	document.getElementById('form-button').classList.add('hidden');
	document.getElementById('payment-info').classList.remove('hidden');
});


function submitFormData(){
	console.log('Payment button clicked');
	console.log('Total: ', total);
	
	var userFormData = {
		'name':null,
		'email':null,
		'total':total,
	}
	
	var shippingInfo = {
		'address1':null,
		'address2':null,
		'city':null,
		'county':null,
		'postcode':null,
	}
	
	if(shipping != 'False'){
		shippingInfo.address1 = form.address1.value
		shippingInfo.address2 = form.address2.value
		shippingInfo.city = form.city.value
		shippingInfo.county = form.county.value
		shippingInfo.postcode = form.postcode.value
	}
	
	if(user == 'AnonymousUser'){
		userFormData.name = form.name.value
		userFormData.email = form.email.value
		}


	var url = '/process_order/'
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},
		body: JSON.stringify({'form':userFormData, 'shipping':shippingInfo}),
	})
	.then((response) => response.json())
	.then((data) => {
		console.log('Success:', data);
		alert('Transaction completed');
		
		cart= {};
		document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
		
		window.location.href = "{% url 'store' %}";
	});
}	
