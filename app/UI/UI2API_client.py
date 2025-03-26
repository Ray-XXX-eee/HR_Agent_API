import os
from pprint import pprint
from typing import Any
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

__BASE_API_URL = os.getenv("BASE_API_URL")
__UPLOAD_ENDPOINT = os.getenv("UPLOAD_ENDPOINT")
__CHAT_ENDPOINT = os.getenv("CHAT_ENDPOINT")

def API_upload_doc(files: Any) -> str:
    """Document upload and processing."""
    files = {"file": (files.name, files.getbuffer(), "application/pdf")}
    response = requests.post(f"{__BASE_API_URL}/{__UPLOAD_ENDPOINT}", files=files)
  
    response_json = response.json()  # Store JSON response once to avoid multiple calls
    st.session_state.final_doc = response_json.get("final_doc", [])[0].get("page_content", 'no data')  # Ensure it's a list
    st.session_state.metadata = response_json.get("pages", {})  # Ensure it's a dict

    print("Upload Response:", response.status_code)

    return response_json.get("message", "No message received.")

import requests

def API_upload_doc_multi(files: dict):
    responses = []  # Store all responses

    for file_name, (file_obj, file_type) in files.items():
        try:
            # Prepare files and data payload
            upload_files = {"file": (file_name, file_obj.getbuffer(), "application/pdf")}
            data = {"file_type": file_type}  # Send file type (JD or CV)

            # Make API request
            response = requests.post(f"{__BASE_API_URL}/{__UPLOAD_ENDPOINT}", files=upload_files, data=data)

            # Check for valid JSON response
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    responses.append(json_response)
                except requests.exceptions.JSONDecodeError:
                    responses.append({"error": "Invalid JSON response from API"})
            else:
                responses.append({"error": f"Failed with status {response.status_code}"})

        except Exception as e:
            responses.append({"error": str(e)})

    return responses


def API_chat(user_prompt: str):
    """chatbot API."""
    payload = {"user_prompt": user_prompt}
    response = requests.post(f"{__BASE_API_URL}/chat", json=payload)
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("answer", "No answer found")
    else:
        return f"API Error: {response.status_code}"
    
