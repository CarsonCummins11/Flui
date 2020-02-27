from paypalrestsdk import Payment
import paypalrestsdk
from app.scraping.authentication.auth import auth_data
def pay():
	paypalrestsdk.configure({
		'mode': 'sandbox', #change to live when not testing
		'client_id': auth_data['paypal_auth']['client_id'],
		'client_secret': auth_data['paypal_auth']['secret']})

	payment = Payment({
		"intent": "sale",

	  # Set payment method
		"payer": {
			"payment_method": "paypal"
		},

	  # Set redirect URLs, these still need to be updated for testing to work
		"redirect_urls": {
			"return_url": "http://localhost:5000/advertiserprofile",
			"cancel_url": "http://localhost:5000/advertiserprofile"
		},

	  # Set transaction object
		"transactions": [{
			"amount": {
				"total": "1.00",
				"currency": "USD"
			},
			"description": "payment description"
		}]
	})
	if payment.create():
		for link in payment.links:
			if link.method == "REDIRECT":
				redirect_url = (link.href)
	else:
		print("Error making payment.")
		print(payment.error)
	print("bullshit")
	print(payment)