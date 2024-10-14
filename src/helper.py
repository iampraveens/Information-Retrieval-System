import os
import tempfile
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_together import Together
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

def get_pdf_text(uploaded_files):
    """Takes a list of uploaded PDF files, reads their contents, and returns
    the text of all the pages in all the files.

    Args:
        uploaded_files: A list of file objects, each containing a PDF file
            to be read.

    Returns:
        A list of strings, where each string is the text of a page from the
            PDF files. The order of the strings is the same as the order of
            the uploaded files, and the pages within each file are in the order
            they appear in the file.
    """
    all_pages = []
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        loader = PyPDFLoader(file_path=tmp_file_path)
        pages = loader.load()
        all_pages.extend(pages)
        os.unlink(tmp_file_path)  # Clean up the temporary file
    return all_pages

def get_text_chunks(pages):
    """Takes a list of strings, each string being the text of a page from
    a PDF file, and breaks them up into smaller chunks of text.

    Args:
        pages: A list of strings, where each string is the text of a
            page from the PDF file.

    Returns:
        A list of strings, where each string is a chunk of text from the
        pages. The order of the strings is the same as the order of
        the pages, and the chunks within each page are in the order
        they appear in the page.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500, chunk_overlap = 200, 
        length_function=len, separators=['\n\n', '\n', ' ', '']
    )
    chunks = text_splitter.split_documents(pages)
    
    return chunks

def get_embeddings():
    """Gets the embeddings model for use in generating vectors from text.

    Returns:
        An instance of GoogleGenerativeAIEmbeddings, which is a model for generating
            vectors from text.
    """
    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=GOOGLE_API_KEY, 
                                              model="models/embedding-001")
    
    return embeddings

def get_vectorstore(chunks, embeddings):
    """Gets a vectorstore from a list of text chunks and an embeddings model.

    Args:
        chunks: A list of strings, where each string is a chunk of text from the
            pages of the PDF file.
        embeddings: An instance of GoogleGenerativeAIEmbeddings, which is a model
            for generating vectors from text.

    Returns:
        An instance of FAISS, which is a vectorstore that can be used for
        similarity searches.
    """
    vectorstore = FAISS.from_documents(documents=chunks, 
                                       embedding=embeddings)
    
    return vectorstore

def get_conversation_chain(vectorstore):
    
    """Gets a conversational retrieval chain from a vectorstore.

    Args:
        vectorstore: An instance of FAISS, which is a vectorstore that can be used
            for similarity searches.

    Returns:
        An instance of ConversationalRetrievalChain, which is a chain that can be
            used to generate text based on a prompt, where the generated text is
            informed by the vectorstore.
    """
    llm = Together(model="google/gemma-2-27b-it", 
                   api_key=TOGETHER_API_KEY, max_tokens=512)
    memory = ConversationBufferMemory(memory_key= "chat_history", 
                                      return_messages=True)
    conversation = ConversationalRetrievalChain.from_llm(llm=llm, 
                                        retriever=vectorstore.as_retriever(), memory=memory)
    
    return conversation
