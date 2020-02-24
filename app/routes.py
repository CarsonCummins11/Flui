#routes.py
#routes html requests to python functions
from flask import render_template,request, session,redirect
from app import app,db,User,AdvertiserProfile,InfluencerProfile,tweepy_bot,payment
from app.InfluencerProfile import Influencer
from app.AdvertiserProfile import Advertiser
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user, login_user, login_required
import pickle
from app.request import Request
from jinja2 import Environment, BaseLoader
from urllib.parse import unquote

@app.route("/")
def main(): #returns the home page on start
    return render_template('home.html')
@app.route("/about")
def about(): #returns the about page
    return render_template('about.html')
@app.route("/newinfluencer",methods=['POST'])
def newinfluencer(): #Creates a new influencer with blank information from the request form
    if db['influencers'].find_one({'user':request.form['user']}) is None and db['advertisers'].find_one({'user':request.form['user']}) is None:
        new_influencer = Influencer(
            name = request.form['name'], #NewInfluencer has the tag as 'name', but when you inspect it's still fname?
            username = request.form['user'],
            password = request.form['pass'], #generates hash in __init__()
            email = request.form['email'],
            desc = '',
            img = '',
            insta = '',
            yt = '',
            tw = '',
            tags = ''
        )
        db['influencers'].insert_one(new_influencer.to_dict()) #Adds the profile to db, needs to be a dict
        use = User.User(username=new_influencer.username) #Sets the user to the newly created user
        login_user(use) #Logins in through Flask's LoginManager
        return redirect('/influencerprofile') #Redirects to their profile
    else:
        return 'That username is in use'
    
@app.route("/newadvertiser",methods=['POST'])
def newadvertiser(): #Creates a new advertiser
    if db['advertisers'].find_one({'user':request.form['user']}) is None and db['influencers'].find_one({'user':request.form['user']}) is None:
        new_advertiser = Advertiser(
            username = request.form['user'],
            password = request.form['pass'], #generates hash in __init__()
            desc = '',
            email = '',
            img = ''
        )
        db['advertisers'].insert_one(new_advertiser.to_dict()) #Adds the profile to db, needs to be a dict
        use = User.User(username=new_advertiser.username) #Sets the user to the newly created user
        print(current_user)
        login_user(use)#Logins in through Flask's LoginManager
        print(current_user)
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
    prof = db['advertisers'].find_one({"user":request.form['user']}) #find's an advertiser from db
    if prof is None:
        return redirect('/')
    if(check_password_hash(prof['pass'],request.form['pass'])): #If correct pass, redirect to their profile
        login_user(User.User(username=request.form['user']))
        return redirect('/advertiserprofile')
    return redirect('/')
@app.route("/advertiserprofile")
def advertiserprofile(): #If the user isn't null, then return a rendered template(using Jinja), this is used in rendering to browser
    print(current_user)
    profile = db['advertisers'].find_one({'user':current_user.username})
    print(profile)
    return render_template('AdvertiserProfile.html',profile=profile) 
@app.route("/influencerprofile")
def influencerprofile(): #If the user isn't null, then return a rendered template(using Jinja), this is used in rendering to browser
    profile = db['influencers'].find_one({'user':current_user.username})
    return render_template('InfluencerProfile.html',profile=profile)
@app.route("/advertiserprofilechange",methods=['POST'])
def advertiserprofilechange(): #Changes the current user based on a request form
    db['advertisers'].update({'user':current_user.username},{'$set':{"company":request.form['company'],"desc":request.form['desc'],"email":request.form['email']}})
    return redirect('/advertiserprofile')
@app.route("/influencerprofilechange",methods=['POST'])
def influencerprofilechange(): #Changes the influencer based on a request form
    db['influencers'].update({'user':current_user.username},{'$set':{"name":request.form['fname'],
    "desc":request.form['desc'],"email":request.form['email'],"instagram":request.form['instagram'],
    "youtube":request.form['youtube'],"twitter":request.form['twitter']}})
    return redirect('/influencerprofile')
@app.route("/searchforinfluencers")
def searchforinfluencers(): #Returns the search form for influencers
    return render_template('InfluencerSearch.html')
@app.route("/searchforadvertisers")
def searchforadvertisers(): #Returns the search form for advertisers 
    return render_template('AdvertiserSearch.html')
@app.route('/getinfluencertags')
def getinfluencertags(): #returns the tags of an influencer
    return db['influencers'].find_one({'user':current_user.username})['tags']
@app.route('/getadvertisertags')
def getadvertisertags(): #returns the tags of an advertiser
    return db['advertisers'].find_one({'user':current_user.username})['tags']
@app.route('/submitinfluencertags',methods=['POST'])
def submitinfluencertags(): #Get's tags from the form, parses to json, and sets the influencers tags
    tags=request.get_json()['tags']
    db['influencers'].update({'user':current_user.username},{'$set':{'tags':tags}})
    return 'good'
@app.route('/submitadvertisertags',methods=['POST'])
def submitadvertisertags():#Get's tags from the form, parses to json, and sets the advertisers tags
    tags=request.get_json()['tags']
    db['advertisers'].update({'user':current_user.username},{'$set':{'tags':tags}})
    return 'good'
@app.route("/advertisersearch", methods=['POST'])
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
def influencersearch(): #Creates an array of influencers that match a tag and returns it
    db['influencers'].create_index([('tags','text')])
    results = db['influencers'].find({'$text': { '$search': request.get_json()['term'] } })
    ret = {}
    i = 0
    for k in results:
        ret[str(i)]=InfluencerProfile.create_from(k) #Adds influencers's rendered template to a list(something that can be outputed to a webpage)
        i+=1
    return ret if len(ret)>0 else 'no matches for term:(' #Returns the results
@app.route("/createrequest", methods=['POST'])
def create_request(): #Creates a request object from a form submission
    r = Request(
        budget=request.form['budget'],
        link=request.form['note'],
        tags=unquote(request.args.get('tags')),
        contact=request.form['contact'],
        author=current_user.username
    )
    db['influencers'].update({'user':current_user.username},{'$push':{'request':r.get_json()}})
    r.sendmail()
    return redirect('/advertiserprofile')
@app.route("/adwithgroup")
def adwithgroup():
    return render_template('buygroup.html')
@app.route("/viewrequest")
def viewrequest():
    prof = db['influencers'].find_one({'user':request.args.get('user')})['request']
    if type(prof) is not dict:
        prof = prof[int(request.args.get('r'))]
    r= Request(
        budget=prof['budget'],
        link=prof['link'],
        tags=prof['tags'],
        contact=prof['contact'],
        author=prof['author'],
        user=request.args.get('user'),
        r=int(request.args.get('r'))
    )
    return r.get_render_template()
@app.route("/viewadvertiserprofile")
def viewadvertiserprofile():
    prof = db['advertisers'].find_one({'user':request.args.get('user')})
    return render_template('StaticAdvertiser.html',profile=prof)
@app.route("/viewinfluencerprofile")
def viewinfluencerprofile():
    prof = db['influencers'].find_one({'user':request.args.get('user')})
    return render_template('StaticInfluencer.html',profile=prof)
@app.route('/submitad',methods=['POST'])
def submitad():
    link = request.form['link']
    db['influencers'].update({'user':current_user.username},{'$push':{'link':link}})
    adnumber = request.args.get('r')
    payment.paypal_payment(
        #get user paypal and amount to be paid here
    )