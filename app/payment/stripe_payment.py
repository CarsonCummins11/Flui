#Commenting this out for testing, there isn't a 'stripe_auth' in the version of the auth file I was testing with
"""
from paypalrestsdk import Payment
from app.scraping.authentication import auth
import stripe
stripe.api_key = auth.auth_data['stripe_auth']['secret']
def payment(amount):
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'name': 'Advertisement',
      'description': 'This branded content will help your brand grow at unreasonable rates',
      'images': ['/static/images/logo_square.png'],
      'amount': amount,
      'currency': 'usd',
      'quantity': 1,
    }],
    success_url='/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='/cancel'
  )
  return session
"""