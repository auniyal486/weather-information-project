from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from dotenv import load_dotenv
import requests
import jwt
import datetime
import os
load_dotenv()

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")

class MainView(APIView):          

    def get(self, request):
        content = {'message': 'Weather Application'}
        return Response(content)


class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({'message':'Invalid Details! Please Provide Correct Details'},status= status.HTTP_401_UNAUTHORIZED)
        payload = {
            'username':user.username,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, AUTH_SECRET_KEY, algorithm='HS256')
        token = token if type(token)==str else token.decode("utf-8")

        response = Response()
        response.set_cookie(key='token', value=token, httponly=True)
        response.data = {
            'message': 'You are successfully logged in.',
            'token': token
        }
        return response
    
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('token')
        response.data = {'message' : 'You are successfully logged out.'}
        return response

class WeatherApi(APIView):
    ids_list = ["2643743","5128638","1275004","1275339","1264527","1185241","1162015","1850147","1174872","1177654",\
                "1259229","2267226","1792947","1642911","1609348","1176734","1791247","1279233","1819729","3530597",\
                "4190598","3435907","1270351","1263968","1264733","1253405","1253628","1253985","4736286","4350049"]
    weather_app_key = os.getenv("WEATHER_APP_KEY")
    url = "http://api.openweathermap.org/data/2.5/group"
    def get(self,request):
        limit= int(request.GET.get('limit',10))
        pageno= int(request.GET.get('pageno',1))
        if (pageno-1)*limit>=len(self.ids_list):
            return Response({"Weather Information":[]})
        cities_id_list = self.ids_list[(pageno-1)*limit:(pageno)*limit]
        weather_data = []
        index = 0
        while(index<len(cities_id_list)):
            PARAMS = {"appid":self.weather_app_key,"units":"imperial","id":','.join(cities_id_list[index:index+20])}
            r = requests.get(url=self.url,params=PARAMS)
            if r.status_code!=200:
                return Response(status= status.HTTP_500_INTERNAL_SERVER_ERROR)
            weather_data.extend(r.json()["list"])
            index +=20
        return Response({"Weather Information":weather_data,'total_cities':len(weather_data)})
