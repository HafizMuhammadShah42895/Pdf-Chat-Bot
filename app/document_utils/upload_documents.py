# app/document_utils/upload_documents.py

import os
import re
import uuid
from PIL import Image
import pytesseract
import pickle
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# ---------- Clean Text ----------
def clean_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'[\r\n]+', '\n', text)
    text = re.sub(r'\n{2,}', '\n\n', text)
    text = text.replace('\x0c', '')
    return text

# ---------- OCR ----------
def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return clean_text(text)
    except Exception as e:
        print(f"❌ Failed to process image {file_path}: {e}")
        return ""

# ---------- Main Upload Function ----------
def process_and_store_documents(folder_path, vector_store_path):
    embeddings = OllamaEmbeddings(model="llama3")
    documents = []
    image_extensions = ('.png', '.jpg', '.jpeg')

    # Load text docs
    loader = UnstructuredFileLoader(folder_path)
    raw_docs = loader.load()
    for doc in raw_docs:
        cleaned = clean_text(doc.page_content)
        if cleaned:
            documents.append(Document(page_content=cleaned, metadata=doc.metadata))

    # OCR for images
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(image_extensions):
                ocr_text = extract_text_from_image(file_path)
                if ocr_text:
                    documents.append(Document(page_content=ocr_text, metadata={"source": file_path}))

    # Split & embed
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(documents)

    # Optional: Save chunks
    with open(os.path.join(vector_store_path, "bm25_chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=vector_store_path
    )
    vectorstore.persist()
    return len(chunks)
