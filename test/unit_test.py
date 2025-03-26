import requests
from app.doc_processor.doc_processor import DocumentProcessor
from app.main_chat.base_chat_service import base_chat_response

API_URL = "http://localhost:8000"

def test_upload_document():
    """Test document upload and processing."""
    file_path = "sample_resume.pdf"  # Make sure to have a test PDF file in the same directory
    processor = DocumentProcessor()
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "application/pdf")}
        # response = processor.process_document(file_path)
        response = requests.post(f"{API_URL}/process_document", files=files)
        print('test_1',response.content)
    print("Upload Response:", response.status_code, response.content)
    return response
    

def test_chat():
    """Test the chatbot API."""
    payload = {"user_prompt": "what is this document about ? also extract the contact details"}
    response = requests.post(f"{API_URL}/chat", json=payload)
    
    answer = response.json().get("answer","no answer") 
    print("Chat Response:", answer) #response.status_code
    

if __name__ == "__main__":
    test_upload_document()
    # print('main print : ',vector)
    test_chat()