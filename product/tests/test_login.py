import json

from django.test import TestCase, RequestFactory

import account.views
from product.models import *
from account.models import User


class LoginLogout(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_signin(self):
        self.url = '/signin/'
        json_data = json.dumps({"username": "hossein", "password": "hossein1234"})
        request = self.factory.post(self.url, data=json_data, content_type='application/json')

        response = account.views.signin(request)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        self.url = '/signin/'
        json_data = json.dumps({"username": "hossein", "password": "hossein1234"})
        request = self.factory.post(self.url, data=json_data, content_type='application/json')

        response = account.views.signin(request)
        self.url = '/login/'

        json_data = json.dumps({"username": "hossein", "password": "hossein1234"})
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.url = '/signin/'
        json_data = json.dumps({"username": "hossein", "password": "hossein1234"})
        request = self.factory.post(self.url, data=json_data, content_type='application/json')
        json_data = json.dumps({"username": "hossein", "password": "hossein1234"})
        self.url = '/login/'

        request = self.client.post(self.url, data=json_data, content_type='application/json')
        self.url = '/logout/'

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
