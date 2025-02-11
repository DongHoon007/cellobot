import os
from openai import OpenAI
import streamlit as st
import toml

secrets_path = ".streamlit/secrets.toml"
system_path = ".streamlit/system.toml"

# .streamlit 폴더가 없으면 생성
if not os.path.exists(".streamlit"):    
    os.makedirs(".streamlit")
    
# secrets.toml 파일 생성

if not os.path.exists(secrets_path):
    with open(secrets_path, "w", encoding="utf-8") as f:
        f.write(f'OPENAI_API_KEY = "{api_key}"\n')

if not os.path.exists(system_path):
    with open(system_path, "w", encoding="utf-8") as s:
        s.write(f'SYSTEM_MESSAGE = "{system_message}"\n')
    
st.title("노인들의 우울증 상담을 위한 챗봇")

api_key = st.secrets["OPENAI_API_KEY"]

if os.path.exists(system_path):
    system_config = toml.load(system_path)
else:
    system_config = {}

system_message = system_config.get("SYSTEM_MESSAGE", "기본메시지")    
#system_message = st.system["SYSTEM_MESSAGE"]
#system_message = ""

#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = OpenAI(api_key=api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages = [{"role": "system", "content": system_message}]

for message in st.session_state.messages:
    if message["role"] != "system":  # 시스템 메시지는 출력하지 않음
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("메시지를 기입해 주세요."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})