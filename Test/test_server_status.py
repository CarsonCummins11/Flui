import pytest
import requests
def test_website_up():
    r = requests.get('https://www.flui.co')
    assert r.status_code == 200

def test_local_server_up():
    r = requests.get('http://localhost:5000')
    assert r.status_code == 200

def test_local_server_login():
    payload = {'name':'test', 'user':'test', 'pass':'p', 'email':'fake@email.com'}
    r = requests.post('http://localhost:5000/newinfluencer',payload,allow_redirects=True)
    assert r.status_code == 200
test_local_server_up()
test_local_server_login()