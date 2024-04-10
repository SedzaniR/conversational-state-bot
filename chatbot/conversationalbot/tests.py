from django.test import TestCase
from django.contrib.auth.models import User
from .models import Log, Step, UserMeta
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from conversationalbot.api import ConversationAssistant
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse

class UserMetaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")

    def test_user_meta_str(self):
        user_meta = UserMeta.objects.get(user=self.user)
        self.assertEqual(self.user.id, user_meta.user.id)


class LogTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test_user_log")

    def test_update_state_signal(self):
        state = "greeting"
        Log.objects.create(
            user=self.user,
            user_input="Test input",
            bot_response="Test response",
            state=state,
        )

        user_meta = UserMeta.objects.get(user=self.user)
        user_step = Step.objects.get(user_meta=user_meta)
        self.assertEqual(user_step.user_meta.state, state)


class UserChatApiViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="password123"
        )

    def test_create_session_and_log(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        data = {"message": "Test message"}

        response = client.post(
            "http://127.0.0.1:8000/conversationalbot/chat/", data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user_input", response.data)
        self.assertIn("bot_response", response.data)
        self.assertIn("state", response.data)



class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.password = "test_password"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_login_valid_credentials(self):
        response = self.client.post(reverse("conversationalbot:user_login"), {"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, 302)  # Expecting redirect
        self.assertRedirects(response, reverse("conversationalbot:conversation"))

    def test_user_login_invalid_credentials(self):
        response = self.client.post(reverse("conversationalbot:user_login"), {"username": "invalid", "password": "invalid"})
        
        print('this is the res[psme', response.reason_phrase)
        self.assertEqual(response.status_code, 302)  # Expecting redirect
        self.assertRedirects(response, reverse("conversationalbot:user_login"))
    
       
class ConversationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.password = "test_password"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_conversation_authenticated_user(self):
    
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("conversationalbot:conversation"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat.html")

    def test_conversation_unauthenticated_user(self):
     
        response = self.client.get(reverse("conversationalbot:conversation"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/conversationalbot/login/?next=/conversationalbot/conversation/')