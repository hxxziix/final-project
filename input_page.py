import streamlit as st

def text_input():

    _, col1, _ = st.columns([1, 10, 1])

    with col1:
        st.image("app_gui/input_image.png",width=600)


    subheader = st.markdown("""
            <style>
                .subheader {
                    font-size: 20px;
                    text-align: center;
                    background-color: #b6ccfb;
                    color: #6d7df7;
                    border: 7px outset #91a8f9;
                    padding: 10px 20px 10px 20px;
                    margin: 0px 50px 0px 50px;
                    border-radius: 8px;
                    width: fit-center;
                    }
            </style>
            <p class=subheader>
                입력창에 재료를 입력하고 <strong>확인 버튼</strong>을 눌러주세요
            </p>""", unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 12, 1])
    with col2:
        st.text_input("")
    
    _,  _, col3 = st.columns([4, 4, 2])
    
    with col3:
        st.button("확인", key="button1")

        st.markdown("""
            <style>
            .stButton>button#button1 {
                background-color: #b3c4fa;
                color: #B761B4;
                font-size: 25px;
                font-weight: bold;
                width: 60px;
                height: 50px;
                border: 2px solid #CDBDEB;
            }
            .stButton>button:hover {
                background-color: #6d7df7;
            }
            
            </style>
        """, unsafe_allow_html=True)