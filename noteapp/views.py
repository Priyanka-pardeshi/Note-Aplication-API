from django.core.exceptions import FieldDoesNotExist
from registerapp.models import UserRegistration
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

    def post(self, req):
        try:
            serializer = NoteSerializer(data=req.data)
            if serializer.is_valid():
                logging.info('Data is valid data')
                serializer.save()
                logging.info('Data is saved and status has been generated')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logging.error('Data is not valid data, bad status generated')
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except FieldDoesNotExist:
            logging.exception('Field does not exists')
            return Response('Field Does not exists')
        except Exception as e:
            logging.exception('Exception occurs as:', str(e))
            return Response('Exception', str(e))

    def get(self, req, reg_no=None, note_id=None):
        if reg_no is not None:
            if note_id is not None:

                # getting a single note associated with FK
                get_id = UserRegistration.objects.get(id=reg_no)
                getting_a_note = Note.objects.get(id=note_id)
                serializer = NoteSerializer(getting_a_note)
                # return Response('return note with associated with fk')
                logging.info('Getting specific Note from Register User')
                return Response(serializer.data)
            else:
                # getting all notes associated with FK
                get_id = UserRegistration.objects.get(reg_no)
                getting_all_note = Note.objects.all()
                serializer = NoteSerializer(getting_all_note, data=req.data)
                logging.info("As User doesn't provide Note Id Returning all Notes Information")
                return Response(serializer.data)
                # return Response('return all note with specific fk')
        else:
            # return all Register user
            specific_note_id =UserRegistration.objects.all()
            serializer = NoteSerializer(specific_note_id, many=True)
            # return Response('Return all register user')
            return Response(serializer.data)

    def put(self, req, reg_no, note_id):
        get_id = UserRegistration.objects.get(id=reg_no)
        getting_a_note = Note.objects.get(id=note_id)
        serializer = NoteSerializer(getting_a_note, data=req.data)
        if serializer.is_valid():
            logging.info('Data is valid data')
            serializer.save()
            return Response('Data is updated/Edited')
        return Response('Not updated')

    def delete(self, req, reg_no, note_id):
        get_id = UserRegistration.objects.get(id=reg_no)
        getting_a_note = Note.objects.get(id=note_id)
        getting_a_note.delete()
        logging.info('Record has been successfully deleted')
        return Response('Deleted record')
