from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect

def host_required(function=None):
    """
    Decorator for views that checks that the user is logged in and is a host,
    redirecting to the home page if necessary.
    """
    def check_is_host(user):
        return user.is_authenticated and user.is_host

    def _wrapped_view(request, *args, **kwargs):
        if check_is_host(request.user):
            return function(request, *args, **kwargs)
        
        if not request.user.is_authenticated:
            return redirect('login')
            
        messages.error(request, "Access denied. You must be a host to view this page.")
        return redirect('home')

    if function:
        return _wrapped_view
    return user_passes_test(check_is_host, login_url='login')
