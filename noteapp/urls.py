from django.urls import path
from noteapp.views import Notes, NoteLabel, AddCollaborator

app_name = 'note/'
urlpatterns = [
    path('notes/', Notes.as_view(), name='my_note'),
    path('label/', NoteLabel.as_view(), name='my_label'),
    path('colab/', AddCollaborator.as_view(), name='my_colab')
]
