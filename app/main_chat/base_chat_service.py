from fastapi import HTTPException
from app.utils.llm_base import BaseInference
from app.doc_processor.new_doc_processor import DocumentProcessor,document_processor

base_inference = BaseInference()

def base_chat_response(user_prompt: str):
    """Handles user input and generates an LLM-based response."""
    try:
        if not document_processor.vectors:
            raise HTTPException(status_code=400, detail="No processed document found. Please upload a document first.")

        prompt_template = """
            You are an expert Recruitment/HR knowledge assistant who can answer to the point about the
            <context>
            {context}
            <context>
            with comprehensive point-wise explanation and complete examples if needed with 
            respect to the following user question:
            Question: {input}
        """
        response = base_inference.agent_answer(
            base_prompt=prompt_template,
            user_prompt=user_prompt
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
