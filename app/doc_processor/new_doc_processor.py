import os
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config.config import DEFAULT_EMBEDDING_MODEL
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


class DocumentProcessor:
    def __init__(self):
        self.vectors = None  # Store vectors globally
        self.pages = None
        self.final_doc = None

    def process_document(self, file_path: str):
        
        # file_path = os.path.join(DATA_DIR, f"{time.time()}_file.pdf")
        """Process a PDF file, split its text into chunks, and create a vector embedding."""
        print("Processing document...")
        start_time = time.time()
        
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        self.final_doc = text_splitter.split_documents(docs)
        self.num_pages = {doc.metadata['source']: doc.metadata.get('page', 0) + 1 for doc in docs}

        print("Creating vector store...")
        embeddings = GoogleGenerativeAIEmbeddings(model=DEFAULT_EMBEDDING_MODEL,google_api_key=GOOGLE_API_KEY)
        self.vectors = FAISS.from_documents(self.final_doc, embeddings)

        elapsed_time = time.time() - start_time
        print(f"Vectorstore is ready! Processed in {elapsed_time:.2f} seconds.")
        # return self.vectors,self.num_pages,self.final_doc
# Global instance to store document vectors
document_processor = DocumentProcessor()
