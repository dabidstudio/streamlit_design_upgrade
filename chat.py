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
        help="높을수록 더 창의적이고 다양한 응답을, 낮을수록 더 일관된 응답을 생성합니다."
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

# Add sidebar
with st.sidebar:
    st.write("### 채팅 설정")
    
    # Add expander for chat settings
    with st.expander("고급 설정", expanded=True):
        # System prompt editor
        system_prompt = st.text_area(
            "시스템 프롬프트",
            value=system_message,
            help="AI의 페르소나를 설정하는 프롬프트입니다."
        )
        
        # Save changes button
        if st.button("설정 저장"):
            st.session_state.messages[0]["content"] = system_prompt
            st.success("설정이 저장되었습니다!")
            
    # Add information about the chat
    st.info("""
    💡 **사용 팁**
    - Temperature를 낮추면 더 일관된 답변을
    - Temperature를 높이면 더 창의적인 답변을
    - GPT-4o는 더 정확하지만 느립니다
    - GPT-4o-mini는 더 빠르지만 간단합니다
    """)
    
    # Add message count
    if len(st.session_state.messages) > 1:
        st.metric(
            "대화 수", 
            len(st.session_state.messages) - 1,  # Subtract 1 to exclude system message
            help="현재까지의 대화 수입니다."
        )


# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    if idx > 0:  # Skip system message
        icon = "🤖" if message["role"] == "assistant" else ":material/person:"
        with st.chat_message(message["role"], avatar=icon):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
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
