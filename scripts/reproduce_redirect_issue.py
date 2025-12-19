import os
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()

def test_login_redirect():
    print("Starting login redirect test...")
    
    # Clean up previous test user
    User.objects.filter(email='redirect_test@example.com').delete()
    
    # Create an active user
    user = User.objects.create_user(
        username='redirect_test',
        email='redirect_test@example.com',
        password='password123'
    )
    user.is_active = True
    user.save()
    
    client = Client()
    
    # Target URL to redirect to
    next_url = '/listing/1/'
    
    print(f"Attempting login with next={next_url}")
    
    # Post to login with next parameter
    # Note: The next parameter is usually in GET for the form display, 
    # but validation might look for it in POST or GET depending on implementation.
    # Typically, the login template renders it as a hidden field or the action URL includes it.
    # For now, let's try sending it in POST data (common if hidden field) AND query string.
    
    login_url = reverse('login') + f'?next={next_url}'
    response = client.post(login_url, {
        'email': 'redirect_test@example.com',
        'password': 'password123',
        'next': next_url # Try passing as data too
    })
    
    if response.status_code == 302:
        print(f"Redirect location: {response.url}")
        if response.url == next_url:
            print("PASS: Redirected to next_url")
        elif response.url == reverse('home'):
            print("FAIL: Redirected to home")
        else:
            print(f"FAIL: Redirected to unexpected location: {response.url}")
    else:
        print(f"FAIL: Expected redirect (302), got {response.status_code}")

if __name__ == '__main__':
    test_login_redirect()
