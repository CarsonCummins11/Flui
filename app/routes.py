#routes.py
#routes html requests to python functions
from flask import render_template,request, session,redirect,escape,jsonify
from app import app,db,User,AdvertiserProfile,InfluencerProfile,payment
from app.InfluencerProfile import Influencer
from app.AdvertiserProfile import Advertiser
from app.payment import stripe_payment,fulfiller
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user, login_user, login_required,logout_user
import pickle
from app.request import Request
from jinja2 import Environment, BaseLoader
from urllib.parse import unquote
import secrets
import yagmail
import nltk
from app.scraping import scraping_workflow
from app.scraping.tagger import Tagger
from app.scraping.authentication import auth
import stripe
import json
from requests_oauthlib import OAuth1Session
import requests
import re
from lxml import html
nltk.download('punkt')
searchtagger = Tagger()
@app.route("/")
def main(): 
    #returns the home page on start
    return render_template('home.html')
@app.route("/about")
def about(): #returns the about page
    return render_template('About.html')
@app.route("/checkusername",methods=['POST'])
def checkusername():
    if db['influencers'].find_one({'user':request.get_json()['user']}) is None and db['advertisers'].find_one({'user':request.get_json()['user']}) is None:
        return 'Username is available'
    else:
        return 'That username is in use'
@app.route("/newinfluencer",methods=['POST'])
def newinfluencer(): #Creates a new influencer with blank information from the request form
    if db['influencers'].find_one({'user':request.form['user']}) is None and db['advertisers'].find_one({'user':request.form['user']}) is None:
        new_influencer = Influencer(
            name = escape(request.form['name']), #NewInfluencer has the tag as 'name', but when you inspect it's still fname?
            username = request.form['user'],
            password = request.form['pass'], #generates hash in __init__()
            email = escape(request.form['email']),
            desc = 'No description',
            img = '/static/images/default_profile_image.png',
            insta = 'No Instagram',
            yt = 'No Youtube',
            tw = 'No Twitter',
            tags = '',
            votes={}
        )
        db['influencers'].insert_one(new_influencer.to_dict()) #Adds the profile to db, needs to be a dict
        use = User.User(username=new_influencer.username) #Sets the user to the newly created user
        login_user(use) #Logins in through Flask's LoginManager
        return redirect('/influencerprofile') #Redirects to their profile
    else:
        return 'That username is in use'
@app.route('/uploadimage',methods=['POST'])
def updateimage():
    if db['advertisers'].find_one({'user':current_user.username}) is None:
        db['influencers'].update({'user':current_user.username},{'$set':{'img':str(request.get_json()['img'])}}) 
        return 'good'
    else:
        db['advertisers'].update({'user':current_user.username},{'$set':{'img':str(request.get_json()['img'])}}) 
        return 'good'
@app.route("/newadvertiser",methods=['POST'])
def newadvertiser(): #Creates a new advertiser
    if db['advertisers'].find_one({'user':request.form['user']}) is None and db['influencers'].find_one({'user':request.form['user']}) is None:
        new_advertiser = Advertiser(
            company=escape(request.form['company']),
            username = request.form['user'],
            password = request.form['pass'], #generates hash in __init__()
            desc = 'No Description',
            email = 'No Email',
            img = '/static/images/default_profile_image.png'
        )
        db['advertisers'].insert_one(new_advertiser.to_dict()) #Adds the profile to db, needs to be a dict
        use = User.User(username=new_advertiser.username) #Sets the user to the newly created user
        login_user(use)#Logins in through Flask's LoginManager
        return redirect('/advertiserprofile')#Redirects to their profile
    else:
        return 'That username is in use'

@app.route("/logininfluencer",methods=['POST'])
def logininfluencer(): #login method for an influencer, if login fails, either incorrect user or password, directs to /, if not, redirects to their profile
    prof = db['influencers'].find_one({"user":request.form['user']})
    if prof is None:
        print('no user')
        return redirect('/')
    if(check_password_hash(prof['pass'],request.form['pass'])): #Uses the password hash to auth
        print('success')
        login_user(User.User(username=request.form['user'])) #Log the user in
        return redirect('/influencerprofile')
    print('bad password')
    return redirect('/')
@app.route("/loginadvertiser",methods=['POST'])
def loginadvertiser(): #Logs an advertiser in
    fulfiller.do_fulfillment()#fulfills any standing advertiser requests
    prof = db['advertisers'].find_one({"user":request.form['user']}) #find's an advertiser from db
    if prof is None:
        return redirect('/')
    if(check_password_hash(prof['pass'],request.form['pass'])): #If correct pass, redirect to their profile
        login_user(User.User(username=request.form['user']))
        return redirect('/advertiserprofile')
    return redirect('/')
