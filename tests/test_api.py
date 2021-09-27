import json
import pytest
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from registerapp.models import UserRegistration

pytestmark = pytest.mark.django_db


# mixer , use client

class TestUser:
    @pytest.mark.django_db
    def test_registrations(self, client):
        url = reverse('reg:register')

        data = {"username": "sidhh139", "email": "priyankasspardeshi@gmail.com", "password": "System",
                "first_name": "sidh",
                "last_name": "adkar"}
        print(data)
        # data.save()
        response = client.post(url, data)
        assert response.status_code == 201


class TestLogin():

    @pytest.mark.django_db
    def test_login(self, client):
        user = UserRegistration.objects.create_user(
            username="SID", password="System", email="priyankasspardeshi@gmail.com")
        user.is_verify = True
        user.save()
        url = reverse('reg:Login')
        data = {"username": "SID", "password": "System"}
        response = client.post(url, data)
        print(json.loads(response.content))
        assert response.status_code == 200


class TestNote:
    @pytest.mark.django_db
    def test_add_note(self, client):
        user = UserRegistration.objects.create_user(
            username="SID", password="System", email="priyankasspardeshi@gmail.com")
        user.is_verify = True
        user.save()
        url = reverse('reg:Login')
        data = {"username": "SID", "password": "System"}
        response = client.post(url, data)
        print(json.loads(response.content))
        temp = json.loads(response.content)
        print(temp)
        my_token = temp.get('token')
        print(my_token)

        note_url = reverse('note:my_note')
        note_data = {"title": "my note", "description": "my note"}
        header = {"HTTP_TOKEN": my_token}
        note_response = client.post(note_url, note_data, **header)
        print(note_response.content)
        assert note_response.status_code == 201


class TestNotePut:
    @pytest.mark.django_db
    def test_put_note(self, client):
        user = UserRegistration.objects.create_user(
            username="SIDH", password="System", email="priyankasspardeshi@gmail.com")
        user.is_verify = True
        user.save()
        url = reverse('reg:Login')
        data = {"username": "SIDH", "password": "System"}
        response = client.post(url, data)
        print(json.loads(response.content))
        temp = json.loads(response.content)
        print(temp)
        my_token = temp.get('token')
        print(my_token)

        # create note
        note_url = reverse('note:my_note')
        note_data = { "title": "my note", "description": "my note"}
        header = {"HTTP_TOKEN": my_token}
        note_response = client.post(note_url, note_data, **header,content_type='application/json')
        print("response:", note_response.content)
        # getting id
        data_response = note_response.content
        print("id-",data_response)
        dict = json.loads(data_response)

        temp_id = dict['data']['id']
        print("  temp id-",temp_id)

        print("data:", note_data)

        # update note
        note_update_url = reverse('note:my_note')
        note_updated_data = {"title": "my note", "description": "my updated note", "id": temp_id}
        note_update_response = client.put(note_update_url, note_updated_data, **header, content_type='application/json')
        print("updated response:", note_update_response.content)
        assert note_update_response.status_code == 200


class TestNoteDelete:
    @pytest.mark.django_db
    def test_delete_note(self, client):
        user = UserRegistration.objects.create_user(
            username="SIDHH", password="System", email="priyankasspardeshi@gmail.com")
        user.is_verify = True
        user.save()
        url = reverse('reg:Login')
        data = {"username": "SIDHH", "password": "System"}
        response = client.post(url, data)
        print(json.loads(response.content))
        temp = json.loads(response.content)
        print(temp)

        my_token = temp.get('token')
        print(my_token)

        note_url = reverse('note:my_note')
        note_data = { "title": "my note", "description": "my note"}
        header = {"HTTP_TOKEN": my_token}
        note_response = client.post(note_url, note_data, **header)

        note_url = reverse('note:my_note')
        note_data = {"id": 1}
        header = {"HTTP_TOKEN": my_token}
        note_response = client.delete(note_url, note_data, **header,content_type='application/json')
        print(note_response.content)
        assert note_response.status_code == 200
