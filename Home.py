import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
st.image("pages/images/chatbotimage.jpg")

st.title("Get answers. Be more productive.")

st.text("Free to use. Easy to try. Just ask ChatBot and  can help with learning, brainstorming, and more.")

st.logo("pages/images/chatbot.png")


st.divider()

#st.link_button("Go to Sales Dashboard ->","http://localhost:8501/Sales_Dashboard")
#st.link_button("Generate Invoice ->","http://localhost:8501/Invoice_generator")
#st.link_button("Deep Dive ->","http://localhost:8501/Deep_dive_into_data")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("Go to Sales Dashboard ->", "https://app-4uhyvwebwby8t9kcvylwzz.streamlit.app/Sales_Dashboard")
    
with col2:
    st.link_button("Generate Invoice ->", "https://app-4uhyvwebwby8t9kcvylwzz.streamlit.app/Invoice_generator")
    
with col3:
    st.link_button("Deep Dive ->", "https://app-4uhyvwebwby8t9kcvylwzz.streamlit.app/Deep_dive_into_data")





