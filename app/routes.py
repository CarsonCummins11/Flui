#routes.py
#routes html requests to python functions
from flask import render_template,request, session,redirect
from app import app,db,User, InfluencerProfile,AdvertiserProfile
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user, login_user

@app.route("/")
def main(): #returns the home page on start
    return render_template('home.html')
@app.route("/about")
def about(): #returns the about page
    return render_template('about.html')
@app.route("/newinfluencer",methods=['POST'])
def newinfluencer(): #Creates a new influencer with blank information from the request form
    if db['influencers'].find_one({'user':request.form['user']}) is None and db['advertisers'].find_one({'user':request.form['user']}) is None:
        prof = {'first':request.form['fname'],
        'last':request.form['lname'],
        'user':request.form['user'],
        'pass':generate_password_hash(request.form['pass']), #generates password hash from entered password
        'desc':'No Description',
        'email':'No Email',
        'image':'', #file path?
        'instagram':'No Instagram',
        'youtube':'No YouTube',
        'twitter':'No Twitter',
        'tags':''} #Does python have enums? We could use enums for tags
        db['influencers'].insert_one(prof) #Adds the profile to db
        use = User.User(username=prof['user']) #Sets the user to the newly created user
        login_user(use) #Logins in through Flask's LoginManager
        return redirect('/influencerprofile') #Redirects to their profile
    else:
        return 'That username is in use'
    
@app.route("/newadvertiser",methods=['POST'])
def newadvertiser(): #Creates a new advertiser
    if db['advertisers'].find_one({'user':request.form['user']}) is None and db['influencers'].find_one({'user':request.form['user']}) is None:
        prof = {'company':request.form['company'], #create a profile object from the request form
        'user':request.form['user'],
        'pass':generate_password_hash(request.form['pass']),
        'desc':'No Description',
        'email':'No Email',
        'image':'',#file path
        'tags':''}#Does python have enums? We could use enums for tags
        db['advertisers'].insert_one(prof) #Adds the profile to db
        use = User.User(username=prof['user']) #Sets the user to the newly created user
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
    prof = db['advertisers'].find_one({"user":request.form['user']}) #find's an advertiser from db
    if prof is None:
        return redirect('/')
    if(check_password_hash(prof['pass'],request.form['pass'])): #If correct pass, redirect to their profile
        login_user(User.User(username=request.form['user']))
        return redirect('/advertiserprofile')
    return redirect('/')
@app.route("/advertiserprofile")
def advertiserprofile(): #If the user isn't null, then return a rendered template(using Jinja), this is used in rendering to browser
    profile = db['advertisers'].find_one({'user':current_user.username})
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
    db['influencers'].update({'user':current_user.username},{'$set':{"first":request.form['fname'],
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
    return ret if len(ret)>0 else 'No matches for that term :(' #Returns the results
@app.route("/influencersearch", methods=['POST'])
def influencersearch(): #Creates an array of influencers that match a tag and returns it
    db['influencers'].create_index([('tags','text')])
    results = db['influencers'].find({'$text': { '$search': request.get_json()['term'] } })
    ret = {}
    i = 0
    for k in results:
        ret[str(i)]=InfluencerProfile.create_from(k) #Adds influencers's rendered template to a list(something that can be outputed to a webpage)
    return ret if len(ret)>0 else 'No matches for that term :(' #Returns the results
@app.route("/adwithgroup")
def adwithgroup():
    return render_template('buygroup.html')
@app.route("/buygroup", methods=['POST'])
def buygroup():
    k = request.form['budget']
    return redirect('/advertiserprofile')