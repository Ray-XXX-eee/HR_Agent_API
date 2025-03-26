from pydantic import BaseModel
from typing import Any

class ChatRequest(BaseModel):
    user_prompt: str

class JDRequest(BaseModel):
    job_description: str

class CVRequest(BaseModel):
    resume_text: str
