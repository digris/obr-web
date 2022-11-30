from flask import redirect

def auth_redirect(request):
    print(request.__dict__)
    location = "https://next.openbroadcast.ch/social/login/google-oauth2/?source=app"
    return redirect(location)