@app.route("/advertiserprofile")
@login_required
def advertiserprofile(): #If the user isn't null, then return a rendered template(using Jinja), this is used in rendering to browser
    profile = db['advertisers'].find_one({'user':current_user.username})
    return render_template('AdvertiserProfile.html',profile=profile) 
@app.route("/influencerprofile")
@login_required
def influencerprofile(): #If the user isn't null, then return a rendered template(using Jinja), this is used in rendering to browser
    profile = db['influencers'].find_one({'user':current_user.username})
    return render_template('InfluencerProfile.html',profile=profile,instagram_app_id=auth.auth_data['insta_auth']['app_id'],yt_client_id=auth.auth_data['yt_auth']['client_id'])
@app.route("/advertiserprofilechange",methods=['POST'])
@login_required
def advertiserprofilechange(): #Changes the current user based on a request form
    db['advertisers'].update({'user':current_user.username},{'$set':{"company":escape(request.form['company']),"desc":escape(request.form['desc']),"email":escape(request.form['email'])}})
    return redirect('/advertiserprofile')
@app.route("/searchforinfluencers")
@login_required
def searchforinfluencers(): #Returns the search form for influencers
    if(db['advertisers'].find_one({'user':current_user.username}) is not None):
        return render_template('InfluencerSearch.html')
    else:
        return render_template('CollabSearch.html')
@app.route("/advertisersearch", methods=['POST'])
@login_required
def advertisersearch(): #Creates an array of advertisers that match a tag and returns it
    db['advertisers'].create_index([('tags', 'text')])
    results = db['advertisers'].find({ '$text': { '$search': request.get_json()['term'] } }) #find all advertisers with a tag
    ret = {}
    i = 0
    for k in results:
        ret[str(i)]=AdvertiserProfile.create_from(k) #Adds advertiser's rendered template to a list(something that can be outputed to a webpage)
        i+=1
    return ret if len(ret)>0 else 'no matches for that term:(' #Returns the results
@app.route("/influencersearch", methods=['POST'])
@login_required
def influencersearch(): #Creates an array of influencers that match a tag and returns it
    print('search term: '+str(request.get_json()['term'].split(' ')))
    terms = (searchtagger.tag(request.get_json()['term'].split(' '))['plain'])
    term = ' '.join(terms)
    print('generated term: '+term)
    db['influencers'].create_index([('tags','text')])
    results = db['influencers'].find({'$text': { '$search': term } })
    def countofterms(val):
        count = 0
        for k in terms:
            if k in val['votes'].keys():
                count+=val['votes'][k]
        return count
    results = list(results)
    results.sort(key=countofterms,reverse=True)
    ret = {}
    i = 0
    for k in results:
        ret[str(i)]=InfluencerProfile.create_from(k) #Adds influencers's rendered template to a list(something that can be outputed to a webpage)
        i+=1
    return ret if len(ret)>0 else 'no matches for term:(' #Returns the results
@app.route("/createrequest", methods=['POST'])
@login_required
def create_request(): #Creates a request object from a form submission
    sess = stripe_payment.payment(request.form['budget'])
    r = Request(
        budget=request.form['budget'],
        link=request.form['note'],
        tags=unquote(request.args.get('tags')),
        contact=request.form['contact'],
        user='',
        author=current_user.username,
        session =sess.id
    )
    db['advertisers'].update({'user':current_user.username},{'$set':{'pending_request':r.get_json()}})
    authorize={'public_key':auth.auth_data['stripe_auth']['public'],'CHECKOUT_SESSION_ID':sess.id}
    return render_template("stripe_payment.html",authori=authorize)
@app.route("/adwithgroup")
@login_required
def adwithgroup():
    return render_template('buygroup.html')
@app.route("/viewcampaign")
@login_required
def viewcampaign():
    return render_template('viewcampaign.html',prof=db['advertisers'].find_one({'user':current_user.username}))
@app.route("/viewrequest")
@login_required
def viewrequest():
    prof = db['influencers'].find_one({'user':request.args.get('user')})['request']
    if type(prof) is not dict:
        try:
            prof = prof[int(request.args.get('r'))]
        except:
            return render_template('no_ads.html')
    r= Request(
        budget=prof['budget'],
        link=prof['link'],
        tags=prof['tags'],
        contact=prof['contact'],
        author=prof['author'],
        user=request.args.get('user'),
        r=int(request.args.get('r'))
    )
    return redirect('/viewrequest?r='+str(int(request.args.get('r'))+1)) if prof['completed']==1 else r.get_render_template()
