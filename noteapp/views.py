from django.core.exceptions import FieldDoesNotExist
from django.shortcuts import render
import logging
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from noteapp.serializer import NoteSerializer
from django.core import exceptions

logging.basicConfig(filename='Lognote.log', filemode='w')


class AddNote(APIView):

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
