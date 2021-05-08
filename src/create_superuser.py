#!/usr/bin/env python

import os
import environ

import django

# Load operating system environment variables and then prepare to use them
env = environ.Env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth.models import User

username = env.str("DJANGO_ADMIN")
password = env.str("DJANGO_ADMIN_PASSWORD")
email = env.str("DJANGO_ADMIN_EMAIL")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created.")
else:
    print("Superuser creation skipped.")
