from jinja2 import Environment, BaseLoader
from werkzeug.security import generate_password_hash

#Creates a Jinja template from an advertiser profile object
#'Loaders are responsible for loading templates from a resource such as the file system.'
#This code uses the BaseLoader, which is the base class for every loader
def create_from(profile):
 #String for the Jinja template
    template='''
    <link href="https://fonts.googleapis.com/css?family=Montserrat:100i&display=swap" rel="stylesheet">
        <style>
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
    .clickbox{
        display:inline-block;
        text-align:left;
        border-radius:25px;
        box-shadow: 0px 3px 7px DarkGrey;
        cursor:pointer;
        margin-top:20px;
    }
    .clickbox:focus, .clickbox:active, .clickbox.active, .clickbox:focus:active {
        -webkit-box-shadow: none;
        box-shadow: none;
    }
    </style>
    <div class=clickbox>
        <div class='nametext'>{{profile.first}}</div>
        <div class='text'>
            <img style="width:1vw;height:1vw;" src="/static/images/Instagram_Logo.png">{{profile.instagram}}
            <img style="width:1vw;height:1vw;" src="/static/images/Twitter_Logo.png">{{profile.twitter}}
            <img style="width:1.4vw;height:1vw;" src="/static/images/Youtube_Logo.png">{{profile.youtube}}
        </div>
        <div class='text'>{{profile.desc}}</div>
    </div>
    '''
    rtemplate = Environment(loader=BaseLoader).from_string(template) #Creates a Jinja template from a string
    return rtemplate.render(profile=profile) #Returns rendered template(as a unicode string)

class Influencer:
    #insta, yt, tw, etc can be usernames used in the apis
    def __init__(self, name, username, password, desc, email, img, insta, yt, tw, tags): #when initializing just Influencer(name="name") and you can leave the others blank
        self.name = name
        self.username = username
        self.password = generate_password_hash(password)
        self.desc = desc
        self.email = email
        self.img = img
        self.insta = insta
        self.yt = yt
        self.tw = tw #This has to be their twitter handle
        self.tags = tags
        self.engagement_ratio_tw = 0
    def to_dict(self):
        return {
            "name": self.name,
            "user": self.username,
            "pass": self.password, #hashed in __init__() of course
            "description": self.desc,
            "email": self.email,
            "img": self.img,
            "insta": self.insta,
            "yt": self.yt,
            "tw": self.tw, #This has to be their twitter handle
            "tags": self.tags,
            "engagement_ratio": 0 #change to this later -> self.engagement_ratio
        }

