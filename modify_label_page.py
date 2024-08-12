import streamlit as st

def modify_label_page():
    col1, _, _ = st.columns([3, 5, 5])
    with col1:
        st.markdown("""
        <style>
            .stButton>button {
                background-color: #fdffeb;
                color: #727421;
                font-size: 25px;
                font-weight: bold;
                width: 100%;
                height: 50px;
                border:5px outset #fdffb2;
            }
            .stButton>button:hover {
                background-color: #ffffD3;
                border: 7px outset #FFFF41;
            }
        </style>
        """, unsafe_allow_html=True)
    
        if st.session_state.selected_menu == "카메라 식재료 인식":
            if st.button("**뒤로 가기**"):
                st.session_state.modify_label_page = False
                st.session_state.camera_running = True
                st.experimental_rerun()
    
    if st.session_state.selected_menu == "카메라 식재료 인식":
        st.image("app_gui/ingredients.png")
    else: # "식재료 직접 입력"
        st.image("app_gui/input_icon.png",width=600)

    for label in list(st.session_state.detected_label_set):
        if label not in st.session_state.edit_label:
            st.session_state.edit_label[label] = False

        col1, col2, col3 = st.columns([6, 2, 2])
        
        with col1:
            if st.session_state.edit_label[label]:
                changed_label = st.text_input("", value=label, key=f"label_{label}", label_visibility="collapsed")
            else:
                st.markdown(f"""
                    <style>
                        .ingredients {{
                            font-size: 20px;
                            font-family: 'Fira Code';
                            font-weight: bold;
                            color: #727421;
                            border-radius: 8px;
                            background-color: #fdffeb;
                            border: 5px dotted  #fdffb2;
                            text-shadow: 3px  3px 0 #fff;
                            border-radius: 8px;
                            text-align: center;
                            padding: 4px 0px 4px 0px;
                            margin: 1px 0px 0px 0px;
                            }}
                    </style>
                    <p class=ingredients>
                        {label}
                    </p>
                            """, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.edit_label[label]:
                if st.button("확인", key=f"confirm_{label}"):
                    st.session_state.detected_label_set.remove(label)
                    st.session_state.detected_label_set.add(changed_label)
                    st.session_state.edit_label[label] = False
                    st.experimental_rerun()
            else:
                if st.button("수정", key=f"modify_{label}"):
                    st.session_state.edit_label[label] = True
                    st.experimental_rerun()
        
        with col3:
            if st.button("삭제", key=f"delete_{label}"):
                st.session_state.detected_label_set.remove(label)
                st.experimental_rerun()

    message = """
            <style>
                .add_ingredients {
                    font-size: 25px;
                    color: #727421;
                    font-weight: bold;
                    text-shadow: 2px  2px 0 #fff;
                    font-family: 'Fira Code';
                    text-align: center;
                    padding: 50px 10px 0px 10px;
                    border-radius: 8px;
                }    
            </style>    
            <p class=add_ingredients>
                추가할 재료가 있으면<br> 아래 칸에 입력 후 "추가" 버튼을 눌러주시고<br>추가할 재료가 없으면<br>"다음" 버튼을 눌러주세요
            </p>"""

    if st.session_state.selected_menu == "식재료 직접 입력":
        message = """
                <style>
                    .add_ingredients {
                        font-size: 25px;
                        color: #727421;
                        font-weight: bold;
                        text-shadow: 2px  2px 0 #fff;
                        font-family: 'Fira Code';
                        text-align: center;
                        padding: 50px 10px 0px 10px;
                        border-radius: 8px;
                    }    
                </style>    
                <p class=add_ingredients>
                    아래에 재료를 추가하고 <br>"다음" 버튼을 눌러주세요
                </p>"""

    st.markdown(message, unsafe_allow_html=True)
    
    # text_input box CSS
    st.markdown("""
        <style>
            .st-ct.st-bn.st-cu.st-bq.st-cx.st-cy.st-cz.st-d0.st-d1.st-d2.st-d3.st-d4.st-eu.st-d6.st-ar.st-ak.st-an.st-al.st-am.st-cd.st-ck.st-cl.st-cm.st-cn.st-co.st-d7.st-d8.st-d9.st-da.st-db.st-ev.st-ew.st-dc {
                border: 5px dotted #fef8ad;
                height: 50px;
                border-radius: 10px;
                padding: 10px 10px 10px 10px;
                font-size: 30px;
                color: #333;
                background-color: #f9f9f9;
                width: 100%;
            }
            .st-ct.st-bn.st-cu.st-bq.st-cx.st-cy.st-cz.st-d0.st-d1.st-d2.st-d3.st-d4.st-eu.st-d6.st-ar.st-ak.st-an.st-al.st-am.st-cd.st-ck.st-cl.st-cm.st-cn.st-co.st-f7.st-f8.st-f9.st-fa.st-db.st-ev.st-ew.st-dc {
                border: 5px dotted #f2a653;
                height: 50px;
                border-radius: 10px;
                padding: 10px 10px 10px 10px;
                font-size: 30px;
                color: #333;
                background-color: #f9f9f9;
                width: 100%;
            }
        </style>""",
        unsafe_allow_html=True)

    # 재료 추가 입력창
    new_label_input = st.text_input(" ", key="new_label_input")
    
    col4, col5 = st.columns([5, 5])
    
    if col4.button("추가"):
        if new_label_input:
            st.session_state.detected_label_set.add(new_label_input)
            st.experimental_rerun()

    if col5.button("다음"):
        if st.session_state.detected_label_set:
            st.session_state.modify_label_page = False
            st.session_state.search_recipe_page = True
            st.experimental_rerun()
        else:
            st.markdown("""
            <style>
                .warning {
                    font-size: 25px;
                    color: #99999;
                    font-weight: bold;
                    text-shadow: 2px  2px 0 #fff;
                    font-family: 'Fira Code';
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                    border-radius: 8px;
                    border: 10px outset red;
                }    
            </style>
            <p class=warning>
                ⚠️ 재료가 없습니다 ⚠️
            </p>
            """, unsafe_allow_html=True)
