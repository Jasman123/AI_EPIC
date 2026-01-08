from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from pathlib import Path

def load_pdf(file_path: str) -> list:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path.resolve()}")
    
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    for i in range(len(docs)):
        docs[i].page_content =' '.join(docs[i].page_content.split())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    pages_splitter = text_splitter.split_documents(docs)
    return pages_splitter


if __name__ == "__main__":
    file_path = "AI_EPIC\\documents\\Big data analytics—A review of data-mining models for small.pdf" 
    pages = load_pdf(file_path)
    print(f"Total pages after splitting: {len(pages)}")
    # for i, page in enumerate(pages):
    #     print(f"Page {i+1}:\n{page.page_content}\n")
    