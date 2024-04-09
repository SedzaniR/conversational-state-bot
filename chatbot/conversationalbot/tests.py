from django.test import TestCase
from django.contrib.auth.models import User
from .models import Log, Step, UserMeta
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class LogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user_meta = UserMeta.objects.create(user=self.user, state='greeting')

    def test_update_state_signal(self):
        state = 'greeting'
        log_entry = Log.objects.create(
            user=self.user,
            user_input='Test input',
            bot_response='Test response',
            state=state
        )

      
        user_step = Step.objects.get(user_meta=self.user_meta)
        self.assertEqual(user_step.user_meta.state, state)

class UserChatApiViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.user_meta = UserMeta.objects.create(user=self.user, state='greeting')
    def test_get_user_logs(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        
        log_entry = Log.objects.create(
            user=self.user_meta,
            user_input='Test input',
            bot_response='Test response',
            state='question'
        )
        
        response = client.get('http://127.0.0.1:8000/conversationalbot/chat/') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  

    def test_create_session_and_log(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        
        data = {'message': 'Test message'}  
        
        response = client.post('http://127.0.0.1:8000/conversationalbot/chat/', data=data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user_input', response.data)
        self.assertIn('bot_response', response.data)
        self.assertIn('state', response.data)