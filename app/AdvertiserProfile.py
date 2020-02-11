from jinja2 import Environment, BaseLoader
from werkzeug.security import generate_password_hash

#Creates a Jinja template from an advertiser profile object
#'Loaders are responsible for loading templates from a resource such as the file system.'
#This code uses the BaseLoader, which is the base class for every loader
def create_from(profile):
    template=''' #Jinja Template for Advertiser as a string
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
        <div class='nametext'>{{profile.company}}</div>
        <div class='text'>{{profile.desc}}</div>
    </div>
    '''
    rtemplate = Environment(loader=BaseLoader).from_string(template) #Creates the Jinja template object for an advertiser from the string 'template'
    return rtemplate.render(profile=profile) #Returns rendered template(as a unicode string)

class Advertiser():
    def __init__(self, username, password, desc, email, img, insta, yt, tw, tags): #when initializing just Influencer(name="name") and you can leave the others blank
        self.username = username
        self.password = generate_password_hash(password)
        self.desc = desc
        self.email = email
        self.img = img
        self.tags = tags