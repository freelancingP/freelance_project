from functools import wraps
from django.shortcuts import redirect
import urllib.request
import urllib.parse
 
from twilio.rest import Client

def send_sms(request):

    account_sid = 'AC954f796095e63724d29cb5bc17b5c0df'
    auth_token = '[AuthToken]'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        to='+918299037804'
    )

    print(message.sid)
    return message.sid


    
def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Replace this logic with your session-based authentication check
        if "user" in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login")  # Redirect to your login view

    return _wrapped_view