import os
from dotenv import load_dotenv
from pathlib import Path

# Explicitly define the path to .env to match what settings.py likely sees
env_path = Path('.') / '.env'
print(f"Checking for .env at: {env_path.resolve()}")
print(f"File exists: {env_path.exists()}")

# Load .env
load_dotenv()

# Check keys
print(f"STRIPE_PUBLIC_KEY: {os.environ.get('STRIPE_PUBLIC_KEY')}")
print(f"STRIPE_SECRET_KEY: {os.environ.get('STRIPE_SECRET_KEY')}")
