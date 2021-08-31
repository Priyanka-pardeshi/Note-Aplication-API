import logging
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
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
                encoded_token = jwt.encode({"username": request.data.get('username')}, "secret", algorithm="HS256")
                url = "http://127.0.0.1:8000/reg/verify/" + encoded_token
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

    def post(self, request):
        # try:
        username = request.data.get('username')
        password = request.data.get('password')
        is_verified = request.data.get('is_verify')
        # setPassword
        encoded_token = jwt.encode({"username": request.data.get('username')}, "secret", algorithm="HS256")
        user = authenticate(request, username=username, password=password)
        #is verified and not none.

        print(username, password)
        print(user)
        if user is not None:
            if is_verified is True:
                logging.info('model user exists and logging is successful')
                return Response({"Message": "Login is successful", "token": encoded_token})
            logging.info('Model user is not valid')
            return Response({"Message": "model user is not valid User"})
    # except Exception as e:
    #    logging.exception('Exception occurs as:', e)
    #    return Response({'Exception': str(e)})


class VerifyUser(APIView):
    def get(self, request, token):
        try:
            decoded_token = jwt.decode(token, "secret", algorithm=["HS256"])
            user = UserRegistration.objects.get(id=decoded_token)
            serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.is_verify = True

                serializer.save()
                return Response({"Message": "Successfully validated user "})
            return Response({"Message": "Data is not validated"})
        except Exception as exception:
            logging.exception("Exception occurs")
            return Response({"Exception": str(exception)})
