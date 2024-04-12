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
from conversationalbot.utils import hugging_face_zero_shot_free, rest_error_response_codes

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
        Log.objects.create(
            user=self.user,
            user_input="Test input",
            bot_response="Test response",
            state="greeting",
        )

    def retrieve_user_logs(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get("/api/chat")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_authentication_required(self):
        
        self.client.logout()
        response = self.client.get('/api/chat')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        
    def test_create_session_and_log(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        data = {"message": "Test message"}

        response = client.post("/api/chat/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user_input", response.data)
        self.assertIn("bot_response", response.data)
        self.assertIn("state", response.data)
        self.assertIn("user", response.data)

    

class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.password = "test_password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_user_login_valid_credentials(self):
        response = self.client.post(
            reverse("conversationalbot:user_login"),
            {"username": self.username, "password": self.password},
        )
        self.assertEqual(response.status_code, 302)  # Expecting redirect
        self.assertRedirects(response, reverse("conversationalbot:conversation"))

    def test_user_login_invalid_credentials(self):
        response = self.client.post(
            reverse("conversationalbot:user_login"),
            {"username": "invalid", "password": "invalid"},
        )
        self.assertContains(response, "Invalid username or password.")


class ConversationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.password = "test_password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_conversation_authenticated_user(self):

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("conversationalbot:conversation"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat.html")

    def test_conversation_unauthenticated_user(self):

        response = self.client.get(reverse("conversationalbot:conversation"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/")


class HuggingFaceTestCase(TestCase):
    def test_hugging_face_zero_shot_free(self):
        user_input = "How are you?"
        label = hugging_face_zero_shot_free(user_input)
        # Assuming the model returns one of the candidate labels
        self.assertTrue(
            label == "greeting"
            or label == "question"
            or label == "end"
            or label == None
        )

    def send_a_non_string_type(self):
        # expect it not to classify since it is not a text
        user_input = 123
        label = hugging_face_zero_shot_free(user_input)
        self.assertTrue(label == None)


class AssistantTestCase(TestCase):

    def test_incorrect_thread_id_and_assistant_id(self):

        #raises exception for an incorrect thread_id or assistant_id
        assistant = ConversationAssistant(
            assistant_id="some gibberish", thread_id="hogwash", username="sedzani"
        )
        code, message = assistant.send_message("Hello", "greeting")

        self.assertEqual(code, 400)


class TestErrorResponseCodes(TestCase):

    def test_http_400_bad_request(self):
        self.assertEqual(rest_error_response_codes(400), status.HTTP_400_BAD_REQUEST)

    def test_http_404_not_found(self):
        self.assertEqual(rest_error_response_codes(404), status.HTTP_404_NOT_FOUND)

    def test_http_401_unauthorized(self):
        self.assertEqual(rest_error_response_codes(401), status.HTTP_401_UNAUTHORIZED)

    def test_http_500_internal_server_error(self):
        self.assertEqual(rest_error_response_codes(500), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_other_error_codes(self):
        self.assertEqual(rest_error_response_codes(403), status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(rest_error_response_codes(405), status.HTTP_500_INTERNAL_SERVER_ERROR)