from django.urls import path
from noteapp.views import Notes

app_name = 'note/'
urlpatterns = [
    path('noteit/', Notes.as_view()),
    path('noteit/<str:reg_no>/<str:note_id>/', Notes.as_view()),

]
