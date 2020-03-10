#Class for a request object
from flask import Flask, render_template
from jinja2 import Environment, BaseLoader
from app import app,db,User,AdvertiserProfile,InfluencerProfile
import yagmail
from app.scraping import tagger

class Request:
	#budget is an integer, media will be some multimedia object(needs to be implemented), description is a string, tags is an array of strings, author is a string
	def __init__(self, budget, link, tags, contact, author,session,user='', r=0):
		self.budget = budget
		self.link = link
		self.tags = tags
		self.contact = contact
		self.author = author
		self.user = user
		self.r = r
		self.session=session
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
	#sends emails to relevant creators
	def sendmail(self):
		t = tagger.Tagger()
		request = {'budget': self.budget, 'description': self.link, 'tags': ' '.join(t.tag(self.tags)), 'author': self.author}
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
			company = db['advertisers'].find_one({'user':self.author})
			yag.send(influencer['email'],'Re: Ad with '+company,'Hi '+influencer['name']+',\nOur partner '+company+' was wondering if you would be willing to run an ad for them? Their request can be found at your account on Flui, which you should have access to from a prior email. We\'re super excited to work with you.\nThanks,\nCarson Cummins\nFounder, Flui')
			db['influencers'].update({'user':influencer['user']},{'$set':{'request':self.get_json()}})
	#Returns the request class as a jinja template
	def get_render_template(self):
		request = self.get_json()
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
				<div class='outbox'style='text-align:center'><div class='textt'>{{request.budget}}</div></div>
				<div class='outbox'style='text-align:center'><div class='textt'>{{request.contact}}</div></div>
				<div class='outbox'style='text-align:center'><div class='textt'>{{request.description}}</div></div>
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