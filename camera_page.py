import streamlit as st
from AvengersEnsemble import *
from Draw import *
from labels_modify_page import *
from search_recipe_page import *

# '촬영 시작' 버튼의 콜백함수
def enable_camera():
    st.session_state.camera_running = True
    st.session_state.detected_labels.clear()
    st.session_state.labels_modify_page = False

# 카메라 시작 함수
def show_camera():
    # 로컬 웹캠 열기
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("오류: 웹캠이 열려있지 않음.")
        return
    
    placeholder = st.empty()  # 영상 출력을 위한 빈 공간 정의
    label_placeholder = st.empty()  # 탐지된 라벨을 표시할 빈 공간 정의

    def end_modify(): # "재료 인식 종료 및 수정" 버튼의 콜백함수
        st.session_state.camera_running = False
        st.session_state.finish_recognizing_button = False
        st.session_state.labels_modify_page = True

    while st.session_state.camera_running:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            st.error("오류: 프레임을 읽을 수 없음.")
            break

        # 앙상블 예측 수행
        boxes, confidences, labels = ensemble_predict(frame)

        # 예측 결과를 프레임에 그리기
        output_image = draw_with_pil(frame, boxes, confidences, labels)

        # 프레임을 BGR에서 RGB로 변환
        frame = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame)

        # 이미지 업데이트
        placeholder.image(frame_image, use_column_width=True)  # 빈 공간에 프레임 이미지 업데이트

        # 탐지된 라벨 업데이트
        for label in labels:
            st.session_state.detected_labels.add(label)
        
        # 탐지된 라벨 표시
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

        # "재료 인식 종료 및 수정" 버튼 생성
        if not st.session_state.finish_recognizing_button:
            st.button("재료 인식 종료 및 수정", use_container_width=True, on_click=end_modify)
            st.session_state.finish_recognizing_button = True

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

def camera_page():
    if st.session_state.camera_running:
        show_camera() # 카메라 시작 페이지 진입
    elif st.session_state.labels_modify_page:
        # 라벨 수정 페이지 진입
        labels_modify_page()
    elif st.session_state.search_recipe_page:
        # 레시피 검색 페이지 진입
        search_recipe_page()
        
        if st.session_state.cook:
            # 요리 안내
            cook()
    else:
        _, col1, _ = st.columns([3, 10, 1])

        with col1:
            st.image("app_gui/camera.png")

        header = st.markdown("""
                <style>
                    .title {
                            font-size: 40px;
                            color: #f481512;
                            font-family: 'Fira Code';
                            font-weight: bold;
                            background-color: #FAECFE;
                            color: #B761B4;
                            border-radius: 8px;
                            
                            border-radius: 8px;
                            text-align: center;
                            margin: 0px 0px 20px 0px;
                </style>
                <p class=title>
                    카메라 촬영
                </p>""", unsafe_allow_html=True)

        subheader = st.markdown("""
                <style>
                    .subheader {
                        font-size: 20px;
                        background-color: #FAECFE;
                        color: #B761B4;
                        text-align: center;
                        text-shadow: 3px  0px 0 #fff;
                        border-radius: 8px;
                        }
                </style>
                <p class=subheader>
                    AI 요리 비서가 레시피를 추천할 수 있도록 재료를 준비해주세요<br>
                준비가 완료되었다면 아래에 <strong>촬영 시작</strong> 버튼을 눌러주세요
                </p>""", unsafe_allow_html=True)

        _, col2, _ = st.columns([2, 5, 2])

        # '촬영 시작' 버튼 생성
        with col2:
            camera_button_placeholder = st.empty()
            camera_button_placeholder.button("촬영 시작", use_container_width=True, on_click=lambda: [enable_camera(), camera_button_placeholder.empty()])

        button = st.markdown("""
                <style>
                .stButton>button {
                    background-color: #f6c6fb;
                    color: #B761B4;
                    font-size: 25px;
                    font-weight: bold;
                    width: 100%;
                    height: 50px;
                    margin: 10px 0;
                    border: 2px solid #CDBDEB;
                }
                .stButton>button:hover {
                    background-color: #f67dfb;
                }
                </style>
            """, unsafe_allow_html=True)