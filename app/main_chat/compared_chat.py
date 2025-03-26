from fastapi import HTTPException
from app.utils.llm_base import BaseInference
from app.doc_processor.doc_processor import DocumentProcessor,document_processor

base_inference = BaseInference()

def compared_chat_response(user_prompt: str):
    """Handles user input and generates an LLM-based response based on document type."""
    try:
        if not document_processor.vectors:
            raise HTTPException(status_code=400, detail="No processed document found. Please upload a document first.")

        # Separate JD & CV contexts
        jd_context = ""
        cv_context = ""

        for doc in document_processor.final_doc:
            if "jd_files" in doc.metadata["source"]:
                jd_context += doc.page_content + "\n"
            elif "cv_files" in doc.metadata["source"]:
                cv_context += doc.page_content + "\n"

        # Determine which engine to use based on the question
        if "skill match" in user_prompt.lower() or "candidate vs jd" in user_prompt.lower():
            prompt_template = """
                You are an expert Recruitment/HR assistant analyzing a **Job Description (JD) and a Resume (CV)**. 
                You must **treat them as separate entities** and perform the following:
                
                - Compare **required skills** from the JD with the skills listed in the CV.
                - Highlight **matches**, **gaps**, and **additional relevant skills**.
                - Provide a **structured candidate vs JD analysis report**.

                <Job Description (JD)>
                {jd_context}
                </Job Description (JD)>

                <Candidate Resume (CV)>
                {cv_context}
                </Candidate Resume (CV)>

                Now, answer the following user query:
                Question: {input}
            """
        else:
            # Default context-aware prompt
            prompt_template = """
                You are an expert Recruitment/HR assistant helping with document-based queries.
                Consider the following **context**, extracted from the uploaded documents:
                
                <Context>
                {context}
                </Context>

                Provide a **point-wise detailed explanation** with examples where needed.
                Question: {input}
            """

        # Select the correct context
        context = jd_context + cv_context if jd_context and cv_context else jd_context or cv_context

        response = base_inference.agent_answer(
            base_prompt=prompt_template,
            user_prompt=user_prompt,
            context=context
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
