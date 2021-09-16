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
        url = reverse('reg:userReg')

        data = {"username": "sidhh139", "email": "priyankasspardeshi@gmail.com", "password": "System",
                "first_name": "sidh",
                "last_name": "adkar"}

        # data.save()
        response = client.post(url, data)
        assert response.status_code == 200


def test_login():
    url = "http://127.0..0.1:8000/reg/login/"
    # pass encrypted username
    data = {"username": "sidhh139", "password": "System"}
    data = json.loads(data.content)
    # extract token update

    response = client.post(url, data)

    assert response.status_code == 200
