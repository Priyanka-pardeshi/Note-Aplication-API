from noteapp.models import Note, Label
from rest_framework.serializers import ModelSerializer


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'user']


class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
