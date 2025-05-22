import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pyprojroot import here

def convert_pdfs_to_chroma(pdf_dir: str, vectordb_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200, embedding_model: str = "text-embedding-ada-002", collection_name: str = "papers_vectordb"):
    """
    Converts PDFs in a directory into text chunks and saves them as a Chroma vector database.

    Parameters:
        pdf_dir (str): Directory containing PDF files.
        vectordb_dir (str): Directory to save the Chroma vector database.
        chunk_size (int): Maximum size of each text chunk. Default is 1000.
        chunk_overlap (int): Overlap size between consecutive chunks. Default is 200.
        embedding_model (str): Name of the embedding model to use. Default is "text-embedding-ada-002".
        collection_name (str): Name of the Chroma collection. Default is "papers_vectordb".
    """
    # Load PDFs and extract text
    pdf_texts = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(pdf_dir, filename)
            loader = PyPDFLoader(file_path)
            documents = loader.load_and_split()
            pdf_texts.extend(documents)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(pdf_texts)

    # Save chunks to Chroma vector database
    if not os.path.exists(vectordb_dir):
        os.makedirs(vectordb_dir)

    vectordb = Chroma.from_documents(
        documents=chunks,
        collection_name=collection_name,
        embedding=OpenAIEmbeddings(model=embedding_model),
        persist_directory=vectordb_dir
    )
    vectordb.persist()

    print(f"Chroma vector database saved to {vectordb_dir}.")
    print(f"Number of vectors in the database: {vectordb._collection.count()}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # Define paths and parameters
    pdf_dir = str(here("data/papers"))
    vectordb_dir = str(here("data/papers_vectordb"))
    chunk_size = 1000
    chunk_overlap = 200
    embedding_model = "text-embedding-ada-002"
    collection_name = "papers_vectordb"

    # Run the conversion
    convert_pdfs_to_chroma(
        pdf_dir=pdf_dir,
        vectordb_dir=vectordb_dir,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        embedding_model=embedding_model,
        collection_name=collection_name
    )
