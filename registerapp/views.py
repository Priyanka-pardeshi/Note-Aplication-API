import logging
import jwt
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from registerapp.models import UserRegistration
from registerapp.serializer import UserRegistrationSerializer

# Create your views here.
"""
This is user defined register model.
Which return Http response user registered or not  
"""

logging.basicConfig(filename='UserRegistration.log', filemode='w')

"""
Function save registration data into user model
Return Http response
"""


class Registration(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'username': openapi.Schema(type=openapi.TYPE_STRING, description="username"),
                             'email': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
                             'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
                             'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                             'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name')}))
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                user = UserRegistration.objects.create_user(username=request.data['username'],
                                                            password=request.data['password'],
                                                            email=request.data['email'],
                                                            first_name=request.data['first_name'],
                                                            last_name=request.data['last_name'])
                user.location = request.data.get('location')
                user.save()
                logging.info('Information is saved')

                print(user.id)
                encoded_token_id = jwt.encode({"id": user.id}, "secret", algorithm="HS256")

                print(encoded_token_id)
                url = "http://127.0.0.1:8000/reg/" + encoded_token_id
                send_mail('Verification', url, 'priyankapardeshi224@gmail.com',
                      [ request.data.get('email')])

                return Response({"Message":"Info is saved"}, status=status.HTTP_201_CREATED)
            logging.info('something went wrong check input data')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.info('Exception occurs:', e)
            print(str(e))
            return Response({'Exception': str(e)})


"""
Function take User name an password
and return response That user is valid or not  
"""


class UserLogin(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                             'password': openapi.Schema(type=openapi.TYPE_STRING, description='password')}))
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

        # setPassword
            user = authenticate(request, username=username, password=password)
            is_verified = user.is_verify
            encoded_token = jwt.encode({"id": user.id}, "secret", algorithm="HS256")
            print(username, password)
            print(user)
            if user is not None:
                if is_verified is True:
                    logging.info('model user exists and logging is successful')
                    return Response({"Message": "Login is successful", "token": encoded_token})
                logging.info('Model user is not valid')
                return Response({"Message": "model user is not valid User"})
        except Exception as e:
            logging.exception('Exception occurs as:', e)
            return Response({'Exception': str(e)})


class VerifyUser(APIView):
    def get(self, request, token):
        try:
            print(token)
            decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
            print(decoded_token)
            user_id = decoded_token.get("id")
            print(user_id)
            # retrieve value from dict
            user = UserRegistration.objects.get(id=user_id)
            user.is_verify = True
            serializer = UserRegistrationSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "Successfully validated user "})
            return Response({"Message": "Data is not validated"})
        except Exception as exception:
            logging.exception("Exception occurs")
            return Response({"Exception": str(exception)})

