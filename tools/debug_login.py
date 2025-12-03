import os
import sys

# Ensure DJANGO_SETTINGS_MODULE is set by manage.py environment; emulate manage.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django import setup
from django.test import Client
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
setup()

c = Client()
try:
    r = c.post('/login/', {'username': 'doesnotexist', 'password': 'bad'}, follow=True)
    print('STATUS', r.status_code)
    print(r.content.decode('utf-8')[:2000])
except Exception:
    traceback.print_exc()
