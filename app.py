from AvengersEnsemble import *
from Draw import *
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
# from PIL import Image

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
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# 버튼 클릭 이벤트 처리
def start_camera():
    st.session_state.button_clicked = True

# 버튼 크기 넓히기 위해 container 생성
container = st.container()
container.button("Camera Start", on_click=start_camera, use_container_width=True)

# 탐지된 라벨을 저장할 집합(set)
detected_labels = set()

def transform(frame: av.VideoFrame):
    global detected_labels
    # 프레임을 RGB로 변환
    img = frame.to_ndarray(format="bgr24")

    # 예측 수행
    boxes, confidences, labels = ensemble_predict(img)

    # 예측 결과를 프레임에 그리기 및 집합에 라벨 추가
    draw(img, boxes, confidences, labels)

    for label in labels:
        detected_labels.add(label)
    
    st.write("탐지된 라벨 기록:", detected_labels)

    print("\n탐지된 라벨 기록:")
    print(detected_labels)
    print('\n' + '==' * 50)
    
    return av.VideoFrame.from_ndarray(img, format="bgr24")

def show_camera():
    global detected_labels
    detected_labels = set()

    # WebRTC 연결 설정: STUN/TURN 서버 설정
    rtc_configuration = {
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}] # STUN
        # TURN 서버: 선택사항
    }

    # 웹캠 스트리밍 및 변환기 설정
    webrtc_streamer(key="streamer", video_frame_callback=transform, rtc_configuration=rtc_configuration, sendback_audio=False)

# 애는 사진 캡쳐방식(실시간 스트리밍X)
# def show_camera():
#     detected_labels = set() # 탐지된 라벨을 저장할 집합(set)

#     image = st.camera_input("Capture an image")
#     if image is not None:
#         frame = Image.open(image)

#         # 예측 수행
#         boxes, confidences, labels = ensemble_predict(frame)

#         # 예측 결과를 프레임에 그리기 및 집합에 라벨 추가
#         draw(frame, boxes, confidences, labels)

#         detected_labels.add(labels)

#         # 최종 결과 이미지 업데이트
#         st.image(frame, caption='Processed Image', use_column_width=True)

# 버튼이 클릭되었을 때 카메라 화면 표시 함수 호출
if st.session_state.button_clicked:
    show_camera()