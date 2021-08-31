import jwt
from django.core.exceptions import FieldDoesNotExist
from rest_framework.exceptions import ParseError, NotFound

import logging
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from noteapp.serializer import NoteSerializer
from noteapp.models import Note

logging.basicConfig(filename='UserRegistration.log', filemode='w')

"""
Class Note contains Methods POST, GET, PUT, DELETE
POST-used to Insert record.
GET-Used to get specific record.
PUT-Used to Alter or edit  record.
Delete- Used to Delete record. 
"""


class Notes(APIView):

    def post(self, request):
        try:
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid():
                token=request.headers.get['token']
                serializer.token = jwt.decode(token, "secret", algorithm=["HS256"])
                logging.info('Data is valid data')
                serializer.save()
                logging.info('Data is saved and status has been generated')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logging.error('Data is not valid data, bad status generated')
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except FieldDoesNotExist:
            logging.exception('Field does not exists')
            return Response('Field Does not exists')

        except ParseError as exception:
            logging.exception({'Exception': 'Request contains malformed data'})
            return Response('Exception:', exception)
        except Exception as e:
            logging.exception('Exception occurs as:', str(e))
            return Response('Exception', str(e))

    def get(self, request,token):
        try:
            decoded_token = jwt.decode(token, "secret", algorithm=["HS256"])
            note = Note.objects.all(fk=decoded_token)
            serializer = NoteSerializer(note)
            # return Response('return note with associated with fk')
            logging.info('Getting specific Note from Register User')
            return Response(serializer.data)
        except NotFound as exception:
            logging.exception('Record Not found')
            return Response({'Resource Does not exists': exception})

    def put(self, request, token):
        try:
            decoded_token=jwt.decode(token, "secret", algorithms="HS256")
            note = Note.objects.get(fk=decoded_token)
            serializer = NoteSerializer(note, data=request.data)
            if serializer.is_valid():
                logging.info('Data is valid data')
                serializer.save()
                return Response('Data is updated/Edited')
            return Response('Not updated')
        except FieldDoesNotExist as exception:
            logging.exception('Requested field Does not exists')
            return Response({'Exception': exception})

    def delete(self, reqest, token):
        try:
            decoded_token=jwt.decode(token,"secret",algorithms="HS265")
            note = Note.objects.get(fk=decoded_token)
            note.delete()
            logging.info('Record has been successfully deleted')
            return Response('Deleted record')
        except Exception as exception:
            logging.exception('Exception occurs as:', exception)
            return Response({'Excption': exception })