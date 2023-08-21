from functools import wraps
from django.shortcuts import redirect
import urllib.request
import urllib.parse
 
# def sendSMS(numbers):
#     apikey = "Mzg0YjM4NmE2OTY3NzI1ODQ3NjI1MTMwNmUzNTY4NzI="
#     data = urllib.parse.urlencode({
#         'apikey': apikey,
#         'numbers': numbers,
#         'message': "Your message content here",
#         'sender': "Manish"
#     })
#     data = data.encode('utf-8')

#     request = urllib.request.Request("https://api.textlocal.in/send")
#     request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')

#     f = urllib.request.urlopen(request, data)
#     fr = f.read().decode('utf-8')
#     print(fr)
#     return fr

def sendSMS(numbers):
    apikey = "Mzg0YjM4NmE2OTY3NzI1ODQ3NjI1MTMwNmUzNTY4NzI="
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': str(829903), 'sender': "Manish", 'format': 'json'})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/")
    
    try:
        with urllib.request.urlopen(request, data) as f:
            response = f.read().decode('utf-8')
            print(response)
            return response
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e)
        return None



    
def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Replace this logic with your session-based authentication check
        if "user" in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login")  # Redirect to your login view

    return _wrapped_view