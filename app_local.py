from AvengersEnsemble import *
from Draw import *
import streamlit as st
from PIL import Image

# 페이지 기본 설정
st.set_page_config(
    # 페이지 제목
    page_title='MultiCampus Enjo2조',
    # 페이지 아이콘
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

# 버튼 클릭 여부를 확인하기 위한 상태 변수
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False  # 카메라 상태 초기화

# 버튼 클릭 이벤트 처리
def start_camera():
    st.session_state.camera_running = True

def stop_camera():
    st.session_state.camera_running = False

# 버튼을 위한 container 생성
container = st.container()

# 카메라 시작 버튼
if not st.session_state.camera_running:
    container.button("Camera Start", on_click=start_camera, use_container_width=True)

# 카메라 종료 버튼
if st.session_state.camera_running:
    container.button("Camera Stop", on_click=stop_camera, use_container_width=True)

def show_camera():
    # 로컬 웹캠 열기
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("오류: 웹캠이 열려있지 않음.")
        return

    detected_labels = set()  # 탐지된 라벨을 저장할 집합(set)

    placeholder = st.empty()

    while st.session_state.camera_running:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            st.error("오류: 프레임을 읽을 수 없음.")
            break

        # 앙상블 예측 수행
        boxes, confidences, labels = ensemble_predict(frame)

        # 예측 결과를 프레임에 그리기 및 집합에 라벨 추가
        draw(frame, boxes, confidences, labels)

        for label in labels:
            detected_labels.add(label)

        print("\n탐지된 라벨 기록:")
        print(detected_labels)
        print('\n' + '==' * 50)

        # 프레임을 BGR에서 RGB로 변환
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame)

        # 이미지 업데이트
        placeholder.image(frame_image, use_column_width=True)

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

# 버튼이 클릭되었을 때 카메라 화면 표시 함수 호출
if st.session_state.camera_running:
    show_camera()