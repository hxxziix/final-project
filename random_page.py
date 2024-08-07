import streamlit as st
import random
from Recipe import *
import time

def random_page():
    # 0부터 (행 수 - 1)까지의 숫자 생성
    random_number = random.randint(0, recipe_df.shape[0] - 1)
    recipe_result = random_recipe(random_number)
    
    
    st.image("app_gui/11.png", width=700)
    
    
    
    _, col1, _ = st.columns([3, 10, 1])


    with col1:
        st.image("app_gui/5.png", width=400)

    subheader = st.markdown(f"""
            <style>
                .subheader {{
                    font-size: 20px;
                    background-color: #FAECFE;
                    color: #B761B4;
                    text-align: center;
                    border: 10px outset #e3a9fa;
                    text-shadow: 3px  0px 0 #fff;
                    border-radius: 8px;
                    margin: 0px 0px 50px 50px;
                    }}
            </style>
            <p class=subheader>
                요리 비서가 추천 드리는 레시피는 <br> <strong>{recipe_result['요리명']}</strong> 입니다 !
            </p>""", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 8, 1])
    with col2:  
        st.write(recipe_result)