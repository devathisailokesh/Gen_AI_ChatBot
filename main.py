import streamlit as st
import os
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model, gemini_pro_vision_response, embeddings_model_response, gemini_pro_response)
from PIL import Image


# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))


# setting up the page configuration
st.set_page_config(
    page_title= "Gemini AI",
    page_icon = "🧠",
    layout= "centered"
)

with st.sidebar:
    selected =  option_menu(menu_title="Gemini AI",
                            options=["ChatBot",
                                      "Image Captioning",
                                       "Embed text",
                                        "Ask me anything"],
                                       menu_icon='robot',  icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
                                    default_index=0)

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    # If the role is 'model', translate it to 'assistant' for display in Streamlit
    if user_role == 'model':
        return "assistant"
    else:
        # Otherwise, return the role as it is
        return user_role

# Assuming 'selected' is a variable that determines the current selection
if selected == "ChatBot":
    # Load the Gemini-Pro model
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Streamlit page title
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        # Translate the role for Streamlit and create a chat message block
        with st.chat_message(translate_role_for_streamlit(message.role)):
            # Display the text part of the message using Markdown
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro--")

    if user_prompt:
        # Display the user's message
        st.chat_message("user").markdown(user_prompt)
        # Send the user's message to the Gemini-Pro model and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display the response from Gemini-Pro
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


# Image captioning page
if selected == "Image Captioning":

    # Streamlit page title
    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):

        image  = Image.open(uploaded_image)

        col1, col2 =  st.columns(2)

        with col1:
            resized_image = image.resize((800,500))
            st.image(resized_image)

        default_prompt = "write a short caption for this image"

        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)

# text embedding model
if selected == "Embed text":
    st.title("🔡 Embed Text")

    # input text box
    input_text = st.text_area(label="", placeholder="Enter the text to get the embeddings")

    if st.button("Get Embeddings"):
        response = embeddings_model_response(input_text)
        st.markdown(response)

# Question answering page
if selected == "Ask me anything":
    st.title("❓ Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get an answer"):
        response = gemini_pro_response((user_prompt))
        st.markdown(response)









