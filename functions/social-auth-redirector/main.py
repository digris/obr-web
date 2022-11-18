from flask import redirect

'''
http://local.next.openbroadcast.ch:3000/social/login/google-oauth2/?source=app
https://next.openbroadcast.ch/social/login/google-oauth2/?source=app
'''

def auth_redirect(request):
    print(request.__dict__)
    location = "https://next.openbroadcast.ch/social/login/google-oauth2/?source=app"
    return redirect(location)