from openai import OpenAI
import openai
from typing_extensions import override
from django.conf import settings

class ConversationAssistant:
    assistant_id = None
    thread_id = None
    username = "User"

    def __init__(self, assistant_id=None, thread_id=None, username=username):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )
        self.assistant_id = assistant_id
        self.thread_id = thread_id
        self.username = username
        if self.assistant_id is None or self.thread_id is None:
            self.thread_id, self.assistant_id = self.create_assistant_for_user()
        else:
            self.thread_id = self.thread_id
            self.assistant_id = self.assistant_id

    def create_assistant_for_user(self):

        assistant = self.client.beta.assistants.create(
            name="The Conversationalist",
            instructions="You are a general conversationalist.Use your knowledge base to converse with the user. Do give long answers unless necessary."
            ,
            tools=[{"type": "retrieval"}],
            model="gpt-3.5-turbo",
        )

        thread = self.client.beta.threads.create()

        return thread.id, assistant.id

    def send_message(self, message,user_input_classification):

        try:
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id, role="user", content=message
            )
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
                instructions="""
                    Users will expect you to be able to answer general questions and engage in casual conversation.
                    The users' input may either be classified as a question, greeting, or end of conversation.
                    You should respond appropriately to each classification.
                    The classification of the user input will be provided to you.
                    The current user input classification is {}.
                """.format(user_input_classification),
            )
        except openai.APIError as e:
            return 400, f"OpenAI API returned an API Error: {e}"
        except openai.APIConnectionError as e:
            return 500, f"Failed to connect to OpenAI API: {e}"
        except openai.RateLimitError as e:
            return 429, f"OpenAI API request exceeded rate limit: {e}"
        except openai.AuthenticationError as e:
            return 401, f"OpenAI API request failed due to authentication error: {e}"
        except openai.NotFoundError as e:
            return 404, f"OpenAI API request failed due to not found error: {e}"

        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id,
        )
        message_text = self.extract_message_value(messages.data[0])
        return 201, message_text

    def extract_message_value(self, message):
        return message.content[0].text.value
