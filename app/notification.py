#Class for a request object
from flask import Flask, render_template
from jinja2 import Environment, BaseLoader
from app import app,db,User,AdvertiserProfile,InfluencerProfile
import uuid

class Notification:
    # IMPORTANT: How to use this object
    #
    # When creating a notification from an ad request, collab request, or 'try checking out this creator', it needs five things passed in a json object:
    #
    # {
    #     'title': title, <- title of the notification
    #     'img': img, <- the icon to be used in the notification(think youtube-style notification), this is a link to an image
    #     'author': author, <- what advertiser/collaborator does it come from(it could also come from us, flui, set it None if it is)
    #     'message': msg, <- what the notification says(keep it short)
    #     'link': link, <- this is the link to the request/creator page
    #     'target-user': user <- notifications are tied to a specific user
    # }
    #
    # How to create notification object:
    #
    # notification has variables passed into it, default null, so that you can specify which type of notification it is, ie, if it's an ad request, collab request, 'check out this creator', a message, or announcement
    #
    # if you have an ad request, you would convert this into a notification object like this:
    #
    # n = Notification(type_request={
    #     'title': title,
    #     'img': img,
    #     'author': author,
    #     'message': msg,
    #     'link': link,
    #     'target-user': user
    # })
    #
    # In order to change what type of notification you create, change what variable you pass in through, so if you wanted to create a personal message, change 'type_request' when passing to the constructor to 'type_pm'
    # Don't set two types of requests because it will only take one
    # Also, when you create the object with a target user, it will automatically deliver the notification to them
    #
    # type_request = specifies an ad request type
    # type_collab = specifies a request for a collab
    # type_checkout_creator = this is like a 'hey this is someone you might want to collab with'
    # type_pm = personal message
    # type_announcement = official Flui announcement(with great power comes great responsibility)
    def __init__(self, type_request=None, type_collab=None, type_checkout_creator=None, type_pm=None, type_announcement=None): 
        params = locals()
        for p in params: #iterates over the parameters, it will set the obj based on which one isn't null
            if not p == None:
                self.obj = p
                #This sets the text for the type of notification
                self.obj['template-header'] = '<p class="notif" style="font-size:10px; color: #696969; margin-top:3px;margin-bottom: -24px;padding-bottom:0px;margin-left: -32px;">'
                if params.index(p) == 0: self.obj['template-header'] = self.obj['template-header'] + 'Ad Request</p>'
                elif params.index(p) == 1: self.obj['template-header'] = self.obj['template-header'] + 'Collaboration</p>'
                elif params.index(p) == 2: self.obj['template-header'] = self.obj['template-header'] + 'Check this out</p>'
                elif params.index(p) == 3: self.obj['template-header'] = self.obj['template-header'] + 'Message</p>'
                elif params.index(p) == 4: self.obj['template-header'] = self.obj['template-header'] + 'Announcement</p>'
                break
        #sets up id and read variable
        if self.obj != None:
            self.obj['read'] = False
            self.obj['id'] = uuid.uuid1()
        #sets the default profile pic
        if self.obj != None and self.obj['img'] == None:
            self.obj['img'] = '/static/images/default_profile_image.png'

        target_user=db['influencers'].find_one({'user':self.obj['target-user']})
        target_user.notifications.append(self.obj)

    def get_json(self):
        return self.obj
	
    #Returns the request class as a jinja template
    def get_render_template(self):
        #Jinja Template for request as a string
        template = '''
            <hr />''' + self.obj['template-header'] + '''
            <img id="notif-img" src="''' + self.obj['img']+'''" width="25px" height="25px" style="margin-bottom:3px;vertical-align: middle;">
            <span class="notif" style="font-size:17px;margin-bottom:3px;">''' + self.obj['message'] + '''</span>
            <hr />
        '''
        rtemplate = Environment(loader=BaseLoader).from_string(template) 
        return rtemplate.render()