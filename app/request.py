#Class for a request object
from flask import Flask, render_template
from jinja2 import Environment, BaseLoader
from app import app,db,User,AdvertiserProfile
import yagmail

class Request:
	#budget is an integer, media will be some multimedia object(needs to be implemented), description is a string, tags is an array of strings, author is a string
	def __init__(self, budget, link, tags, contact, author):
		self.budget = budget
		self.link = link
		self.tags = tags
		self.contact = contact
		self.author = author
	def get_json(self):
		return {
			'budget':self.budget,
			'link':self.link,
			'tags':self.tags,
			'contact':self.contact,
			'author':self.author
		}
	#sends emails to relevant creators
	def sendmail(self):
		request = {'budget': self.budget, 'description': self.link, 'tags':self.tags, 'author': self.author}
		db['influencers'].create_index([('tags','text')])
		results = db['influencers'].find({'$text': { '$search': self.tags } })
		for influencer in results:
			db[influencer['user']].insert_one({'request': self.get_json()})
	#Returns the request class as a jinja template
	def get_render_template(self):
		request = {'budget': self.budget, 'description': self.link, 'tags':self.tags, 'author': self.author}
		advertiser=db['advertisers'].find_one({'username':self.author})
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
			<div style="float:right;">
		'''+ AdvertiserProfile.create_from(advertiser)+'''
			</div>
			<div style="float:right; display:inline-block;text-align:left;">
				<div class='text'>{{request.budget}}</div>
				<div class='text'>{{request.contact}}</div>
				<div class='text'>{{request.description}}</div>
			</div>
		'''
		rtemplate = Environment(loader=BaseLoader).from_string(template) 
		return rtemplate.render(request=request)