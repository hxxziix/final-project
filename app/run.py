import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../technique')))

from AvengersEnsemble import *
import streamlit as st
import cv2
from PIL import Image

# 페이지 기본 설정
st.set_page_config(
    # 페이지 제목
    page_title='MultiCampus Enjo2조',
    # 페이지 아이콘
    page_icon='app/images/1.png'
)

# 공백
empty = st.empty()
empty.markdown('<div style="height: 200px;"></div>', unsafe_allow_html=True)

# 이미지와 제목을 한 줄에 나란히 표시하기 위해 column 두개로 나눔
col1, col2 = st.columns([2, 5])

# col1 위치에 이미지
with col1:
    st.image('app/images/1.png', width=150)

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

# 카메라를 클라이언트 측에서 시작하는 함수
def show_camera():
    detected_labels = set()  # 중복 없이 탐지된 라벨을 저장할 집합(set)

    image = st.camera_input("Capture an image")
    if image is not None:
        # 이미지 처리 및 앙상블 예측 수행
        frame = Image.open(image)

        # 앙상블 예측 수행
        boxes, confidences, labels = ensemble_predict(frame)

        # 예측 결과를 프레임에 그리기 및 집합에 라벨 추가
        print("\nfinal conclusion:")
        if len(boxes) > 0 and len(confidences) > 0 and len(labels) > 0:
            for box, conf, label in zip(boxes, confidences, labels):
                x1, y1, x2, y2 = map(int, box)
                label_name = label

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                print(f'Box: {box}, Confidence: {conf}, Label: {label_name}')

                detected_labels.add(label_name)
                print("\nDetected Labels:", detected_labels) # 지금까지 탐지된 라벨 출력
        print('\n' + '==' * 50)

        # 최종 결과 이미지 업데이트
        st.image(frame, caption='Processed Image', use_column_width=True)

# def show_camera():
#     detected_labels = set()  # 중복 없이 탐지된 라벨을 저장할 집합(set)

#     while True:
#         # 웹캠 입력을 받기 위한 Streamlit의 camera_input 사용
#         image = st.camera_input("Capture an image")

#         if image is not None:
#             # 이미지 처리 및 앙상블 예측 수행
#             frame = Image.open(image)

#             # 앙상블 예측 수행
#             boxes, confidences, labels = ensemble_predict(frame)

#             # 예측 결과를 프레임에 그리기 및 집합에 라벨 추가
#             print("\nfinal conclusion:")
#             if len(boxes) > 0 and len(confidences) > 0 and len(labels) > 0:
#                 for box, conf, label in zip(boxes, confidences, labels):
#                     x1, y1, x2, y2 = map(int, box)
#                     label_name = label

#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     cv2.putText(frame, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
#                     print(f'Box: {box}, Confidence: {conf}, Label: {label_name}')

#                     detected_labels.add(label_name)
#                     print("\nDetected Labels:", detected_labels) # 지금까지 탐지된 라벨 출력
#             print('\n' + '==' * 50)

#             # 최종 결과 이미지 업데이트
#             st.image(frame, caption='Processed Image', use_column_width=True)

#             # 버튼 클릭 여부 확인하여 루프 종료
#             if st.session_state.button_clicked:
#                 break

# 버튼이 클릭되었을 때 카메라 화면 표시 함수 호출
if st.session_state.button_clicked:
    show_camera()