from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class GetUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE())


from rest_framework import serializers

class SerializerUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class Register(APIView):
    def post(self,request):
        if request.method == "post":
            serializers = SerializerUser(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request):
        if request.method == "post":
            email = request.data.get('email')
            password = request.data.get('password')

            user = User.objects.filter(email=email)
            if user and user.check_password(request.data.get('password')):
                refresh = RefreshToken.for_user(user)
                return Response({"status":201,"response":"success","refresh":str(refresh),'access':str(refresh.access_token())},status=status.HTTP_200_OK)
            else:
                return Response({"status":401,"Response":"not found"},status=status.HTTP_404_NOT_FOUND)

class GetPutDelete(APIView):
    def get(self,request):
        if request.method == 'get':
            try:
                user = User.objects.get(id=request.user.pk)
                if user:
                    serializers = SerializerUser(user)
                    return Response(serializers.data,status=status.HTTP_200_OK)            
            except:
                return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)    
    def put(self,request):
        if request.method == 'put':
            try:
                user = User.objects.get(id=request.user.pk)
                if user:
                    serializers = SerializerUser(user,partial=True)
                    if serializers.is_valid():
                        serializers.save()
                        return Response(serializers.data,status=status.HTTP_200_OK)
            except:
                return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        if request.method =='delete':
            try:
                user = User.objects.get(id=request.user.pk)
                if user:
                    user.delete()
                    return Response({"status":200,"response":"success"},status=status.HTTP_200_OK)
            except:
                return Response({"status":400,"response":"failed"},status=status.HTTP_400_BAD_REQUEST)                            
            
from django.urls import path

urlpatterns = [
    path("",Register.as_view()),
    path("login",Login.as_view()),
    path('get',GetPutDelete.as_view()),
    path('put',GetPutDelete.as_view),
    path('delete',GetPutDelete.as_view())
]


    