@app.route("/viewadvertiserprofile")
def viewadvertiserprofile():
    prof = db['advertisers'].find_one({'user':request.args.get('user')})
    return render_template('StaticAdvertiser.html',profile=prof)
@app.route("/viewinfluencerprofile")
def viewinfluencerprofile():
    prof = db['influencers'].find_one({'user':request.args.get('user')})
    return render_template('StaticInfluencer.html',profile=prof)
@app.route('/submitad',methods=['POST'])
@login_required
def submitad():
    link = request.form['link']
    db['influencers'].update({'user':current_user.username},{'$push':{'link':link}})
    adnumber = request.args.get('r')
    prof = db['influencers'].find_one({'user':request.args.get('user')})['request']
    if type(prof) is not dict:
        try:
            prof = prof[int(adnumber)]
        except:
            print('stop it hacker')
            return redirect('/logout')
    db['advertisers'].update({'user':prof['author']},{'$push':{'links':link}})
@app.route('/likead',methods=['POST'])
@login_required
def likead():
    def prof_from_link(link):
        result = re.sub(r'(.*://)?([^/?]+).*', '\g<1>\g<2>', link)
        if 'youtube' in result:
            uname = requests.get(link).text.split('<a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/channel/"')[1].split('dir="auto">')[0]
            return db['influencers'].find_one({'youtube':uname})
        elif 'twitter' in result:
            uname = link.split('https://twitter.com/')[1].split('/')[0]
            return db['influencers'].find_one({'twitter':uname})
        elif 'instagram' in result:
            k = html.fromstring(requests.get(link).content).xpath('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/a')
            uname = k.split('>')[1].split('<')[0]
            return db['influencers'].find_one({'instagram':uname})
    if request.get_json()['link'] in db['advertisers'].find_one({'user':current_user.username})['links']:
        prof=prof_from_link(request.get_json()['link'])
        stripe_payment.pay_influencer(prof)
        yag = yagmail.SMTP(auth.auth_data['yag_auth']['username'], auth.auth_data['yag_auth']['password'])
        yag.send(prof['email'],'Flui Sponsorship',["What's up!\n\nYou've just been paid for your content! Congrats- Keep earning with Flui.\n\n-Carson Cummins\n\nFounder,Flui"])
        db['advertisers'].update({'user':current_user.username},{'$pull':{'link':request.get_json()['link']}})
    else:
        #fuck hackers
        return redirect('/logout')
@app.route('/submitinfluencer')
def submitinfluencer():
    return render_template('submit.html')
@app.route('/gosubmitinfluencer',methods=['POST'])
def gosubmitinfluencer():
    form = request.form.to_dict(flat=False)
    inf = db['influencers'].find_one({'email':request.form['email']})
    def buildvotes(t):
        ret = {}
        for k in t:
            ret[k] = 1
        return ret
    def combine_vote_tables(t_new,t_cur):
        ret = {}
        for k in t_new:
            if k in t_cur.keys():
                ret[k] = t_new[k]+t_cur[k]
            else:
                ret[k] = t_new[k]
        return ret
    if(inf is not None):
        newtags=inf['tags']
        tags_votes_cur = inf['votes']
        for tag in form['tags']:
            if not tag in newtags:
                newtags+=','+tag
            else:
                tags_votes_cur['tag']+=1
        db['influencers'].update({'email':request.form['email']},{'$set':{'tags':newtags}})
        db['influencers'].update({'email':request.form['email']},{'$set':{'votes':tags_votes_cur}})
                
    else:
        passw = secrets.token_urlsafe(32)
        new_influencer = Influencer(
            name = request.form['name'], #NewInfluencer has the tag as 'name', but when you inspect it's still fname?
            username = request.form['email'],
            password = passw, #generates hash in __init__()
            email = request.form['email'],
            desc = '',
            img = '',
            insta = '',
            yt = '',
            tw = '',
            tags = ','.join(form['tags']),
            votes=buildvotes(form['tags'])
        )
        db['influencers'].insert_one(new_influencer.to_dict())
        yag = yagmail.SMTP('carson@flui.co', 'Luv4soccer.1')
        yag.send(form['email'],'Flui Sponsorship',["What's up "+request.form['name']+"!\n\n One of your followers just sponsored you to join the Flui advertising network - an advertising platform focused on smaller influencers. That's really cool. To log in, go to https://flui.co and use this email for your username and "+passw+" as your password.\n\n-Carson Cummins\n\nFounder,Flui"])
    return redirect('/submitinfluencer')
