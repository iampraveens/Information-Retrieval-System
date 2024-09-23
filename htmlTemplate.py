import requests
from io import BytesIO
from PIL import Image
import streamlit as st

css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/n71P4k0/Gemini-Generated-Image-8dg7f08dg7f08dg7.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/0sPjcBq/Untitled-design-3.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

def web_styles():
    """
    Set the layout and appearance of the Streamlit web interface.

    This function sets the page title, page icon, and layout of the Streamlit web interface. 
    It also hides the main menu, footer, and header of the page.
    """
    url = "https://cdn-icons-png.flaticon.com/512/9422/9422946.png"
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    page_title = 'Information Retrieval System - A RAG Application'
    page_icon = image
    layout = 'centered'

    st.set_page_config(page_title=page_title,
                    page_icon=page_icon,
                    layout=layout
                    )

    hide_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                <style>
                
                '''
    header_style = '''
                <style>
                .navbar {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    z-index: 1;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 80px;
                    background-color: #475063;
                    box-sizing: border-box;
                }
                
                .navbar-brand {
                    color: white !important;
                    font-size: 23px;
                    text-decoration: none;
                    margin-right: auto;
                    margin-left: 50px;
                }
                
                .navbar-brand img {
                    margin-bottom: 6px;
                    margin-right: 1px;
                    width: 40px;
                    height: 40px;
                    justify-content: center;
                }
                
                /* Add the following CSS to change the color of the text */
                .navbar-brand span {
                    color: #EF6E04;
                    justify-content: center;
                }
                
                </style>
                
                <nav class="navbar">
                    <div class="navbar-brand">
                    <img src="https://cdn-icons-png.flaticon.com/512/9422/9422946.png" alt="Logo">
                        Information Retrieval System - A RAG Application
                    </div>
                </nav>
                '''
    st.markdown(hide_style, unsafe_allow_html=True)
    st.markdown(header_style, unsafe_allow_html=True)