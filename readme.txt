how to run:
    1. run the setup batch file appropriate for your device
    2. open command prompt in the project directory 
    3. run the command python3 -m flask run
    4. go to the link displayed in command prompt

Code Overview:

Diagram:
 _______          _____________           _________
|MongoDB| <----- |Python3/Flask| <------ |JS/JQuery|
|_______| -----> |_____________| ------> |_________|

Backend - 
    matcher.py starts the code by importing everything in the app folder into the python run environment. 
    __init__.py is the next thing run, it's run by the import in matcher.py. It does stuff like start the database connection, and just set up the website in general
    routes.py is the main portion of the backend. Under each route (denoted by @app.route('the url')), the backend takes a specific action, like adding to the database or returning some html
    advertiserprofile.py and InfluencerProfile.py are both basically just an easier way for me to render search results
    User.py represents the user agent for when someone logs in on the website
Frontend - 
    home.html is the most complex. Basically, when one of the buttons is clicked (there's 4 - the new user and login buttons), a javascript funtion replaces the relevant html with html from the static/html folder
    Everything else is pretty simple, but this whole doc needs more stuff so just add what you can
