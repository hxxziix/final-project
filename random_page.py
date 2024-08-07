import streamlit as st
import random
from Recipe import *

def random_page():
    # recipe_df의 행 수를 사용하여 랜덤 숫자 생성
    random_number = random.randint(0, recipe_df.shape[0] - 1) # 0부터 (행 수 - 1)까지의 숫자 생성
    recipe_result = random_recipe(random_number)
    
    _, col1, _ = st.columns([4, 10, 1])

    with col1:
        st.image("app_gui/5.png")

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
                랜덤 추천 레시피
            </p>""", unsafe_allow_html=True)

    subheader = st.markdown(f"""
            <style>
                .subheader {{
                    font-size: 20px;
                    background-color: #FAECFE;
                    color: #B761B4;
                    text-align: center;
                    text-shadow: 3px  0px 0 #fff;
                    border-radius: 8px;
                    }}
            </style>
            <p class=subheader>
                요리 비서가 추천 드리는 레시피는 <br> <strong>{recipe_result['요리명']}</strong> 입니다 !
            </p>""", unsafe_allow_html=True)
    
    st.write(recipe_result)