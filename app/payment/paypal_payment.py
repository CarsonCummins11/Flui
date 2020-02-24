import paypalrestsdk
from app.scraping.authentication.auth import auth_data

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
		"return_url": "http://localhost:3000/process",
		"cancel_url": "http://localhost:3000/cancel"
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
#NOT FINISHED
if payment.create():
	for link in payment.links:
		if link.method == "REDIRECT':
			redirect_url = (link.href)
			
	