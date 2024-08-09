import streamlit as st
from labels_modify_page import *
from search_recipe_page import *

def text_input():
    if st.session_state.labels_modify_page:
        _, col1, _ = st.columns([1, 10, 1])

        with col1:
            st.image("app_gui/input_icon.png",width=600)

        subheader = st.markdown("""
                <style>
                    .subheader {
                        font-size: 20px;
                        text-align: center;
                        background-color: #f8d7cb;
                        color: #EF8E34;
                        border: 7px outset #f5c299;
                        padding: 10px 20px 10px 20px;
                        margin: 0px 0px 0px 50px;
                        border-radius: 8px;
                        width: fit-center;
                        }
                </style>
                <p class=subheader>
                    입력창에 재료를 입력하고 <strong>다음 버튼</strong>을 눌러주세요
                </p>""", unsafe_allow_html=True)

        st.text("\n")
        st.text("\n")
        labels_modify_page()
    elif st.session_state.search_recipe_page:
        # 레시피 검색 페이지 진입
        search_recipe_page()
        
        if st.session_state.cook:
            # 요리 안내
            cook()