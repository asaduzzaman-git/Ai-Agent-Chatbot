#setp1: setup UI with streamlit (model provide, model, system prompt, web_search, query)
import streamlit as st

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("ASAD AI Chatbot Agents")
st.write("Create and interact with the AI Agents!")

system_prompt=st.text_area("Define your AI Agent:", height=70, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
model_name_openAI=["gpt-4o-mini"]

provider=st.radio("select provider:", ("Groq", "OpenAI"))

if provider=="Groq":
    select_model=st.selectbox("Select Groq model:", MODEL_NAMES_GROQ)
elif provider=="OpenAI":
    select_model=st.selectbox("select OpenAI model:", model_name_openAI)

allow_web_search=st.checkbox("Allow_web_search")

user_query=st.text_area("Enter your Query:", height=150, placeholder="Now, your Turn!...")

API_URL="http://127.0.0.1:9999/chat"


if st.button("ASK AGENT!"):
    if user_query.strip():
        #step2: Connect with backend via url
        import requests

        payload={
            "model_name": select_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response=requests.post(API_URL, json=payload)
        #Get response from backend and show here
        if response.status_code==200:
            response_data=response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {response_data}")
