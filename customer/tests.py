from django.test import TestCase
from django.urls import reverse
from customer.models import Customer
import copy
from .util import test_general


class RegisterTestCase(TestCase):
    """ Test normal customer registration procedural. """

    auth = {
        'email': 'register@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'register',
        'last_name': 'test'
    }
    customer = {
        'tel': '123456789',
        'address': 'the test is awesome'
    }
    data = {
        'auth': auth,
        'customer': customer,
    }
    fields = ['email', 'password', 'password_confirmation', 'first_name', 'last_name', 'tel', 'address']
    url = reverse('customer_register')

    def setUp(self):
        Customer.objects.filter(user__email='register@test.com').delete()

    def test_normal_register(self):
        status, body = test_general(self.url, self.data, 'post')
        self.assertEqual(status, 200)

    def test_fields_blank_exception(self):
        request = copy.deepcopy(self.data)
        for field in self.fields:
            key = 'auth' if field in self.auth else 'customer'
            request[key].pop(field, None)
            status, body = test_general(self.url, request, 'post')
            self.assertEqual(status, 400)
            request[key].update({field: self.data[key][field]})

    def test_email_exist_exception(self):
        request = copy.deepcopy(self.data)
        test_general(self.url, request, 'post')
        status, body = test_general(self.url, request, 'post')
        self.assertEqual(status, 400)

    def test_password_mismatch_exception(self):
        request = copy.deepcopy(self.data)
        request['auth']['password_confirmation'] = '/.,buz'
        status, body = test_general(self.url, request, 'post')
        self.assertEqual(status, 400)


class LoginTestCase(TestCase):
    """ Test customer normal login. """

    data = {
        'auth': {
            'email': 'login@test.com',
            'password': '/.,buz123',
            'password_confirmation': '/.,buz123',
            'first_name': 'login',
            'last_name': 'test'
        },
        'customer': {
            'tel': '123456789',
            'address': 'the test is awesome'
        }
    }
    url = reverse('customer_login')

    def setUp(self):
        Customer.objects.filter(user__email='login@test.com').delete()
        test_general(reverse('customer_register'), self.data, 'post')

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
        'auth': {
            'email': 'profile@test.com',
            'password': '/.,buz123',
            'password_confirmation': '/.,buz123',
            'first_name': 'profile',
            'last_name': 'test'
        },
        'customer': {
            'tel': '123456789',
            'address': 'the test is awesome'
        }
    }
    url = reverse('customer_profile')

    def setUp(self):
        Customer.objects.filter(user__email='profile@test.com').delete()
        test_general(reverse('customer_register'), self.data, 'post')
        self.id = Customer.objects.get(user__email='profile@test.com').id

    def test_normal_profile_info_retrieve(self):
        # TODO: Retrieve data with customer id.
        pass

    def test_normal_profile_info_update(self):
        pass