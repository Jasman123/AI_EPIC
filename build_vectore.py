from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from generate_pdf import load_pdf

PDF_PATH = "documents\\Big data analytics—A review of data-mining models for small.pdf"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "pdf_docs"


def load_vector_store(embeddings):
    vector_store = Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )
    return vector_store

def build_vector_store(documents, embeddings):
    vector_store = Chroma.from_documents(
        documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )
    vector_store.persist()
    return vector_store


def get_vector_store(embeddings):
    if os.path.exists(CHROMA_DIR):
        return load_vector_store(embeddings)

    documents = load_pdf(PDF_PATH)
    return build_vector_store(documents, embeddings)