@app.errorhandler(404)
def notfound(e):
    return render_template('notfound.html'),404
@app.errorhandler(500)
def errhand(e):
    return render_template('notfound.html'),500
@app.route('/influencersettings')
@login_required
def influencersettings():
    return render_template('influencersettings.html')
@app.route('/advertisersettings')
@login_required
def advertisedrsettings():
    return render_template('advertisersettings.html')
@app.route('/tagsvoting',methods=['GET'])
@login_required
def tagsvoting():
    return jsonify(db['influencers'].find_one({'user':current_user.username})['votes'])
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
@app.route('/resetpassword')
@login_required
def resetpassword():
    if db['influencers'].find_one({'user':current_user.username}):
        def generate_password_reset():
            reset_key = secrets.token_urlsafe(32)
            db['influencers'].update({'user':current_user.username},{'$set':{'reset_key':reset_key}})
            return 'http://www.flui.co/reset_pw?key='+reset_key
        use = db['influencers'].find_one({'user':current_user.username})
        yag = yagmail.SMTP('carson@flui.co', 'Luv4soccer.1')
        yag.send(use['email'],'Password reset',["Hey  "+use['name']+",\n\n I heard you needed to reset your password so I'm sending along this link to help you do that:\n"+generate_password_reset()+"\n\n-Carson Cummins\n\nFounder,Flui"])
        return redirect('/')
    else:
        def generate_password_reset():
            reset_key = secrets.token_urlsafe(32)
            db['advertisers'].update({'user':current_user.username},{'$set':{'reset_key':reset_key}})
            return 'https://flui.co/reset_pw?key='+reset_key
        use = db['advertisers'].find_one({'user':current_user.username})
        yag = yagmail.SMTP('carson@flui.co', 'Luv4soccer.1')
        yag.send(use['email'],'Password reset',["Hey  "+use['comapny']+" team,\n\n I heard you needed to reset your password so I'm sending along this link to help you do that:\n"+generate_password_reset()+"\n\n-Carson Cummins\n\nFounder,Flui"])
        return redirect('/')
@app.route('/reset_pw',methods=['GET','POST'])
def reset_pw():
    if request.method == 'POST':
        if(db['influencers'].find_one({'reset_key':request.args.get('key')}) is not None):
            db['influencers'].update({'reset_key':request.args.get('key')},{'$set':{'pass':generate_password_hash(request.form['pass'])}})
        elif(db['advertisers'].find_one({'reset_key':request.args.get('key')}) is not None):
            db['advertisers'].update({'reset_key':request.args.get('key')},{'$set':{'pass':generate_password_hash(request.form['pass'])}})
        else:
            print('uhh hacker?')
        return redirect('/')
    else:
        return '''
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script>
        function getUrlVars() {
            var vars = {};
            var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
                vars[key] = value;
            });
            return vars;
        }
        $("#f").attr("action", "/reset_pw?key="+getURLVars()['key']);​)
        </script>
        <form id="f" method="post">
        <input type="text" name="pass" placeholder="New password">
        <input type="submit" value="Set">
        </form>
        '''
@app.route('/success')
def success():
    return render_template('payment_success.html')
@app.route('/cancel')
def cancel():
    return  render_template('payment_cancel.html')
@app.route('/connect_stripe',methods=['GET'])
def connect_stripe():
    stripe.api_key=auth.auth_data['stripe_auth']['secret']
        # Assert the state matches the state you provided in the OAuth link (optional).
    state = request.args.get("state")
    # Send the authorization code to Stripe's API.
    code = request.args.get("code")
    try:
        response = stripe.OAuth.token(grant_type="authorization_code", code=code,)
    except stripe.oauth_error.OAuthError as e:
        return json.dumps({"error": "Invalid authorization code: " + code}), 400
    except Exception as e:
        return json.dumps({"error": "An unknown error occurred."}), 500

    connected_account_id = response["stripe_user_id"]
    def save_account_id(account_id):
        db['advertisers'].update({'user':current_user.username},{'$set':{'stripe_id':account_id}})
    save_account_id(connected_account_id)

    # Render some HTML or redirect to a different page.
    return redirect('/advertiserprofile')
