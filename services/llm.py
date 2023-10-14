import os

import random

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI


PERSIST_DIRECTORY = './data/'

async def save_file(file):
    """
        save the file in a temp space
    """
    try:
        file_content = await file.read()
        file_name = str(random.randint(0, 999)) + "_" + file.filename
        file_path = f"tmp/{file_name}"
        with open(file_path, "wb") as f:
            f.write(file_content)
    except Exception as e:
        print(e)
        raise Exception('error save_file')
    return file_path, file_name

def delete_file(path):
    """
        delete the file
    """
    try:
        os.remove(path)
    except OSError as e:
        print(f"Error deleting the file: {e}")
        raise Exception('delete_file')

async def load_file(file):
    """
        Load and vectorize file
    """
    try:
        path, file_name = await save_file(file)
        pdf_loader = PyPDFLoader(path)
        documents = pdf_loader.load()
        document = split_document(documents)
        vector_db = store_index(document, file_name)
    except Exception as e:
        raise Exception(e)
    finally:
        if path:
            delete_file(path)
    return file_name, file.filename

def split_document(documents):
    """
        Split in chunks
    """
    text_splitter = CharacterTextSplitter(chunk_size=1_000, chunk_overlap=200)
    documents = text_splitter.split_documents(documents)
    return documents

def store_index(documents, file_name):
    """
        sotre the embedded document in vectorize db
    """
    vectordb = Chroma.from_documents(
        documents,
        embedding=OpenAIEmbeddings(),
        persist_directory=PERSIST_DIRECTORY + file_name
    )
    vectordb.persist()
    return vectordb

def load_index(path):
    """
        load the embedded docuement
    """
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY + path,
        embedding_function=OpenAIEmbeddings()
    )
    return vectordb

def ask(path, question, history=None):
    vector_db = load_index(path)
    qa_chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(),
        vector_db.as_retriever(search_kwargs={'k': 6}),
        return_source_documents=True
    )
    question_object = {
        'question': question,
        'chat_history':[]
    }
    if history:
        question_object['chat_history'] = history
    result = qa_chain(question_object)
    return result['answer']
