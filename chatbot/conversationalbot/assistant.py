from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

class ConversationAssistant:
    
    def __init__(self):
        self.client = OpenAI(
            api_key="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"
        )
        self.thread, self.assistant = self.create_assistant_for_user()
       
    def create_assistant_for_user(self):
        
        assistant = self.client.beta.assistants.create(
            name="The Conversationalist",
            instructions="You are a general conversationalist.Use your knowledge base to best respond to customer queries.",
            tools=[{"type": "retrieval"}],
            model="gpt-3.5-turbo",
            )

        thread = self.client.beta.threads.create()
        
        return thread, assistant
    
    def send_message(self,message):
        message = self.client.beta.threads.messages.create(
        thread_id=self.thread.id,
        role="user",
        content=message
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions="Please address the user as Sedzani. The user has a premium account. No file needs to be uploaded"
            )
      
   
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        message_text = self.extract_message_value(messages.data[0])
        print(message_text)
        return message_text
    

    
    def extract_message_value(self, message):
        return message.content[0].text.value
            
 
