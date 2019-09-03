from django.test import TestCase
from unittest.mock import patch
from django.test import Client
from .models import Priority
from .models import Task
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth

# Create your tests here.

dict = {
    'pagination': {
        'object_count': 0
    },
    'events': []
}

GENERIC_PASSWORD = '1234'
class TestModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.high_priority = Priority.objects.create(name='HIGH')

        self.user_without_social = User.objects.create_user(username='nn', password=GENERIC_PASSWORD)
        self.user_with_social = User.objects.create_user(username='nicolas', password=GENERIC_PASSWORD)
        UserSocialAuth.objects.create(
            user=self.user_with_social,
            provider='eventbrite',
            uid='1233543645',
            extra_data={
                'auth_time': 1567127106,
                'access_token': 'testToken',
                'token_type': 'bearer',
            }
        )

    def test_priority(self):
        self.assertEqual('HIGH', self.high_priority.name)

    def test_login(self):
        response = self.client.post('/', {
            'username': self.user_without_social.username,
            'password': GENERIC_PASSWORD
        })
        self.assertEqual(302, response.status_code)

    def test_wrong_password(self):
        self.assertFalse(self.client.login(username='nicolas', password='123'))
        self.client.logout()

    @patch('task_app.views.Eventbrite.get', return_value=dict)
    def test_get_events(self, mocked_get):
        self.client.force_login(self.user_with_social)
        self.client.get('/events/?page=4')
        mocked_get.assert_called_with('/users/me/events?page_size=5&page=4')
        self.client.logout()

    def test_get_events_user_without_social(self):
        self.client.force_login(self.user_without_social)
        response = self.client.get('/events/')
        events = len(response.context_data['object_list'].api_result['events'])
        self.assertEqual(events, 0)
        self.client.logout()

    def test_create_a_task(self):
        self.client.force_login(self.user_with_social)
        url = '/events/1234/tasks/create/'
        response_post = self.client.post(url, {
            'name': 'TestTask',
            'priority': 1,
            'done': 'on'
        })
        response_get = self.client.get('/events/1234/tasks')
        self.assertEqual(302, response_post.status_code)
        self.assertEqual(1, len(response_get.context_data['object_list']))

    # def test_delete_a_task(self):
    #     url = '/events/1234/tasks/create/'
    #     self.client.post(url, {
    #         'name': 'TestTask',
    #         'priority': 1,
    #         'done': 'on'
    #     })
    #     pass
