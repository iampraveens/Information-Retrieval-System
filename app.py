import streamlit as st
from src.helper import (get_pdf_text, get_text_chunks, get_embeddings,
                        get_vectorstore, get_conversation_chain)
from htmlTemplate import css, bot_template, user_template, web_styles



def handle_user_input(user_query):
    """
    Handle user input by passing it to the conversational retrieval chain,
    saving the response to the session state, and then displaying the
    conversation history in the Streamlit app.

    Parameters
    ----------
    user_query : str
        The user's query to be passed to the conversational retrieval chain.
    """
    response = st.session_state.conversation({"question": user_query})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    """
    The main entry point of the application. This function is responsible for
    generating the Streamlit UI and handling user input. When the user submits
    a PDF file and a query, it processes the PDF file, chunks the text into
    smaller pieces, generates embeddings for the chunks, creates a vectorstore
    from the embeddings, creates a conversational retrieval chain from the
    vectorstore, and then uses the chain to generate a response to the user's
    query.
    """
    web_styles()
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_hstory" not in st.session_state:
        st.session_state.chat_history = None
        
    user_query = st.chat_input("Ask a question from the uploaded PDF file")
    if user_query:
        handle_user_input(user_query)
    
    with st.sidebar:
        st.title("☰ Menu")
        with st.form("upload_and_query_form"):
                pdf_docs = st.file_uploader(
                    "Upload your PDF file and enter your question below",
                    accept_multiple_files=True, 
                    type=["pdf"]
                )
                
                submit_button = st.form_submit_button("Submit")
                    
                if submit_button:
                    with st.spinner("Processing..."):
                        pages = get_pdf_text(uploaded_files=pdf_docs)
                        chunks = get_text_chunks(pages=pages)
                        embeddings = get_embeddings()
                        vectorstore = get_vectorstore(chunks=chunks, embeddings=embeddings)
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.success("Processing completed!")
                
if __name__ == "__main__":
    main()