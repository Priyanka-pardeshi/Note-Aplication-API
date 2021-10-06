from django.core.exceptions import FieldDoesNotExist
from registerapp.models import UserRegistration
from rest_framework.exceptions import ParseError, NotFound

import logging
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from noteapp.serializer import NoteSerializer, LabelSerializer
from noteapp.models import Note, Label
from noteapp.util import validate_token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logging.basicConfig(filename='UserRegistration.log', filemode='w')

"""
Class Note contains Methods POST, GET, PUT, DELETE
POST-used to Insert record.
GET-Used to get specific record.
PUT-Used to Alter or edit  record.
Delete- Used to Delete record. 
"""


class Notes(APIView):

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)],
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                             'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")}))
    @validate_token
    def post(self, request):
        try:
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid():
                logging.info('Data is valid data')
                note = serializer.save()
                print("Note id::", note.id)
                logging.info('Data is saved and status has been generated')
                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        except FieldDoesNotExist:
            logging.exception('Field does not exists')
            return Response({'Message': 'Field Does not exists'})

        except ParseError as exception:
            logging.exception({'Exception': 'Request contains malformed data'})
            return Response({'Exception:', str(exception)})
        except Exception as e:
            logging.exception('Exception occurs as:', str(e))
            return Response('Exception', str(e))

    #@swagger_auto_schema(manual_parameters=[openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)],
    #                     request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    #                         'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id")}))
    @validate_token
    def get(self, request):
        try:
            # get collaborator and label
            user_id = request.data['user']
            print(user_id)
            note = Note.objects.filter(user_id=user_id)
            serializer = NoteSerializer(note, many=True)
            logging.info('Getting specific Note from Register User')
            #  add status
            return Response({'Note List': serializer.data}, status=status.HTTP_200_OK)
        except NotFound as exception:
            logging.exception('Record Not found')
            return Response({'Resource Does not exists': exception})
        except Exception as exception:
            return Response({'Exception': exception})

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)],
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                             'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
                             'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id')}))
    @validate_token
    def put(self, request):
        try:
            identity = request.data.get('id')
            print("Note id::", identity)
            obj = Note.objects.get(pk=identity)
            print(obj)
            serializer = NoteSerializer(obj, data=request.data)
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

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)],
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id")}))
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


class NoteLabel(APIView):

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)],
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'label_name': openapi.Schema(type=openapi.TYPE_STRING, description="label_name"),
                             'color': openapi.Schema(type=openapi.TYPE_STRING, description="color")}))
    @validate_token
    def post(self, request):
        try:

            serializer = LabelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'Message': 'Serializer is not valid'})
        except Exception as e:
            return Response({'Exception ': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #@swagger_auto_schema(manual_parameters=[openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)],
    #                     request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    #                         'id': openapi.Schema(type=openapi.TYPE_STRING, description='id')
    #                     }))
    @validate_token
    def get(self, request):
        try:
            label_id = request.data.get('id')
            print(label_id)
            label = Label.objects.get(id=label_id)
            print(label)
            serializer = LabelSerializer(label)
            return Response({"Data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response({'Exception:': str(exception)})

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)],
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'id': openapi.Schema(type=openapi.TYPE_STRING, description='id')
                         }))
    @validate_token
    def delete(self, request):
        try:
            label_id = request.data.get('id')
            label = Label.objects.get(pk=label_id)
            label.delete()
            return Response({'Message': 'Data is successfully deleted'}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response({'Exception:': str(exception)})

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING)],
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                             'label_name': openapi.Schema(type=openapi.TYPE_STRING, description="label_name"),
                             'color': openapi.Schema(type=openapi.TYPE_STRING, description="color"),
                             'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id')}))
    @validate_token
    def put(self, request):
        try:
            label_id = request.data.get('id')
            print(label_id)
            obj = Label.objects.get(pk=label_id)
            serializer = LabelSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=status.HTTP_200_OK)
            return Response({'message:': 'Serializer is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            return Response({'exception:': str(exception)}, status=status.HTTP_400_BAD_REQUEST)


class AddCollaborator(APIView):

    @validate_token
    def post(self, request):
        try:
            # getting the note id, user_id
            note_id = request.data.get('note_id')
            user_id = request.data.get('userregistration_id')
            print("user id::", user_id, "Note Id::", note_id)

            # getting object associated with it
            note = Note.objects.get(pk=note_id)
            collaborator_obj = UserRegistration.objects.get(pk=user_id)
            print("note object::", note, "collaborator object::", collaborator_obj)

            # adding collaboratoer user to notes
            note.collaborator.add(collaborator_obj)
            objs = note.collaborator.all()

            print(objs)
            return Response({"Message": "Successfully added an collaborator"}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response({"exception": str(exception)})
