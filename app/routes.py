from flask import render_template,request, session,redirect
from app import app,db,User, InfluencerProfile,AdvertiserProfile
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user, login_user

@app.route("/")
def main():
    return render_template('home.html')
@app.route("/newinfluencer",methods=['POST'])
def newinfluencer():
    if db['influencers'].find_one({'user':request.form['user']}) is None and db['advertisers'].find_one({'user':request.form['user']}) is None:
        prof = {'first':request.form['fname'],
        'last':request.form['lname'],
        'user':request.form['user'],
        'pass':generate_password_hash(request.form['pass']),
        'desc':'No Description',
        'email':'No Email',
        'image':'',
        'instagram':'No Instagram',
        'youtube':'No YouTube',
        'twitter':'No Twitter',
        'tags':''}
        db['influencers'].insert_one(prof)
        use = User.User(username=prof['user'])
        login_user(use)
        return redirect('/influencerprofile')
    else:
        return 'That username is in use'
    
@app.route("/newadvertiser",methods=['POST'])
def newadvertiser():
    if db['advertisers'].find_one({'user':request.form['user']}) is None and db['influencers'].find_one({'user':request.form['user']}) is None:
        prof = {'company':request.form['company'],
        'user':request.form['user'],
        'pass':generate_password_hash(request.form['pass']),
        'desc':'No Description',
        'email':'No Email',
        'image':'',
        'tags':''}
        db['advertisers'].insert_one(prof)
        use = User.User(username=prof['user'])
        login_user(use)
        return redirect('/advertiserprofile')
    else:
        return 'That username is in use'

@app.route("/logininfluencer",methods=['POST'])
def logininfluencer():
    prof = db['influencers'].find_one({"user":request.form['user']})
    if prof is None:
        print('no user')
        return redirect('/')
    if(check_password_hash(prof['pass'],request.form['pass'])):
        print('success')
        login_user(User.User(username=request.form['user']))
        return redirect('/influencerprofile')
    print('bad password')
    return redirect('/')
@app.route("/loginadvertiser",methods=['POST'])
def loginadvertiser():
    prof = db['advertisers'].find_one({"user":request.form['user']})
    if prof is None:
        return redirect('/')
    if(check_password_hash(prof['pass'],request.form['pass'])):
        login_user(User.User(username=request.form['user']))
        return redirect('/advertiserprofile')
    return redirect('/')
@app.route("/advertiserprofile")
def advertiserprofile():
    profile = db['advertisers'].find_one({'user':current_user.username})
    return render_template('AdvertiserProfile.html',profile=profile)
@app.route("/influencerprofile")
def influencerprofile():
    profile = db['influencers'].find_one({'user':current_user.username})
    return render_template('InfluencerProfile.html',profile=profile)
@app.route("/advertiserprofilechange",methods=['POST'])
def advertiserprofilechange():
    db['advertisers'].update({'user':current_user.username},{'$set':{"company":request.form['company'],"desc":request.form['desc'],"email":request.form['email']}})
    return redirect('/advertiserprofile')
@app.route("/influencerprofilechange",methods=['POST'])
def influencerprofilechange():
    db['influencer'].update({'user':current_user.username},{'$set':{"first":request.form['fname'],
    "desc":request.form['desc'],"email":request.form['email'],"instagram":request.form['instagram'],
    "youtube":request.form['youtube'],"twitter":request.form['twitter']}})
    return redirect('/influencerprofile')
@app.route("/searchforinfluencers")
def searchforinfluencers():
    return render_template('InfluencerSearch.html')
@app.route("/searchforadvertisers")
def searchforadvertisers():
    return render_template('AdvertiserSearch.html')
@app.route('/getinfluencertags')
def getinfluencertags():
    return db['influencers'].find_one({'user':current_user.username})['tags']
@app.route('/getadvertisertags')
def getadvertisertags():
    return db['advertisers'].find_one({'user':current_user.username})['tags']
@app.route('/submitinfluencertags',methods=['POST'])
def submitinfluencertags():
    tags=request.get_json()['tags']
    db['influencers'].update({'user':current_user.username},{'$set':{'tags':tags}})
    return 'good'
@app.route('/submitadvertisertags',methods=['POST'])
def submitadvertisertags():
    tags=request.get_json()['tags']
    db['advertisers'].update({'user':current_user.username},{'$set':{'tags':tags}})
    return 'good'
@app.route("/advertisersearch", methods=['POST'])
def advertisersearch():
    db['advertisers'].create_index([('tags', 'text')])
    results = db['advertisers'].find({ '$text': { '$search': request.get_json()['term'] } })
    ret = {}
    i = 0
    for k in results:
        ret[str(i)]=AdvertiserProfile.create_from(k)
    return ret if len(ret)>0 else 'No matches for that term :('
@app.route("/influencersearch", methods=['POST'])
def influencersearch():
    db['influencers'].create_index([('tags','text')])
    results = db['influencers'].find({'$text': { '$search': request.get_json()['term'] } })
    ret = {}
    i = 0
    for k in results:
        ret[str(i)]=InfluencerProfile.create_from(k)
    return ret if len(ret)>0 else 'No matches for that term :('