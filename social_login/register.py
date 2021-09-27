from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv
import random
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
User = get_user_model()
load_dotenv()


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        registered_user = authenticate(
            username=filtered_user_by_email[0].username, password=os.getenv('SOCIAL_SECRET'))
        token, created = Token.objects.get_or_create(user=filtered_user_by_email[0])
        return {
            'username': registered_user.username,
            'email': registered_user.email,
            'token': token.key
        }

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': os.getenv('SOCIAL_SECRET')}
        user = User.objects.create_user(**user)
        user.is_verified = True
        # user.auth_provider = provider
        user.save()

        new_user = authenticate(
            username=user.username, password=os.getenv('SOCIAL_SECRET'))
        token, created = Token.objects.get_or_create(user=new_user)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'token': token.key
        }
