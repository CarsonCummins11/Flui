#Class for a request object
from flask import Flask, render_template

class Request:
	#budget is an integer, media will be some multimedia object(needs to be implemented), description is a string, tags is an array of strings, author is a string
	def __init__(self, budget, media, description, tags, contact, author):
		self.budget = budget
		self.media = media
		self.description = description
		self.tags = tags
		self.contact = contact
		self.author = author
	
	#Returns the request class as a jinja template
	def get_render_template(self):
		request = {'budget': self.budget, 'media': self.media, 'description': self.description, 'tags':tags, 'author': author}
		#Might want to change this template in the future, it's just a skeleton of viewing a request object
		template = ''' #Jinja Template for request as a string
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
				<div class='nametext'>{{self.author}}</div>
				<div class='text'>{{self.contact}}</div>
				<div class='text'>{{self.budget}}</div>
				<div class='text'>{{self.description}}</div>
				<div class='text'>{{', '.join(tags)}}</div>
			</div>
		'''
		rtemplate = Environment(loader=BaseLoader).from_string(template) 
		return rtemplate