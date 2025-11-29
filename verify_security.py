import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def verify():
    print("Verifying Security Settings...")
    
    # Check Secrets
    if settings.SECRET_KEY == 'django-insecure-rae2f%uus9%0wzr!$80*zc_tdo9x4(4!o15r-+e+vf+@1*)nzy':
        print("[PASS] SECRET_KEY is loaded from env (matches dev default in .env)")
    else:
        print(f"[FAIL] SECRET_KEY mismatch: {settings.SECRET_KEY[:5]}...")

    if settings.DEBUG is True:
        print("[PASS] DEBUG is True (matches dev default in .env)")
    else:
        print(f"[FAIL] DEBUG is {settings.DEBUG}")

    # Check Stripe Keys
    if settings.STRIPE_PUBLIC_KEY and settings.STRIPE_PUBLIC_KEY.startswith('pk_test'):
        print("[PASS] STRIPE_PUBLIC_KEY loaded")
    else:
        print("[FAIL] STRIPE_PUBLIC_KEY missing or invalid")

    if settings.STRIPE_WEBHOOK_SECRET:
        print("[PASS] STRIPE_WEBHOOK_SECRET loaded")
    else:
        print("[FAIL] STRIPE_WEBHOOK_SECRET missing")

    print("\nVerification Complete.")

if __name__ == '__main__':
    verify()
