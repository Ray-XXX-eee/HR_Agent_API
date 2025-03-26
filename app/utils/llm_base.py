from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from app.config.config import DEFAULT_MODEL, DEFAULT_TEMPERATURE,GROQ_API_KEY
from app.doc_processor.new_doc_processor import document_processor

class BaseInference:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE):
        self.model_name = model_name
        self.temperature = temperature

    def _get_llm(self):
        return ChatGroq(model=self.model_name, temperature=self.temperature,api_key=GROQ_API_KEY)

    def agent_answer(self, base_prompt: str, user_prompt: str):
        """Answers a query based on the retrieved document context."""
        if not document_processor.vectors:
            raise ValueError("No document vectors available. Please upload and process a document first.")

        llm = self._get_llm()
        base_prompt = ChatPromptTemplate.from_template(base_prompt)

        document_chain = create_stuff_documents_chain(llm, base_prompt)
        retriever = document_processor.vectors.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        response = retrieval_chain.invoke({"input": user_prompt})
        return response
