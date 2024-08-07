import streamlit as st
from labels_modify_page import labels_modify_page
from search_recipe_page import *

def text_input():
    if st.session_state.labels_modify_page:
        _, col1, _ = st.columns([2.5, 10, 1])

        with col1:
            st.image("app_gui/7.png")

        header = st.markdown("""
                <style>
                    .title {
                            font-size: 40px;
                            color: #f481512;
                            font-family: 'Fira Code';
                            font-weight: bold;
                            background-color: #b3c4fa;
                            color: #6d7df7;
                            border-radius: 8px;
                            text-align: center;
                            margin: 0px 50px 20px 50px;
                </style>
                <p class=title>
                    식재료 입력
                </p>""", unsafe_allow_html=True)

        subheader = st.markdown("""
                <style>
                    .subheader {
                        font-size: 20px;
                        text-align: center;
                        background-color: #b3c4fa;
                        color: #6d7df7;
                        padding: 10px 20px 10px 20px;
                        margin: 0px 50px 0px 50px;
                        border-radius: 8px;
                        width: fit-center;
                        }
                </style>
                <p class=subheader>
                    재료를 추가하고 <strong>다음 버튼</strong>을 눌러주세요.
                </p>""", unsafe_allow_html=True)

        st.text("\n")
        st.text("\n")
        labels_modify_page()

        # _, col2, _ = st.columns([1, 12, 1])
        # with col2:
        #     st.text_input("")
        
        # _,  _, col3 = st.columns([4, 4, 2])
        
        # with col3:
        #     st.button("다음", key="button1")

        #     st.markdown("""
        #         <style>
        #         .stButton>button#button1 {
        #             background-color: #b3c4fa;
        #             color: #B761B4;
        #             font-size: 25px;
        #             font-weight: bold;
        #             width: 60px;
        #             height: 50px;
        #             border: 2px solid #CDBDEB;
        #         }
        #         .stButton>button:hover {
        #             background-color: #6d7df7;
        #         }
                
        #         </style>
        #     """, unsafe_allow_html=True)
    elif st.session_state.search_recipe_page:
        # 레시피 검색 페이지 진입
        search_recipe_page()
        
        if st.session_state.cook:
            # 요리 안내
            cook()