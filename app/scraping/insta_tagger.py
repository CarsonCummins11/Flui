from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError
webApi = Client(autopatch = True, authenticate = True, username = 'flui.co', password = 'Luv4soccer.1')
userId = 1672949341
# sampleUser = webApi.user_info(user_id = userId)
# print(sampleUser.get('user').get('username'))
sampleUserFeed = webApi.user_feed(user_id = userId, count = 1)
print(sampleUserFeed)