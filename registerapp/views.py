import logging
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from registerapp.models import Registration
from registerapp.serializer import RegisterSerializer, UserSerializer

# Create your views here.
"""
This is user defined register model.
Which return Http response user registered or not  
"""

logging.basicConfig(filename='UserRegistration.log',filemode='w')


class Register(APIView):

    def post(self, req):
        """doc str

        """
        try:
            serializer = RegisterSerializer(data=req.data)
            if serializer.is_valid():
                logging.info('Data is validated')
                serializer.save()
                logging.info('Data information is saved')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logging.error('not valid response')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # raise e
            logging.error('Exception occurres')
            return Response(" Exception:",str(e))


"""
UserLogin class take Username and password  and,
Returns Http response That user is valid or not 
"""


class RegisterLogin(APIView):
    def post(self, req):
        try:
            users_mail = req.POST['email']
            password = req.POST['password']
            if Registration.objects.filter(email__exact=users_mail, password__exact=password):
                print("Login successfully")
                logging.info('Login is successful')
                return Response("Login successful")
            print("login failed")
            logging.info('Login is failed')
            return Response("Login failed")
        except Exception as e:
            logging.exception('Exception occurs as:', str(e))
            return Response("Exception:", e)


"""
Function save registration data into user model
Return Http response
"""


class UserRegistrationModel(User, APIView):

    def post(self, req):
        try:
            serializer = UserSerializer(data=req.data)
            if serializer.is_valid():
                serializer.save()
                logging.info('Information is saved')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logging.info('something went wrong check input data')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.info('Exception occurs:', e)
            raise e


"""
Function take User name an password
and return response That user is valid or not  
"""


class UserLogin(User,APIView):

    def post(self, req):

        try:
            users_mail = self.POST['email']
            password = self.POST['password']
            user = authenticate(self, username=users_mail, password=password)
            if user is not None:
                logging.info('model user exists and logging is successful')
                Response("Login is successful")
            else:
                logging.info('Model user is not valid')
                HttpResponse("model user is not valid User")
        except Exception as e:
            logging.exception('Exception occurs as:', e)
            raise e
