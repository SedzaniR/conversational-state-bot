from django.conf import settings
import requests
from conversationalbot.models import STATE
from rest_framework import status

def hugging_face_zero_shot_free(user_input):

    API_TOKEN = settings.HUGGING_FACE_TOKEN
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    candidate_labels = [item[0] for item in STATE]
    payload = {
        "inputs": user_input,
        "parameters": {"candidate_labels": candidate_labels},
    }
    try:
        response = requests.post(url=API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("labels")[0]
    except Exception as e:
        return None

def rest_error_response_codes(code):

    if code == 400:
        return status.HTTP_400_BAD_REQUEST
    elif code == 404:
        return status.HTTP_404_NOT_FOUND
    elif code == 401:
        return status.HTTP_401_UNAUTHORIZED
    else:
        return status.HTTP_500_INTERNAL_SERVER_ERROR