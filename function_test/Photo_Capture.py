from AvengersEnsemble import *
from Draw import *
import streamlit as st
from PIL import Image

def show_camera_for_capture():
    detected_labels = set() # 탐지된 라벨을 저장할 집합(set)

    image = st.camera_input("Capture an image")
    if image is not None:
        frame = Image.open(image)

        # 예측 수행
        boxes, confidences, labels = ensemble_predict(frame)

        # 예측 결과를 프레임에 그리기 및 집합에 라벨 추가
        draw(frame, boxes, confidences, labels)

        detected_labels.add(labels)

        # 최종 결과 이미지 업데이트
        st.image(frame, caption='Processed Image', use_column_width=True)