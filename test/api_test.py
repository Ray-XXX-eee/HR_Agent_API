import requests

API_URL = "http://localhost:8000"

def test_upload_document():
    """Test document upload and processing."""
    file_path = "sample_resume.pdf"  # Make sure to have a test PDF file in the same directory
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "application/pdf")}
        response = requests.post(f"{API_URL}/process_document", files=files)

    print("Upload Response:", response.status_code, response.json())

def test_chat():
    """Test the chatbot API."""
    payload = {"user_prompt": "name of the candidate?"}
    response = requests.post(f"{API_URL}/chat", json=payload)
    
    print("Chat Response:", response.status_code, response.json())

if __name__ == "__main__":
    test_upload_document()
    test_chat()