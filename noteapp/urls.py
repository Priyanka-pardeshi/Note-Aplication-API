from django.urls import path
from noteapp.views import Notes

app_name = 'note/'
urlpatterns = [
    path('notes/', Notes.as_view()),
#    path('noteit/<str:fk>/', Notes.as_view()),

]
