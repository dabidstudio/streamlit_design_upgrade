from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()



system_message = '''
너의 이름은 친구봇이야.
'''

# Initialize session state for model, temperature, and messages
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"
if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.7
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": "안녕하세요! 저는 친구봇이에요. 오늘 하루는 어떠셨나요? 😊 저는 여러분과 대화하면서 함께 성장하고 싶어요."},
        {"role": "user", "content": "안녕하세요! 반가워요. 저도 대화하고 싶었어요."},
        {"role": "assistant", "content": "정말 반가워요! 저와 함께 이야기하면서 즐거운 시간 보내시길 바라요. 무슨 이야기든 편하게 나눠주세요! 여러분의 이야기를 듣는 것이 저의 가장 큰 기쁨이에요. 고민이 있다면 함께 나누어볼까요? 아니면 오늘 있었던 즐거운 일을 들려주시는 것도 좋을 것 같아요! 💫"},
        {"role": "user", "content": "네, 좋아요! 오늘 있었던 일을 이야기해볼게요."},
        {"role": "assistant", "content": "와, 정말 기대되네요! 오늘 하루 어떤 특별한 일들이 있었는지 궁금해요. 기쁜 일이든 힘든 일이든 제가 잘 들어드릴게요. 천천히 이야기해주세요! 🌟"}
    ]

st.title("AI 챗봇과 대화하기")

# Add model settings at the top
col1, col2 = st.columns(2)
with col1:
    st.session_state["openai_model"] = st.selectbox(
        "모델 선택",
        ["gpt-4", "gpt-3.5-turbo"],
        index=0 if st.session_state["openai_model"] == "gpt-4" else 1
    )

with col2:    
    st.toggle("도구 사용", value=True)
    st.session_state["temperature"] = st.slider(
        "Temperature (창의성 조절)",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state["temperature"],
        step=0.1,
    )

# Reset button in a single column
st.file_uploader("파일 업로드", type=["pdf", "docx", "txt"],key="main-uploader")

if st.button("대화 기록 초기화", type="primary"):
    st.session_state.messages = [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": "안녕하세요! 저는 친구봇이에요. 오늘 하루는 어떠셨나요? 😊 저는 여러분과 대화하면서 함께 성장하고 싶어요."},
        {"role": "user", "content": "안녕하세요! 반가워요. 저도 대화하고 싶었어요."},
        {"role": "assistant", "content": "정말 반가워요! 저와 함께 이야기하면서 즐거운 시간 보내시길 바라요. 무슨 이야기든 편하게 나눠주세요! 여러분의 이야기를 듣는 것이 저의 가장 큰 기쁨이에요. 고민이 있다면 함께 나누어볼까요? 아니면 오늘 있었던 즐거운 일을 들려주시는 것도 좋을 것 같아요! 💫"},
        {"role": "user", "content": "네, 좋아요! 오늘 있었던 일을 이야기해볼게요."},
        {"role": "assistant", "content": "와, 정말 기대되네요! 오늘 하루 어떤 특별한 일들이 있었는지 궁금해요. 기쁜 일이든 힘든 일이든 제가 잘 들어드릴게요. 천천히 이야기해주세요! 🌟"}
    ]
    st.rerun()

st.divider()


# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    if idx > 0:  # Skip system message
        with st.chat_message(message["role"], ):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ], # type: ignore
            stream=True,
            temperature=st.session_state["temperature"]
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response}) # type: ignore 
