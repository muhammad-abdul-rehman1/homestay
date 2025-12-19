
import os
import django
from django.conf import settings
from django.template import Template, Context
from django.template.loader import get_template

# Configure Django settings explicitly
if not settings.configured:
    settings.configure(
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.getcwd(), 'listings', 'templates')],
            'APP_DIRS': True,
        }],
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth', 
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'listings',
        ],
        BASE_DIR=os.getcwd(),
    )
    django.setup()

try:
    # Try to load the template
    template = get_template('listings/home.html')
    print("Template syntax is valid.")
except Exception as e:
    print(f"Template syntax error: {e}")
