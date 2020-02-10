from jinja2 import Environment, BaseLoader
#Creates a Jinja template from an advertiser profile object
#'Loaders are responsible for loading templates from a resource such as the file system.'
#This code uses the BaseLoader, which is the base class for every loader
def create_from(profile):
 #String for the Jinja template
    template='''
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