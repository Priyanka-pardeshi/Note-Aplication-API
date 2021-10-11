from django.urls import path
from noteapp.views import Notes, NoteLabel, AddCollaborator
from noteapp.elasticsearch import Elastic_search
app_name = 'note/'
urlpatterns = [
    path('notes/', Notes.as_view(), name='my_note'),
    path('myindex', Notes.as_view(), name='my_elastic_search'),
    path('label/', NoteLabel.as_view(), name='my_label'),
    path('colab/', AddCollaborator.as_view(), name='my_colab')
]
