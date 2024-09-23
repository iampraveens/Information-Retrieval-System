# app.py

import streamlit as st
import time
from src.helper import (
    get_pdf_text, 
    get_text_chunks, 
    get_embeddings,
    get_vectorstore, 
    get_conversation_chain
)

def main():
    st.set_page_config(page_title="Information Retrieval System")
    st.header("Information Retrieval System")
    
    with st.sidebar:
        st.title("Menu")
        
        # Create a form to handle both file upload and query input
        with st.form("upload_and_query_form"):
            pdf_docs = st.file_uploader(
                "Upload your PDF file and enter your question below",
                accept_multiple_files=True, 
                type=["pdf"]
            )
            
            submit_button = st.form_submit_button("Submit")
                 
            if submit_button:
                with st.spinner("Processing..."):
                    time.sleep(5)
                    st.success("Processing completed!")
                    
    user_query = st.text_input("Ask a question from the uploaded PDF file")  
    if user_query:
        try:
            pages = get_pdf_text(uploaded_files=pdf_docs)
            chunks = get_text_chunks(pages=pages)
            embeddings = get_embeddings()
            vectorstore = get_vectorstore(chunks=chunks, embeddings=embeddings)
            conversation = get_conversation_chain(vectorstore)
            # Generate the response to the user's query
            result = conversation({'question': user_query})
            
            st.write("**Question:**", user_query)
            st.write("**Answer:**", result['answer'])
        except Exception as e:
            st.error(f"An error occurred: {e}")
            
                    
    # user_query = st.text_input("Ask a question from the uploaded PDF file")
    # if submit_button:
    #         with st.spinner("Processing..."):
    #             if user_query:
    #                 try:
    #                     # Process the uploaded PDF files
    #                     pages = get_pdf_text(uploaded_files=pdf_docs)
    #                     chunks = get_text_chunks(pages=pages)
    #                     embeddings = get_embeddings()
    #                     vectorstore = get_vectorstore(chunks=chunks, embeddings=embeddings)
    #                     conversation = get_conversation_chain(vectorstore)
    #                     # Generate the response to the user's query
    #                     result = conversation({'question': user_query})
                        
    #                     st.success("Processing completed!")
    #                     st.write("**Question:**", user_query)
    #                     st.write("**Answer:**", result['answer'])
    #                 except Exception as e:
    #                     st.error(f"An error occurred: {e}")
        
                        
if __name__ == "__main__":
    main()
