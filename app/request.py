#Class for a request object
from flask import Flask, render_template
from jinja2 import Environment, BaseLoader
from app import app,db,User
import yagmail

class Request:
	emailbody='''
	Hi {{creator.first}}!

	I’m writing to let you know that you were recently requested to run an ad! For some more info, you can view the request <a href="https://flui.co/viewrequest?co={{request.author}}">here</a>. If you’re interested in running this ad, click <a href="https://flui.co/acceptrequest?co={{request.author}}&in={{creator.user}}">this link</a>. If you accept, we would love to see your ad within the week! Thanks so much for working with us,
	
	Carson Cummins

	Founder, Flui

	'''
	#budget is an integer, media will be some multimedia object(needs to be implemented), description is a string, tags is an array of strings, author is a string
	def __init__(self, budget, media, description, tags, contact, author):
		self.budget = budget
		self.media = media
		self.description = description
		self.tags = tags
		self.contact = contact
		self.author = author
	#sends emails to relevant creators
	def sendmail(self):
		request = {'budget': self.budget, 'media': self.media, 'description': self.description, 'tags':self.tags, 'author': self.author}
		db['influencers'].create_index([('tags','text')])
		results = db['influencers'].find({'$text': { '$search': request.get_json()['term'] } })
		rtemplate = Environment(loader=BaseLoader).from_string(emailbody)
		yag = yagmail.SMTP('carson@flui.co',oauth2_file="../credentials.json")
		for creator in results:
			yag.send(
			to=creator['email'],
			subject="Flui Advertising Request",
			contents=rtemplate.render(request=request,creator=creator)
			)
	#Returns the request class as a jinja template
	def get_render_template(self):
		request = {'budget': self.budget, 'media': self.media, 'description': self.description, 'tags':self.tags, 'author': self.author}
		#Might want to change this template in the future, it's just a skeleton of viewing a request object
		#Jinja Template for request as a string
		template = '''
			<style>
			.nametext{
				font-family: 'Montserrat', sans-serif;
				font-weight: 100;
				color:#707070;
				font-size: 100%;
			}
			.text{
				font-family: 'Montserrat', sans-serif;
				font-weight: 100;
				color:#707070;
				font-size: 25%;
			}
			</style>
			<div style="display:inline-block;text-align:left;">
				<div class='nametext'>{{request.author}}</div>
				<div class='text'>{{request.contact}}</div>
				<div class='text'>{{request.budget}}</div>
				<div class='text'>{{request.description}}</div>
				<div class='text'>{{', '.join(request.tags)}}</div>
			</div>
		'''
		rtemplate = Environment(loader=BaseLoader).from_string(template) 
		return rtemplate.render(request=request)