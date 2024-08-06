import streamlit as st


def camera():
    _, col1, _ = st.columns([3, 10, 1])


    with col1:
        st.image("app_gui/camera.png")

    header = st.markdown("""
            <style>
                .title {
                        font-size: 40px;
                        color: #f481512;
                        font-family: 'Fira Code';
                        font-weight: bold;
                        background-color: #FAECFE;
                        color: #B761B4;
                        border-radius: 8px;
                        
                        border-radius: 8px;
                        text-align: center;
                        margin: 0px 0px 20px 0px;
            </style>
            <p class=title>
                카메라 촬영
            </p>""", unsafe_allow_html=True)

    subheader = st.markdown("""
            <style>
                .subheader {
                    font-size: 20px;
                    background-color: #FAECFE;
                    color: #B761B4;
                    text-align: center;
                    text-shadow: 3px  0px 0 #fff;
                    border-radius: 8px;
                    }
            </style>
            <p class=subheader>
                AI 요리 비서가 레시피를 추천할 수 있도록 재료를 준비해주세요<br>
            준비가 완료되었다면 아래에 <strong>촬영 시작</strong> 버튼을 눌러주세요
            </p>""", unsafe_allow_html=True)

    _, col2, _ = st.columns([2, 5, 2])

    with col2:
        camera_button_con = st.container()
        camera_button_con.button("촬영 시작", use_container_width=True)


    button =st.markdown("""
            <style>
            .stButton>button {
                background-color: #f6c6fb;
                color: #B761B4;
                font-size: 25px;
                font-weight: bold;
                width: 100%;
                height: 50px;
                margin: 10px 0;
                border: 2px solid #CDBDEB;
            }
            .stButton>button:hover {
                background-color: #f67dfb;
            }
            </style>
        """, unsafe_allow_html=True)
