from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

class ConversationAssistant:
    assistant_id = None
    thread_id = None
    def __init__(self, assistant_id=None, thread_id=None):
        self.client = OpenAI(
            api_key="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"
        )
        self.assistant_id = assistant_id
        self.thread_id = thread_id
        if self.assistant_id is None or self.thread_id is None:
            self.thread_id, self.assistant_id = self.create_assistant_for_user()
        else:
            self.thread_id = self.thread_id
            self.assistant_id = self.assistant_id
    def create_assistant_for_user(self):
        
        assistant = self.client.beta.assistants.create(
            name="The Conversationalist",
            instructions="You are a general conversationalist.Use your knowledge base to best respond to customer queries.",
            tools=[{"type": "retrieval"}],
            model="gpt-3.5-turbo",
            )

        thread = self.client.beta.threads.create()
        
        return thread.id, assistant.id
    
    def send_message(self,message):
        message = self.client.beta.threads.messages.create(
        thread_id=self.thread_id,
        role="user",
        content=message
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            instructions="Please address the user as Sedzani. Use your knowledge base to best respond to customer queries."
            )
      
   
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id,
        )
        message_text = self.extract_message_value(messages.data[0])
        return message_text
    
    def extract_message_value(self, message):
        return message.content[0].text.value
            
 
