from AvengersEnsemble import *
from Draw import *
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title='MultiCampus Enjo2조',
    page_icon='app_gui/1.png'
)

# 공백
empty = st.empty()
empty.markdown('<div style="height: 200px;"></div>', unsafe_allow_html=True)

# 이미지와 제목을 한 줄에 나란히 표시하기 위해 column 두개로 나눔
col1, col2 = st.columns([2, 5])

# col1 위치에 이미지
with col1:
    st.image('app_gui/1.png', width=150)

# col2 위치에 프젝 이름
with col2:
    css_title = st.markdown("""
        <style>
            .title {
                font-size: 70px;
                font-weight: bold;
                color: #f481512;
                text-shadow: 3px  0px 0 #fff;}
        </style>
        <p class=title>
            AI 요리 비서 ✨
        </p>""", unsafe_allow_html=True)

# 공백
empty1 = st.empty()
empty1.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

# 상태 초기화
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False
if 'detected_labels' not in st.session_state:
    st.session_state.detected_labels = set()
if 'modify_mode' not in st.session_state:
    st.session_state.modify_mode = False
if 'edit_label' not in st.session_state:
    st.session_state.edit_label = {}

# 버튼 클릭 이벤트 처리
def start_camera():
    st.session_state.camera_running = True
    st.session_state.detected_labels.clear()
    st.session_state.modify_mode = False

def stop_camera():
    st.session_state.camera_running = False

# 버튼을 위한 container 생성
container = st.container()

# 카메라 시작 버튼
if not st.session_state.camera_running and not st.session_state.modify_mode:
    container.button("Camera Start", on_click=start_camera, use_container_width=True)

# 카메라 종료 버튼
if st.session_state.camera_running:
    container.button("Camera Stop", on_click=stop_camera, use_container_width=True)

def show_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("오류: 웹캠이 열려있지 않음.")
        return

    placeholder = st.empty()
    label_placeholder = st.empty()

    def end_modify():
        st.session_state.modify_mode = True
        st.session_state.camera_running = False

    st.button("재료 인식 종료 및 수정", use_container_width=True, on_click=end_modify)

    while st.session_state.camera_running:
        ret, frame = cap.read()
        if not ret:
            st.error("오류: 프레임을 읽을 수 없음.")
            break

        boxes, confidences, labels = ensemble_predict(frame)
        
        output_image = draw_with_pil(frame, boxes, confidences, labels)

        frame = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame)

        placeholder.image(frame_image, use_column_width=True)

        for label in labels:
            st.session_state.detected_labels.add(label)

        label_placeholder.markdown(f"""
            <style>
                .text {{
                    font-size: 35px;
                    color: #f481512;
                    text-shadow: 3px  0px 0 #fff;}}
            </style>
            <p class="text">
                📸탐지된 식재료 : {", ".join(st.session_state.detected_labels)}
            </p>""", unsafe_allow_html=True)

    cap.release()
    cv2.destroyAllWindows()

if st.session_state.camera_running:
    show_camera()

# 수정 모드가 활성화된 경우
if st.session_state.modify_mode:
    def back_to_main():
        st.session_state.modify_mode = False
        st.session_state.camera_running = False
    
    st.button("🔙", on_click=back_to_main)

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