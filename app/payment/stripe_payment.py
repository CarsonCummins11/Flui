from app.scraping.authentication import auth
import stripe
from app import InfluencerProfile
def payment(amount):
  stripe.api_key = auth.auth_data['stripe_auth']['secret']
  print(stripe.api_key)
  print(int(amount))
  session = stripe.checkout.Session.create(
  success_url="https://www.flui.co/success",
  cancel_url="https://www.flui.co/cancel",
  payment_method_types=["card"],
  line_items=[
    {
      "name": "Flui Ad Campaign",
      "description": "An ad campaign that will revolutionize your company",
      "amount": int(amount)*100,
      "currency": "usd",
      "quantity": 1,
    },
  ],
  )
  return session
def pay_influencer(influencer):
  stripe.api_key = auth.auth_data['stripe_auth']['secret']
  val = InfluencerProfile.Influencer.from_dict(influencer).findCost()
  transfer = stripe.Transfer.create(
  amount=val,
  currency="usd",
  destination=influencer['stripe_id'],
)