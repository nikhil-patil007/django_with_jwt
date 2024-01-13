from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers  import make_password,check_password

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .validatorsFile import isJWTAuthanticated


import json
import logging
from .models import User

logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    return render(request,'index.html')

@api_view(['POST'])
def register_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        # name = data.get('name')
        # contact_no = data.get('contact')
        username = data.get('username')
        email = data.get('email')
        email = data.get('email')
        password = data.get('password')
        confirmPassword = data.get('cpassword')

    
        if password != confirmPassword:
            return Response({'message':"password and confirm password doesn't match...!"},status=401)    
        else:
            checkuser = User.objects.filter(email=email)
            print("checkuser",checkuser,len(checkuser) > 0)
            if len(checkuser) > 0:
                return Response({'message':"Existing User...!"},status=409 )
            else:
                userAdd = User.objects.create(
                    username=username,
                    email = email,
                    password= make_password(password),
                )
                return Response({'message':"Successfully Register User!!!"},status=200)
    except Exception as e:
        print('error',e)
        logger.error(f"Error during user registration: {str(e)}")
        return Response({'error': 'Internal Server Error'}, status=500)
        
@api_view(['POST'])
def login_user(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')
    userList = User.objects.filter(email=email).first()
    if len(User.objects.filter(email=email)) > 0:
        if check_password(password,userList.password):
            refresh = RefreshToken.for_user(userList)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({'message':"User Login successfully",'token': token},status=200)
    return Response({'message':"username or password doesn't match...!"},status=401)    

@api_view(['GET'])
@isJWTAuthanticated
def check_token(request):
    # If the request reaches here, the token is valid
    responseData = [{
        "id": 1,
        "title": "iPhone 9",
        "description": "An apple mobile which is nothing like apple",
        "price": 549,
        "discountPercentage": 12.96,
        "rating": 4.69,
        "stock": 94,
        "brand": "Apple",
        "category": "smartphones",
        "thumbnail": "https://cdn.dummyjson.com/product-images/1/thumbnail.jpg",
        "images": [
            "https://cdn.dummyjson.com/product-images/1/1.jpg",
            "https://cdn.dummyjson.com/product-images/1/2.jpg",
            "https://cdn.dummyjson.com/product-images/1/3.jpg",
            "https://cdn.dummyjson.com/product-images/1/4.jpg",
            "https://cdn.dummyjson.com/product-images/1/thumbnail.jpg"
            ]
        }
    ]
    return Response({'message': 'Data Loaded','data':responseData}, status=200)