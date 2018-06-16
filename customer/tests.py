from django.test import TestCase
from customer.models import Customer
import copy
from .util import test_general


class RegisterTestCase(TestCase):
    """ Test normal customer registration procedural. """

    data = {
        'email': 'register@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'do not fuck',
        'last_name': 'me',
        'tel': '123456789',
        'address': 'the test is awesome'
    }
    fields = ['email', 'password', 'password_confirmation', 'first_name', 'last_name', 'tel', 'address']
    url = '/register/'

    def setUp(self):
        Customer.objects.filter(user__email='register@test.com').delete()

    def test_normal_register(self):
        status, body = test_general(self.url, self.data, 'post')
        self.assertEqual(status, 200)

    def test_fields_blank_exception(self):
        request = copy.deepcopy(self.data)
        for field in self.fields:
            request.pop(field, None)
            status, body = test_general(self.url, request, 'post')
            self.assertEqual(status, 400)
            request.update({field: self.data[field]})

    def test_email_exist_exception(self):
        request = copy.deepcopy(self.data)
        test_general(self.url, request, 'post')
        status, body = test_general(self.url, request, 'post')
        self.assertEqual(status, 400)

    def test_password_mismatch_exception(self):
        request = copy.deepcopy(self.data)
        request['password_confirmation'] = '/.,buz'
        status, body = test_general(self.url, request, 'post')
        self.assertEqual(status, 400)


class LoginTestCase(TestCase):
    """ Test customer normal login. """

    data = {
        'email': 'login@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'do not fuck',
        'last_name': 'me',
        'tel': '123456789',
        'address': 'the test is awesome'
    }
    url = '/login/'

    def setUp(self):
        Customer.objects.filter(user__email='login@test.com').delete()
        test_general('/register/', self.data, 'post')

    def test_normal_login(self):
        request = {
            'email': 'login@test.com',
            'password': '/.,buz123'
        }
        status, body = test_general(self.url, request, 'post')
        self.assertEqual(status, 200)

    def test_wrong_password_login(self):
        request = {
            'email': 'login@test.com',
            'password': '/.,buz'
        }
        status, body = test_general(self.url, request, 'post')
        self.assertEqual(status, 400)

    def test_user_not_exist_login(self):
        request = {
            'email': 'login_none@test.com',
            'password': '/.,buz'
        }
        status, body = test_general(self.url, request, 'post')
        self.assertEqual(status, 400)


class ProfileTestCase(TestCase):
    """ Test customer profile. """

    data = {
        'email': 'profile@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'do not fuck',
        'last_name': 'me',
        'tel': '123456789',
        'address': 'the test is awesome'
    }
    url = '/profile/'

    def setUp(self):
        Customer.objects.filter(user__email='profile@test.com').delete()
        test_general('/register/', self.data, 'post')

    def test_normal_profile_info_retrieve(self):
        status, body = test_general(self.url, None, 'get')
        self.assertEqual(status, 200)

    def test_normal_profile_info_update(self):
        pass