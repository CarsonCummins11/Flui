from app import db
from flask_login import current_user
import stripe
from app.scraping.authentication import auth
def fulfill(session):
    r = db['advertisers'].find_one({'pending_request':{'session':session}})['pending_request']
    if(r is not None):
        db['advertisers'].update({'user':r.author},{'$push':{'request':r.get_json()}})
        r.sendmail()
def do_fulfillment():
    stripe.api_key = auth['stripe_auth']['secret']

    events = stripe.Event.list(
    type='checkout.session.completed',
    created={
        # Check for events created in the last 24 hours.
        'gte': int(time.time() - 24 * 60 * 60),
    },
    )

    for event in events.auto_paging_iter():
        session = event['data']['object']

    # Fulfill the purchase...
    fulfill(session)