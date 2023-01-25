from django.contrib.auth.models import User
from rest_framework import status
from django.http import JsonResponse
from django.urls import reverse
from dotenv import load_dotenv
import os
import jwt
load_dotenv()

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path in [reverse('login'),reverse('home')]:
            token = request.COOKIES.get('token')
            if not token:
                return JsonResponse({'message':'Unauthorized! Please Login before accessing this.'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=['HS256'])
            except:
                return JsonResponse({'message':'Unauthorized! Please Login before accessing this.'},status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.filter(username=payload['username']).first()
            if not user:
                return JsonResponse({'message':'Unauthorized! Please Login before accessing this.'},status=status.HTTP_401_UNAUTHORIZED)
        response = self.get_response(request)
        return response