import streamlit as st

# Create pages
chat_page = st.Page("pages/chat.py", title="AI 챗봇", icon=":material/chat:")
report1_page = st.Page("pages/report1.py", title="AI 기술 동향", icon=":material/analytics:")
report2_page = st.Page("pages/report2.py", title="산업별 동향", icon=":material/domain:")


# Set up navigation with sections
pg = st.navigation(
    {
        "AI 서비스": [chat_page],
        "리포트": [report1_page, report2_page],
    },
)

# Set default page configuration
st.set_page_config(
    page_title="AI 플랫폼",
    page_icon="🤖",
)

# Run the selected page
pg.run() 