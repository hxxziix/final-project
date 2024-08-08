import streamlit as st

def camera_labels_modify_page():
    if st.session_state.search_type == "카메라":
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
                    margin: 10px 0;
                    border:5px outset #fdffb2;
                }
                .stButton>button:hover {
                    background-color: #ffffD3;
                    border: 7px outset #FFFF41;
                }
            </style>
        """, unsafe_allow_html=True)
        
            if st.button("**뒤로 가기**"):
                
                st.session_state.labels_modify_page = False
                st.session_state.camera_running = True
                st.experimental_rerun()

    st.image("app_gui/55.png")
    # st.markdown("""
    #     <style>
    #         .my_ingredients {
    #             font-size: 29px;
    #             color: #f481512;
    #             font-family: 'Fira Code';
    #             font-weight: bold;
    #             color: #727421;
    #             border-radius: 8px;
    #             background-color: #fdffeb;
    #             border: 10px dotted #fdffb2;
    #             text-shadow: 3px  3px 0 #fff;
    #             margin: 10px 0px 50px 0px;
    #             border-radius: 8px;
    #             padding: 10px 0px 10px 0px;
    #             text-align: center;
    #             }
    #     </style>
    #     <p class=my_ingredients>
    #         나의 식재료
    #     </p>
    #             """, unsafe_allow_html=True)

    for label in list(st.session_state.detected_labels):
        if label not in st.session_state.edit_label:
            st.session_state.edit_label[label] = False

        col1, col2, col3 = st.columns([6, 2, 2])
        
        with col1:
            if st.session_state.edit_label[label]:
                changed_label = st.text_input(f"'{label}'을(를) 무엇으로 바꾸시겠습니까?", value=label, key=f"label_{label}")
            else:
                st.markdown(f"""
                    <style>
                        .ingredients {{
                            font-size: 20px;
                            color: #f481512;
                            font-family: 'Fira Code';
                            font-weight: bold;
                            color: #727421;
                            border-radius: 8px;
                            background-color: #fdffeb;
                            border: 5px outset #fdffb2;
                            text-shadow: 3px  3px 0 #fff;
                            border-radius: 8px;
                            text-align: center;
                            padding: 4px 0px 4px 0px;
                            margin: 10px 0px 0px 0px;
                            }}
                    </style>
                    <p class=ingredients>
                        {label}
                    </p>
                            """, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.edit_label[label]:
                if st.button("확인", key=f"confirm_{label}"):
                    st.session_state.detected_labels.remove(label)
                    st.session_state.detected_labels.add(changed_label)
                    st.session_state.edit_label[label] = False
                    st.experimental_rerun()
            else:
                if st.button("수정", key=f"modify_{label}"):
                    st.session_state.edit_label[label] = True
                    st.experimental_rerun()
        
        with col3:
            if st.button("삭제", key=f"delete_{label}"):
                st.session_state.detected_labels.remove(label)
                st.experimental_rerun()

    new_label_input = st.text_input("새 재료가 있다면 추가하세요.", key="new_label_input")
    if st.button("재료 추가"):
        if new_label_input:
            st.session_state.detected_labels.add(new_label_input)
            st.experimental_rerun()

    if st.button("다음"):
        if st.session_state.detected_labels:
            st.session_state.labels_modify_page = False
            st.session_state.search_recipe_page = True
            st.experimental_rerun()
        else:
            st.write("재료가 없습니다!")




















def labels_modify_page():
    if st.session_state.search_type == "카메라":
        if st.button("뒤로 가기"):
            st.session_state.labels_modify_page = False
            st.session_state.camera_running = True
            st.experimental_rerun()

    st.write("나의 식재료:")

    for label in list(st.session_state.detected_labels):
        if label not in st.session_state.edit_label:
            st.session_state.edit_label[label] = False

        col1, col2, col3 = st.columns([6, 1, 1])
        
        with col1:
            if st.session_state.edit_label[label]:
                changed_label = st.text_input(f"'{label}'을(를) 무엇으로 바꾸시겠습니까?", value=label, key=f"label_{label}")
            else:
                st.write(label)
        
        with col2:
            if st.session_state.edit_label[label]:
                if st.button("확인", key=f"confirm_{label}"):
                    st.session_state.detected_labels.remove(label)
                    st.session_state.detected_labels.add(changed_label)
                    st.session_state.edit_label[label] = False
                    st.experimental_rerun()
            else:
                if st.button("수정", key=f"modify_{label}"):
                    st.session_state.edit_label[label] = True
                    st.experimental_rerun()
        
        with col3:
            if st.button("삭제", key=f"delete_{label}"):
                st.session_state.detected_labels.remove(label)
                st.experimental_rerun()

    new_label_input = st.text_input("새 재료가 있다면 추가하세요.", key="new_label_input")
    if st.button("재료 추가"):
        if new_label_input:
            st.session_state.detected_labels.add(new_label_input)
            st.experimental_rerun()

    if st.button("다음"):
        if st.session_state.detected_labels:
            st.session_state.labels_modify_page = False
            st.session_state.search_recipe_page = True
            st.experimental_rerun()
        else:
            st.write("재료가 없습니다!")



