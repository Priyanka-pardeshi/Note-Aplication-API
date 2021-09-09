from django.core.exceptions import FieldDoesNotExist
from rest_framework.exceptions import ParseError, NotFound

import logging
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from noteapp.serializer import NoteSerializer
from noteapp.models import Note
from noteapp.util import decode_token, validate_token

logging.basicConfig(filename='UserRegistration.log', filemode='w')

"""
Class Note contains Methods POST, GET, PUT, DELETE
POST-used to Insert record.
GET-Used to get specific record.
PUT-Used to Alter or edit  record.
Delete- Used to Delete record. 
"""


class Notes(APIView):
    @validate_token
    def post(self, request):
        try:
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid():
                logging.info('Data is valid data')
                serializer.save()
                logging.info('Data is saved and status has been generated')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logging.error('Data is not valid data, bad status generated')
            return Response({'message': "note saved"}, status=status.HTTP_400_BAD_REQUEST)

        except FieldDoesNotExist:
            logging.exception('Field does not exists')
            return Response({'Message': 'Field Does not exists'})

        except ParseError as exception:
            logging.exception({'Exception': 'Request contains malformed data'})
            return Response({'Exception:', exception})
        except Exception as e:
            logging.exception('Exception occurs as:', str(e))
            return Response('Exception', str(e))

    @validate_token
    def get(self, request):
        try:
            user_id = request.data['user']
            print(user_id)
            note = Note.objects.filter(user_id=user_id)
            serializer = NoteSerializer(note, many=True)
            # return Response('return note with associated with fk')
            logging.info('Getting specific Note from Register User')
            #  add status
            return Response({'Note List': serializer.data}, status=status.HTTP_200_OK)
        except NotFound as exception:
            logging.exception('Record Not found')
            return Response({'Resource Does not exists': exception})
        except Exception as exception:
            return Response({'Exception': exception})

    @validate_token
    def put(self, request):
        try:
            identity = request.data.get('id')
            print("Note id", identity)
            obj = Note.objects.get(pk=identity)
            print(obj)
            serializer = NoteSerializer(obj, data=request.data)
            #            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                logging.info('Data is valid data')
                serializer.save()
                return Response({'Message': 'Data is updated/Edited'}, status=status.HTTP_200_OK)
            return Response({'Message': 'Not updated'}, status=status.HTTP_304_NOT_MODIFIED)
        except FieldDoesNotExist as exception:
            logging.exception('Requested field Does not exists')
            return Response({'Exception': exception})
        except Exception as exception:
            return Response({'Exception occurs': exception})

    @validate_token
    def delete(self, request):
        try:
            user_id = request.data['user']
            note = Note.objects.all().filter(user_id=user_id)
            serializer = NoteSerializer(note, many=True)
            identity = request.data.get('id')
            print(identity)
            obj = Note.objects.filter(id=identity)
            print("object:", obj)
            print(serializer)
            print("this is Note:", note)
            obj.delete()
            logging.info('Record has been successfully deleted')
            return Response({'Message': 'Deleted record'}, status=status.HTTP_200_OK)
        except Exception as exception:
            logging.exception('Exception occurs as:', exception)
            return Response({'Exception': exception})
