import os
import django
from django.test import Client
from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()

# Override email backend to capture emails
from django.conf import settings
settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

def verify_email_flow():
    print("Starting email verification flow test...")
    
    # Clean up previous test user
    User.objects.filter(email='test@example.com').delete()
    User.objects.filter(username='testuser').delete()
    
    client = Client()
    
    # 1. Register a new user
    print("1. Registering new user...")
    response = client.post(reverse('signup'), {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    if response.status_code != 302:
        print(f"Registration failed with status {response.status_code}")
        return
        
    user = User.objects.get(email='test@example.com')
    if user.is_active:
        print("FAIL: User should be inactive after registration")
        return
    else:
        print("PASS: User is inactive after registration")
        
    # 2. Check email
    print("2. Checking for activation email...")
    if len(mail.outbox) == 0:
        print("FAIL: No email sent")
        return
        
    email = mail.outbox[0]
    if 'Activate your account' not in email.subject:
        print(f"FAIL: Unexpected email subject: {email.subject}")
        return
        
    print("PASS: Activation email sent")
    
    # Extract activation link (simplified extraction)
    body = email.body
    start_index = body.find('http://')
    end_index = body.find('\n', start_index)
    activation_link = body[start_index:end_index].strip()
    
    print(f"Activation link: {activation_link}")
    
    # 3. Activate account
    print("3. Activating account...")
    # Parse the URL to get the path
    from urllib.parse import urlparse
    path = urlparse(activation_link).path
    
    response = client.get(path)
    
    if response.status_code != 302:
        print(f"Activation failed with status {response.status_code}")
        return
        
    user.refresh_from_db()
    if not user.is_active:
        print("FAIL: User should be active after activation")
        return
    else:
        print("PASS: User is active after activation")

    print("Email verification flow verified successfully!")

if __name__ == '__main__':
    verify_email_flow()
