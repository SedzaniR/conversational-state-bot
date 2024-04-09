
from django.conf import settings
import requests

def hugging_face_zero_shot_free(user_input):
    api_token = settings.HUGGING_FACE_TOKEN
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {api_token}"}
    candidate_labels = [
            'greeting',
            'question',
            'end'    
        ]

    payload = {
    "inputs":user_input,
    "parameters": {"candidate_labels": candidate_labels},
    }
    try:
        response = requests.post(url=API_URL, headers=headers, json=payload)
        if response.status_code == 200:
           
            return response.json().get("labels")[0]
    except Exception as e:
        print(e)
        return None