from paypalrestsdk import Payment
from app.scraping.authentication import auth
import stripe
def payment(amount):
  stripe.api_key = auth.auth_data['stripe_auth']['secret']
  print(stripe.api_key)
  print(int(amount))
  session = stripe.checkout.Session.create(
  success_url="https://flui.co/success",
  cancel_url="https://flui.co/cancel",
  payment_method_types=["card"],
  line_items=[
    {
      "name": "Flui Ad Campaign",
      "description": "An ad campaign that will revamp your company",
      "amount": int(amount)*100,
      "currency": "usd",
      "quantity": 1,
    },
  ],
  )
  return session