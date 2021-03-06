#Class for a request object
from flask import Flask, render_template
from jinja2 import Environment, BaseLoader
from app import app,db,User,AdvertiserProfile,InfluencerProfile,notification
import yagmail
from app.scraping import tagger
from flask_login import current_user

class Request:
	#budget is an integer, media will be some multimedia object(needs to be implemented), description is a string, tags is an array of strings, author is a string
	def __init__(self, budget, link, tags, contact, author,session,platforms=[],user='', r=0):
		self.budget = budget
		self.link = link
		self.tags = tags
		self.contact = contact
		self.author = author
		self.user = user
		self.r = r
		self.session=str(session)
	def get_json(self):
		return {
			'budget':self.budget,
			'link':self.link,
			'tags':self.tags,
			'contact':self.contact,
			'author':self.author,
			'user':self.user,
			'r':self.r,
			'session':self.session
		}
	@staticmethod
	def from_json(f):
		return Request(budget=f['budget'],link=f['link'],tags=f['tags'],contact=f['contact'],author=f['author'],user=f['user'],r=f['r'],session=f['session'])
	#sends emails to relevant creators
	def sendmail(self):
		print('in sendmail')
		t = tagger.Tagger()
		request = {'budget': self.budget, 'description': self.link, 'tags': ' '.join(t.tag(self.tags.split(' '))['plain']), 'author': self.author}
		yag = yagmail.SMTP('carson@flui.co', 'Luv4soccer.1')
		db['influencers'].create_index([('tags','text')])
		results = db['influencers'].find({'$text': { '$search': request['tags'] } })
		def countofterms(val):
			count = 0
			for k in self.tags:
				if k in val['votes'].keys():
					count+=val['votes'][k]
			return count
		results = list(results)
		results.sort(key=countofterms,reverse=True)
		budget_used = 0
		for influencer in results:
			infcost = InfluencerProfile.Influencer.from_dict(influencer).findCost()
			budget_used+=infcost
			if(budget_used>self.budget):
				break
			company = db['advertisers'].find_one({'user':self.author})['company']
			yag.send(influencer['email'],'Re: Ad with '+company,'Hi '+influencer['name']+',\nOur partner '+company+' was wondering if you would be willing to run an ad for them? Their request can be found at your account on Flui, which you should have access to from a prior email. We\'re super excited to work with you.\nThanks,\nCarson Cummins\nFounder, Flui')
			db['influencers'].update({'user':influencer['user']},{'$push':{'request':self.get_json()}})
			'''db['influencers'].update({'user':influencer['user']},{'$push':{'notifications':
			notification.Notification(type_request={
				'title':company+' Ad Request',
				'img':db['advertisers'].find_one({'user':self.author})['img'],
				'author':company,
				'message':"New ad request!",
				'link':"link",
				'target-user':influencer['user']
			}).get_render_template()
			}})'''
	#Returns the request class as a jinja template
	def get_render_template(self):
		request = self.get_json()
		request['cost'] = InfluencerProfile.Influencer.from_dict(db['influencers'].find_one('user',current_user.username)).findCost()
		advertiser=db['advertisers'].find_one({'user':self.author})
		#Jinja Template for request as a string
		template = '''
		<html>
			<head>
			<link href="https://fonts.googleapis.com/css?family=Montserrat:100i&display=swap" rel="stylesheet">
			<style>
			body{
				font-size:123px;
				background-image: url("/static/images/adback.png");
            	background-position: center center;
			}
			.nametext{
				font-family: 'Montserrat', sans-serif;
				font-weight: 100;
				color:#707070;
				font-size: 100%;
				padding-left:8px;
			}
			.text{
				font-family: 'Montserrat', sans-serif;
				font-weight: 100;
				color:#707070;
				font-size: 25%;
				padding-left:14px;
			}
			.textt{
				font-family: 'Montserrat', sans-serif;
				font-weight: 100;
				color:#707070;
				font-size: 25%;
				padding-left:0px;
			}
			.clickbox{
				text-align:left;
				border-radius:25px;
				cursor:pointer;
				margin-top:-80px;
				width:120%;
				background-color:white;
			}
			.clickbox:focus, .clickbox:active, .clickbox.active, .clickbox:focus:active {
				-webkit-box-shadow: none;
				box-shadow: none;
			}
			.half{
				position: relative;
				top: 50%;
				transform: translateY(-50%);
			}
			.outbox{
				font-family: 'Montserrat', sans-serif;
				border: 2px solid #707070be;
				color: #547B7B7B;
				padding: 8px 100px;
				font-size: 80px;
				margin-top:70px;
				border-radius: 50px;
				text-align:center;
				font-style: italic;
				box-shadow: 0px 3px 6px darkgray; 
			}
			h1{
				font-family: 'Montserrat', sans-serif;
				color:white;
				font-style:italic;
				text-align:left;
				background:#212121;
				font-size: 70px;
				margin-top: -10px;
				margin-right:-10px;
				margin-left:-10px;
				margin-bottom: 0px;
				padding: -5px;
				font-weight:100;
				box-shadow: 0px 12px 17px  #707070;
    		}
			.proflabel{
				font-size:30%;
				padding:0;
				font-weight: 100;
				margin-right:0;
			}
			.arrow{
				position:absolute;
				top:50%;
				right:1%;
				color: #707070be;
				font-size:50px;
				cursor:pointer;

			}
			.arrowleft{
				transform: rotate(180deg);
				position:absolute;
				top:50%;
				left:1%;
				color: #707070be;
				font-size:50px;
				cursor:pointer;
			}
			.inp{
				font-family: 'Montserrat', sans-serif;
				font-weight: 100;
				color:#707070;
				font-size: 25%;
				padding-left:0px;
				width:100%;
				boder:none;
			}
			</style>
			</head>
			<body>
			<h1>
				<span style="cursor:pointer;" onclick="window.location.href = '/'">Flui</span>
				<span class="proflabel">Ad Request</span>
			</h1>
			<div class="half" style="float:left; margin-left:7vw">
		'''+ AdvertiserProfile.create_from_plain(advertiser)+'''
			</div>
			<div style="float:right;margin-right:15vw; margin-top:70px;">
				<div class='outbox'style='text-align:center'><div class='textt'>{{request.cost}}</div></div>
				<div class='outbox'style='text-align:center'><div class='textt'>{{request.contact}}</div></div>
				<div class='outbox'style='text-align:center'><div class='textt'>{{request.link}}</div></div>
				<form action="/submitad?r={{request.r}}" method="post">
					<div class='outbox'style='text-align:center'><input name='link' class='inp' style='text-align:center' type='text' placeholder='Link to ad'></input></div>
					<div class='outbox'style='text-align:center'><input class='inp' value='submit' type='submit' style='text-align:center'></input></div>
				</form>
			</div>
			</body>
			<div class="arrow" onclick="window.location.href = '/viewrequest?user={{request.user}}&r={{request.r+1}}'">&#9655</div>
			<div class="arrowleft" onclick="window.location.href = '/viewrequest?user={{request.user}}&r={{request.r-1}}'">&#9655</div>
		</html>
		'''
		rtemplate = Environment(loader=BaseLoader).from_string(template) 
		return rtemplate.render(request=request)
	def get_render_template_complete(self):
		template = '''
<!DOCTYPE html>
<html>
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:100i&display=swap" rel="stylesheet">
    <style>
        body{
            font-family: 'Montserrat', sans-serif;
            font-weight: 100;
            color:#707070;
            font-size: 5vw;
            text-align:center;
            overflow-x: hidden;
            background-image: url("/static/images/adback.png");
            background-position: center center;
        }
        h1{
        font-family: 'Montserrat', sans-serif;
        color:white;
        font-style:italic;
        text-align:left;
        background:#212121;
        font-size: 70px;
        margin-top: -10px;
        margin-right:-10px;
        margin-left:-10px;
        margin-bottom: 0px;
        padding: -5px;
        font-weight:100;
        }
        input{
            font-family: 'Montserrat', sans-serif;
            border: 2px solid white;
            color: white;
            padding: 8px 16px;
            font-size: 16px;
            border-radius: 50px;
            text-align:center;
            font-style: italic;
            float:center;
            background-color: transparent;
        }
        .proflabel{
        font-size:30%;
        padding:0;
        font-weight: 100;
       
        margin-right:0;
    }
    </style>
    <body>
        <h1>
            <span style="cursor:pointer;float:left" onclick="window.location.href = '/'">Flui</span>
            <span class="proflabel">Message</span>
        </h1>
        <br>
        <br>
        This ad has already been completed.
    </body>
</html>
		'''
		rtemplate = Environment(loader=BaseLoader).from_string(template) 
		return rtemplate.render()