#untested app route, I didn't have a enough time to test yet
#@app.route('/notificationsrequest',methods=['GET'])
#def notificationsrequest():
#    return request.item.notification.render_template()
@app.route('/tw_auth',methods=['POST'])
def tw_auth():
    token = request.get_json()['token']
    secret = request.get_json()['secret']
    try:
        oauth_user = OAuth1Session(client_key=auth.auth_data['tw_auth']['api_key'],
                                client_secret=auth.auth_data['tw_auth']['api_secret'],
                                resource_owner_key=token,
                                resource_owner_secret=secret)
        url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        user_data = oauth_user.get(url_user)
        uname = json.loads(user_data.text)['screen_name']
        db['influencers'].update({'user':current_user.username},{'$set':{'twitter':uname}})
        scraping_workflow.tagTWUser(uname)
        return 'got tw'
    except:
        return 'failed tw', 500
@app.route('/changemail',methods=['POST'])
@login_required
def changemail():
    mail = request.get_json()['email']
    if(db['advertisers'].find_one({'user':current_user.username}) is not None):
        db['advertisers'].update({'user':current_user.username},{'$set':{'email':mail}})
    else:
        db['influencers'].update({'user':current_user.username},{'$set':{'email':mail}})
    return 'good'
@app.route('/changename',methods=['POST'])
@login_required
def changename():
    name = request.get_json()['name']
    if(db['advertisers'].find_one({'user':current_user.username}) is not None):
        db['advertisers'].update({'user':current_user.username},{'$set':{'company':name}})
    else:
        db['influencers'].update({'user':current_user.username},{'$set':{'name':name}})
    return 'good'
@app.route('/changedesc',methods=['POST'])
@login_required
def changedesc():
    desc = request.get_json()['desc']
    if(db['advertisers'].find_one({'user':current_user.username}) is not None):
        db['advertisers'].update({'user':current_user.username},{'$set':{'desc':desc}})
    else:
        db['influencers'].update({'user':current_user.username},{'$set':{'desc':desc}})
    return 'good'
@app.route('/insta_auth',methods=['GET'])
def insta_auth():
    code = request.args.get('code')
    access = requests.post('https://api.instagram.com/oauth/access_token',data={'client_id':auth.auth_data['insta_auth']['app_id'],'client_secret':auth.auth_data['insta_auth']['app_secret'],'code':code,'grant_type':'authorization_code','redirect_uri':'https://127.0.0.1:5000/insta_auth'}).json()
    token = access['access_token']
    uname = requests.get('https://graph.instagram.com/me?fields=username&access_token='+token).json()['username']
    db['influencers'].update({'user':current_user.username},{'$set':{'instagram':uname}})
    scraping_workflow.tagInstaUser(uname)
    return redirect('/influencerprofile')
@app.route('/yt_auth')
def yt_auth():
    auth_code = request.args.get('code')
    data = {'code': auth_code,
            'client_id': auth.auth_data['yt_auth']['client_id'],
            'client_secret': auth.auth_data['yt_auth']['client_secret'],
            'redirect_uri': 'https://127.0.0.1:5000/yt_auth',
            'grant_type': 'authorization_code'}
    r = requests.post('https://oauth2.googleapis.com/token', data=data).json()['access_token']
    inf = requests.get('https://www.googleapis.com/youtube/v3/channels?access_token='+r+'&part=snippet&mine=true').json()
    uid = inf['items'][0]['id']
    uname = inf['items'][0]['snippet']['title']
    db['influencers'].update({'user':current_user.username},{'$set':{'youtube':uid}})
    db['influencers'].update({'user':current_user.username},{'$set':{'yt_display':uname}})
    scraping_workflow.tagYTUser(uid)
    return redirect('/influencerprofile')
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
@app.route('/mobile')
def mobile():
    return render_template('mobile.html')
@app.route('/buildcampaign')
@login_required
def buildcampaign():
    return render_template('buildcampaign.html')
@app.route('/createcampaign', methods=['POST'])
@login_required
def createcampaign():
    desc = request.form['desc']
    #platforms = request.form['platform']
    sess = stripe_payment.payment(request.form['budget'])
    r = Request(
        budget=request.form['budget'],
        link=request.form['link'],
        tags=desc,
        contact=request.form['contact'],
        user='',
        #platforms=platforms,
        author=current_user.username,
        session =sess.id
    )
    db['advertisers'].update({'user':current_user.username},{'$set':{'pending_request':r.get_json()}})
    authorize={'public_key':auth.auth_data['stripe_auth']['public'],'CHECKOUT_SESSION_ID':sess.id}
    return render_template("stripe_payment.html",authori=authorize)
    