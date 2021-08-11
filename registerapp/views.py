import logging
import json
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from registerapp.models import Registration
from django.views import View
from registerapp.serializer import RegisterSerializer, UserSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
"""
This is user defined register model.
Which return Http response user registered or not  
"""
logger = logging.getLogger(__name__)
logging.basicConfig(filename='UserRegistration.log', encoding='utf-8', level=logging.DEBUG)


class Register(APIView):

    def post(self, req):
        """doc str

        """
        try:
            serializer = RegisterSerializer(data=req.data)
            if serializer.is_valid():
                logger.info('Data is validated')
                serializer.save()
                logger.info('Data information is saved')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error('not valid response')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # raise e
            logger.error('Exception occurres')
            return Response()

            # data = json.loads(req.body)
            # print(data)
            # user_name = data.get("name")
            # user_email = data.get("email")
            # user_password = data.get("password")
            # user_contact = data.get("contact")
            # user_dob = data.get("dob")
            # print(user_name, user_email, user_password, user_contact, user_dob)
            # all_record_object = Registration.objects.all()

            # register_object = Registration(name=user_name, email=user_email, password=user_password, contact=user_contact, dob=user_dob)
            # register_object.save()
            # register_object.id
            # first_record = Registration.objects.get(id=1)
            # print(first_record.id)

            # return HttpResponse("record inserted")


"""
UserLogin class take Username and password  and,
Returns Http response That user is valid or not 
"""


class UserLogin(APIView):
    def post(self, req):
        try:
            users_mail = req.POST['email']
            password = req.POST['password']
            # dataa = json.loads(req.body)
            # user_mail = dataa.get("email")
            # user_password = dataa.get("password")
            if Registration.objects.filter(email__exact=users_mail) & Registration.objects.filter(
                    password__exact=password):
                print("Login successfully")
                return Response()
            else:
                print("login failed")
                return HttpResponse("Login failed")
        except Exception as e:
            raise e


"""
Function save registration data into user model
Return Http response
"""


def RegisrationionUserModel(req):
    try:
        serializer = UserSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise e

        # dataa = json.loads(req.body)
        # user_name = dataa.get("username")
        # user_firstname = dataa.get("first_name")
        # user_lastname = dataa.get("last_name")
        # user_email = dataa.get("email")
        # user_password = dataa.get("password")
        # user_object = User(username=user_name, first_name=user_firstname, last_name=user_lastname, email=user_email, password=user_password)
        # crate_user method have three args as username, email, password
        # euserObject = User.objects.create_user('sidhika22', 'sidhika1@gmailcom', 'sidhi123')
        # euserObject.last_name = 'adkar'
        # user_object.save()
        # return HttpResponse("record is inserted")
    # except Exception as e:
    #    raise e


"""
Function take User name  
"""


class ValiateUser(APIView):
    def ValidUser(req):
        try:
            users_mail = req.POST['email']
            password = req.POST['password']
            user = authenticate(req, username=users_mail, password=password)
            if user is not None:
                HttpResponse("User is Exists")
            else:
                HttpResponse("User is already exists")
        except Exception as e:
            raise e

        # data = json.loads(req.body)
        # users_name = req.POST['username']
        # password = req.POST['password']
        # users_name=data.get("username")
        # password=data.get("password")
