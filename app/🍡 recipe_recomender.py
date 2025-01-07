import streamlit as st
# import openai
import faiss
# from sentence_transformers import SentenceTransformer
import os
import time
# import faiss
# import numpy as np
import pandas as pd
# from tqdm import tqdm
# from sentence_transformers import SentenceTransformer
# from sklearn.preprocessing import normalize
# from ast import literal_eval
from openai import OpenAI
# from utils import read_yaml, get_api_key, get_openai_completion

# import faiss
# import pandas as pd
from utils import (
    get_api_key,
    read_yaml, 
    EmbeddingModel_SBERT,
    retrieve_similar_texts,
    get_openai_completion
)

def get_embeddings(config: dict) -> faiss.IndexFlatIP:
    input_folder = config["embeddings_folder"]
    input_file = config["embeddings_file"]
    path = os.path.join(input_folder, input_file)
    return faiss.read_index(path)

def get_data(config: dict) -> pd.DataFrame:
    data_folder = config["data_folder"]
    data_file = config["data_file"]
    path = os.path.join(data_folder, data_file)
    return pd.read_csv(path)

def get_hello():
    return """
Hi, I'm ROB! I'm here to help you with your recipe questions, \
based on the awesome Guardian Open Platform Archive. 
Ask me anything!
"""
def get_goodbye():
    return """
I'm sorry, I can't help you with more questions at the moment. 
Please start a new chat if you have more questions.
"""

def get_recipe_promt(recipes: list[str]):
    i = 1
    prompt = ""
    for r in recipes:
        prompt += f"""
        RECIPE {i}: {r}"""
        i += 1
    return prompt


def get_starting_system_prompt():
    return f"""
    You work for the Guardian food section and you are knowledgeable about their recipes.
    Readers will come to you with questions. 
    You should answer the questions based on the provided Guardian articles.
    You should mention the articles to the reader.
    You should not provide the full text of the articles, but you can provide a summary.
    Make it inclusive for ASD and ADHD readers.
    """
def get_user_prompts(messages):
    return [m["content"] for m in messages if m["role"] == "user"]

def main() -> None:

    max_prompts = 3

    config = read_yaml("config/rag_config.yaml")
    api_key = get_api_key(config["api_key_name"])
    model = config["model"]
    
    embeddings = get_embeddings(config)
    df = get_data(config)
    
    client = OpenAI(api_key = api_key)

    # -------------- APP ---------------------
    st.title("ROB: Recipe Opinion Bot")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if st.button("Start New Chat"):
        st.session_state["chat_history"] = []

    hello = get_hello()
    st.chat_message("assistant").write(hello)
    query = st.chat_input("Type your question here...")

    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.chat_message("user").write(chat["content"])
        elif chat["role"] == "assistant":
            st.chat_message("assistant").write(chat["content"])

    # -------- respond to query ------------
    if query:
        
        # create system prompt if we are starting
        if len(st.session_state.chat_history) == 0:
            system_prompt = get_starting_system_prompt()
            system_message = {"role": "system", "content": system_prompt}
            st.session_state["chat_history"].append(system_message)
        
        # print user text
        st.chat_message("user").write(query)
        st.session_state["chat_history"].append({"role": "user", "content": query})
            
        # check if we need to end the chat
        user_prompts = get_user_prompts(st.session_state.chat_history)
        n_user_prompts = len(user_prompts)

        if n_user_prompts > max_prompts:
            goodbye = get_goodbye()
            st.chat_message("assistant").write(goodbye)
            st.session_state["chat_history"].append({"role": "assistant", "content": goodbye})

        else:
            # removed to allow follow-up questions 
            # # remove previous recipe prompts        
            # for i, chat in enumerate(st.session_state.chat_history):
            #     if chat["role"] == "system" and chat["content"].startswith("Here are some recipes"):
            #         st.session_state["chat_history"].pop(i)
        

            # TODO: restrict only if the user has aske for more recipes, and not a follow-up
            # get similar recipes
            n_texts = 3
            similarity_query = ' '.join(user_prompts)
            df_recipes = retrieve_similar_texts(
                query = similarity_query,
                model = EmbeddingModel_SBERT(),
                index = embeddings, 
                df = df, 
                k = n_texts
            )

            # convert to openai prompt format
            texts = df_recipes['content'].tolist()
            recipe_prompt = get_recipe_promt(texts)

            # add recipe prompt to system message
            system_prompt = "Here are some recipes that might help you:" + recipe_prompt
            system_message = {"role": "system", "content": system_prompt}
            st.session_state["chat_history"].append(system_message)
                
            with st.status("Thinking..."):
                messages = st.session_state["chat_history"]
                st.dataframe(df_recipes)
                st.write(similarity_query)
                response = get_openai_completion(client, model, messages)[0]
            
            st.chat_message("assistant").write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()















