from django.test import TestCase
from URLShortener.management.commands import create_fake_users
from URLShortener import views, models
from mock import Mock
from django.test import Client

class URLShortenerTestCase(TestCase):
    def setUp(self):
        models.RandomUsers.objects.create_user(
            username = 'test_username',
            first_name = 'test_first_name',
            last_name = 'test_last_name',
            email = 'test_email',
            password = 'test_password'
        )

        self.client = Client()

    def test_randomuserAPI_checking_correctness_of_external_API(self):
        cmd = create_fake_users.Command()
        users = cmd.get_users(100)
        self.assertEqual(len(users), 100)

    def test_urls(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/about')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/contact')
        self.assertEqual(resp.status_code, 200)

    def test_get_unique_id(self):
        #Creating a URL and short URL for the test user
        random_user_instance = models.RandomUsers.objects.get(username = 'test_username')
        obtainedRecord, isCreated = models.UserURLS.objects.get_or_create(
            user_url = 'https://bitly.com/',
            defaults={
                'user': random_user_instance,
                'short_url' : 'A'
             }
        )

        #Running assertion
        views.SHORT_URL_MAX_LEN = 1
        views.uuid4 = Mock(return_value = 'A')
        self.assertEqual(views.get_unique_id(1), '-1')

        views.uuid4 = Mock(return_value = 'B')
        self.assertEqual(views.get_unique_id(1), 'B')

    def test_index(self):
        pass
        