import streamlit as st


# 기본 system message
system_message = "너의 이름은 친구봇이야."

# 기본 메시지들
default_messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": "안녕하세요! 반가워요. 저는 오늘 처음 AI 챗봇과 대화를 해보는데 정말 신기하고 설레네요. 앞으로 많은 이야기를 나눌 수 있었으면 좋겠어요."},
    {"role": "assistant", "content": "안녕하세요! 저는 친구봇이에요. 처음 AI 챗봇과 대화하시는 거라니 저도 설레네요 😊 저와 함께 이야기 나누시면서 궁금한 점도 물어보시고, 고민도 나누고, 재미있는 대화도 나눠보아요. 오늘 하루는 어떻게 보내셨나요?"},
    {"role": "user", "content": "오늘은 회사에서 좀 힘든 일이 있었어요. 동료와 약간의 갈등이 있었거든요."},
    {"role": "assistant", "content": "그렇군요, 직장 생활하다 보면 동료와의 갈등이 생기는 건 자연스러운 일이에요. 혹시 어떤 상황이었는지 더 자세히 이야기해주실 수 있나요? 제가 이야기를 들어드리면서 함께 해결 방법을 찾아보면 좋겠어요. 🤗"},
]


# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = default_messages.copy()
# Hide the stAppHeader via CSS
st.title("나만의 AI 챗봇")




# ---- UI 위젯들 ----
col1, col2 = st.columns(2)
with col1:
    st.selectbox(
        "모델 선택",
        ["gpt-4", "gpt-3.5-turbo"],
    )
    st.button(
        "대화 기록 초기화",
        type="primary",
    )
with col2:
    st.toggle(
        "도구 사용",
        value=True,
    )

    st.slider(
        "Temperature (창의성 조절)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
    )



# ---- 사이드바 ----
with st.sidebar:
    st.write("### 채팅 설정")

    with st.expander("고급 설정", expanded=True):
        system_prompt = st.text_area(
            "시스템 프롬프트",
            value=st.session_state.messages[0]["content"],
            help="AI의 페르소나를 설정하는 프롬프트입니다."
        )
        if st.button("설정 저장", help="변경된 시스템 프롬프트를 저장하고 적용합니다."):
            st.session_state.messages[0]["content"] = system_prompt
            st.success("설정이 저장되었습니다!")

    st.info("""
    💡 **사용 팁**
    - Temperature를 낮추면 더 일관된 답변
    - Temperature를 높이면 더 창의적인 답변
    - GPT-4o는 더 정확하지만 느립니다
    - GPT-4o-mini는 더 빠르지만 간단합니다
    """)






st.divider()

# ---- 채팅 메시지 출력 ----
for message in st.session_state.messages:
    # system 메시지는 출력 안 함
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ---- 사용자 입력 ----
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = f"사용자는 {prompt} 라고 말했습니다"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)



