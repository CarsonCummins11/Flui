from app import db
from flask_login import current_user
import stripe
from app.scraping.authentication.auth import auth_data
from app.request import Request
import time as time
import threading
def fulfill(session):
    r = db['advertisers'].find_one({'pending_request.session':session})
    if(r is not None):
        r = r['pending_request']
        db['advertisers'].update({'user':r['author']},{'$push':{'request':r}})
        Request.from_json(r).sendmail()
    else:
        print('r was none')
def do_fulfillment():
    stripe.api_key = auth_data['stripe_auth']['secret']

    events = stripe.Event.list(
    type='checkout.session.completed',
    created={
        # Check for events created in the last 24 hours.
        'gte': int(time.time() - 24 * 60 * 60),
    },
    )
    for event in events.auto_paging_iter():
        session = event['data']['object']
        threading.Thread(target=fulfill, args = (str(session.id),)).start()