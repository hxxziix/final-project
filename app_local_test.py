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
if 'detected_labels' not in st.session_state:
    st.session_state.detected_labels = set()  # 탐지된 라벨 초기화
if 'modify_mode' not in st.session_state:
    st.session_state.modify_mode = False  # 수정 모드 초기화
if 'new_labels' not in st.session_state:
    st.session_state.new_labels = []  # 새로 추가할 라벨 초기화
if 'result_labels' not in st.session_state:
    st.session_state.result_labels = set()  # 최종 라벨 리스트 초기화

# 버튼 클릭 이벤트 처리
def start_camera():
    st.session_state.camera_running = True
    st.session_state.detected_labels.clear()  # 새로 시작할 때 탐지된 라벨 초기화

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

    placeholder = st.empty()  # 영상 출력을 위한 빈 공간 정의
    label_placeholder = st.empty()  # 탐지된 라벨을 표시할 빈 공간 정의

    st.button("재료 인식 종료 및 수정", use_container_width=True, key="end_modify_button")

    while st.session_state.camera_running:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            st.error("오류: 프레임을 읽을 수 없음.")
            break

        # 앙상블 예측 수행
        boxes, confidences, labels = ensemble_predict(frame)

        # 예측 결과를 프레임에 그리기
        draw(frame, boxes, confidences, labels)

        # 프레임을 BGR에서 RGB로 변환
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame)

        # 이미지 업데이트
        placeholder.image(frame_image, use_column_width=True)  # 빈 공간에 프레임 이미지 업데이트

        # 탐지된 라벨 업데이트
        for label in labels:
            st.session_state.detected_labels.add(label)

        # 라벨 표시
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
        
        # 버튼 클릭 시 수정 모드 활성화
        if st.session_state.get("end_modify_button"):
            st.session_state.modify_mode = True
            st.session_state.camera_running = False
            break

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

# 버튼이 클릭되었을 때 카메라 화면 표시 함수 호출
if st.session_state.camera_running:
    show_camera()

# # 수정 모드가 활성화된 경우
# if st.session_state.modify_mode:
#     # 사용자가 탐지된 재료를 수정할 수 있는 입력 필드 생성
#     st.write("탐지된 식재료 수정하기:")
#     updated_labels = []
#     for label in st.session_state.detected_labels:
#         if label not in st.session_state.new_labels:
#             new_label = st.text_input(f"{label} 수정:", value=label)
#             updated_labels.append(new_label)

#     # 추가할 식재료 입력 필드
#     additional_label = st.text_input("추가할 식재료:", "")

#     # 추가된 라벨 관리
#     if additional_label and additional_label not in st.session_state.detected_labels:
#         st.session_state.new_labels.append(additional_label)  # 추가된 라벨을 저장

#     # 업데이트 버튼
#     if st.button("업데이트", use_container_width=True):
#         # 수정된 재료 목록을 다시 설정
#         st.session_state.detected_labels = set(updated_labels).union(st.session_state.new_labels)  # 새로 추가된 라벨과 기존 라벨 병합
#         st.session_state.new_labels = []  # 추가된 라벨 초기화

#         st.success("재료가 업데이트되었습니다!")
#         st.write("나의 최종 식재료: ", ", ".join(st.session_state.detected_labels))

# 수정 모드가 활성화된 경우
if st.session_state.modify_mode:
    # 사용자가 탐지된 재료를 수정할 수 있는 입력 필드 생성
    st.write("탐지된 식재료 수정하기:")
    updated_labels = []
    for label in st.session_state.detected_labels:
        if label not in st.session_state.new_labels:
            new_label = st.text_input(f"{label} 수정:", value=label)
            updated_labels.append(new_label)

    # 추가할 식재료 입력 필드
    additional_label = st.text_input("추가할 식재료:", "")

    # 추가된 라벨 관리
    if additional_label not in st.session_state.new_labels:
        st.session_state.new_labels.append(additional_label)  # 추가된 라벨을 저장

    # 업데이트 버튼
    if st.button("업데이트", use_container_width=True):
        # updated_labels와 new_labels를 set으로 변환한 후 병합
        all_new_labels = set(updated_labels).union(set(st.session_state.new_labels))
        # 수정된 재료 목록을 다시 설정
        st.session_state.result_labels.update(all_new_labels) # 새로 추가된 라벨과 기존 라벨 병합
        
        st.session_state.new_labels = []  # 추가된 라벨 초기화

        st.success("재료가 업데이트되었습니다!")
        st.write("나의 최종 식재료: ", ", ".join(st.session_state.result_labels))
        
