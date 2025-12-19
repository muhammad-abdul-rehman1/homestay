
import os
import django
from django.conf import settings
from django.template import Template, Context
from django.template.loader import get_template, render_to_string

print(f"Current working directory: {os.getcwd()}")

file_path = os.path.join(os.getcwd(), 'listings', 'templates', 'listings', 'home.html')
print(f"Checking file at: {file_path}")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print("--- FILE CONTENT START ---")
        # Print only the lines around 57
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if 50 < i < 70:
                print(f"{i+1}: {line}")
        print("--- FILE CONTENT END ---")
except Exception as e:
    print(f"Could not read file: {e}")

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
    # Try to verify syntax
    template = get_template('listings/home.html')
    print("Template syntax is VALID.")
except Exception as e:
    print(f"Template syntax error: {e}")
