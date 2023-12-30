"""
Main file to run (if vector database is made)
"""

import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from messages import get_system_message, get_human_message
from utils import fit_context_to_token_limit, get_most_relevant_chunks, get_api_key
import streamlit as st
from streamlit_chat import message
import pandas as pd

# These are the necessary setups for ChatOpenAI LLM
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://open-ai-embeddings.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = get_api_key()

KNOWLEDGE_BASE = "hjertemedisin"


# ========== Section 1: Chat ============================

def chat(question, KNOWLEDGE_BASE):
    most_relevant_chunks = pd.DataFrame([])
    most_relevant_chunks[["documents","distance"]] = get_most_relevant_chunks(question,
                                                                              KNOWLEDGE_BASE,
                                                                              k=10,
                                                                              fit_to_max_token=True)
    most_relevant_chunks["text"] = [i.page_content for i in most_relevant_chunks["documents"]]
    context = "\n".join(most_relevant_chunks.text.to_list())

    chat_LLM = ChatOpenAI(temperature=0.0, 
                          engine="boozt")

    messages = [
        SystemMessage(content=get_system_message()),
        HumanMessage(content=get_human_message(question, context))
    ]
    response = chat_LLM(messages)

    #print(response.content)
    
    return response.content, most_relevant_chunks[["text", "distance"]]


# ========== Section 2: Display ============================


st.title(f"Chatbot Demo - {KNOWLEDGE_BASE}")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'source' not in st.session_state:
    st.session_state['source'] = []


def clear_text():
    st.session_state["input"] = ""


# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input('Chat here! 💬', key="input")
    return input_text


user_input = get_text()

if user_input:
    output, knowledge_df = chat(user_input, KNOWLEDGE_BASE)

    # Display output and similarities
    st.write(output)
    
    # Display output of dataframe!
    st.write(knowledge_df)


if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i],  key=str(i))
        message(st.session_state['past'][i], is_user=True,
                avatar_style="big-ears",  key=str(i) + '_user')
