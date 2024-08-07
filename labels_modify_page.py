import streamlit as st

def labels_modify_page():
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