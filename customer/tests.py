from django.test import TestCase
from customer.models import Customer
import copy
from .util import test_general


class RegisterExceptionHandlingTestCase(TestCase):
    """ Test customer registration exception. """

    data = {
        'email': 'exception_test@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'fuck',
        'last_name': 'me',
        'tel': '123456789',
        'address': 'the test is awesome'
    }
    fields = ['email', 'password', 'password_confirmation', 'first_name', 'last_name', 'tel', 'address']
    url = '/register/'

    def setUp(self):
        Customer.objects.filter(user__email='exception_test@test.com').delete()

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


class NormalRegisterTestCase(TestCase):
    """ Test normal customer registration procedural. """

    data = {
        'email': 'normal_test@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'do not fuck',
        'last_name': 'me',
        'tel': '123456789',
        'address': 'the test is awesome'
    }
    url = '/register/'

    def setUp(self):
        Customer.objects.filter(user__email='normal_test@test.com').delete()

    def test_normal_register(self):
        status, body = test_general(self.url, self.data, 'post')
        self.assertEqual(status, 200)


class NormalLoginTestCase(TestCase):
    """ Test customer normal login. """

    data = {
        'email': 'normal_test@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'do not fuck',
        'last_name': 'me',
        'tel': '123456789',
        'address': 'the test is awesome'
    }
    url = '/register/'

    def setUp(self):
        Customer.objects.filter(user__email='normal_test@test.com').delete()
        test_general(self.url, self.data, 'post')

    def test_normal_login(self):
        pass
