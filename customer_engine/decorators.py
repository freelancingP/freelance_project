from functools import wraps
from django.shortcuts import redirect

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Replace this logic with your session-based authentication check
        if "user" in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login")  # Redirect to your login view

    return _wrapped_view