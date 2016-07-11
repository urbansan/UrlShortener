from django.test import TestCase
from URLShortener.management.commands import create_fake_users
from URLShortener.views import *
from mock import Mock

class AnimalTestCase(TestCase):
    def setUp(self):
        pass

    def test_randomuserAPI_correctness(self):
        cmd = create_fake_users.Command()
        users = cmd.get_users(100)
        self.assertEqual(len(users), 100)

    def test_get_unique_id(self):
        pass