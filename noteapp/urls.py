from django.urls import path
from noteapp.views import AddNote

app_name = 'note/'
urlpatterns = [
    path('addNote/', AddNote.as_view()),
]
