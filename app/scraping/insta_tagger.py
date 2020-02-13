from app.scraping.authentication.auth import auth_data
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError

webApi = Client(autopatch = True, authenticate = True, username = auth_data['insta_auth']['username'], password = auth_data['insta_auth']['username'])
userId = auth_data['insta_auth']["id"]

# sampleUser = webApi.user_info(user_id = userId)
# print(sampleUser.get('user').get('username'))

sampleUserFeed = webApi.user_feed(user_id = userId, count = 1)
print(sampleUserFeed)