import streamlit as st
from AvengersEnsemble import *
from Draw import *
from labels_modify_page import *
from search_recipe_page import *

# 예측 결과를 TensorBoard에 로깅하는 함수
def log_results_to_tensorboard(frame_image, boxes, confidences, labels):
    # TensorBoard에 로깅
    for _, (box, conf, label) in enumerate(zip(boxes, confidences, labels)):
        x1, y1, x2, y2 = box
        # 각 박스의 신뢰도 및 레이블 로깅
        st.session_state.writer.add_scalar(f'Boxes/{label}/Confidence', conf, st.session_state.frame_count)
        st.session_state.writer.add_scalar(f'Boxes/{label}/X1', x1, st.session_state.frame_count)
        st.session_state.writer.add_scalar(f'Boxes/{label}/Y1', y1, st.session_state.frame_count)
        st.session_state.writer.add_scalar(f'Boxes/{label}/X2', x2, st.session_state.frame_count)
        st.session_state.writer.add_scalar(f'Boxes/{label}/Y2', y2, st.session_state.frame_count)
    
    frame_array = np.array(frame_image) # 배열로 변환해서 로깅해야됨

    # 배열의 형태 확인 및 변환
    if len(frame_array.shape) == 3:  # (높이, 너비, 채널)
        frame_array = frame_array.transpose((2, 0, 1))  # (채널, 높이, 너비)로 변환(텐서보드가 요구하는 형식임)
    
    # 프레임 이미지를 TensorBoard에 로깅
    st.session_state.writer.add_image(f'Images/Frame_{st.session_state.frame_count}', frame_array, st.session_state.frame_count)

# 카메라 시작 함수
def show_camera():
    # 로컬 웹캠 열기
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("오류: 웹캠이 열려있지 않음.")
        return
    
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
                border: 7px outset #fdffb2;
            }
            .stButton>button:hover {
                background-color: #ffffD3;
                border: 7px outset #FFFF41;
            }
        </style>
    """, unsafe_allow_html=True)
        if st.button("**뒤로 가기**"):
            st.session_state.camera_running = False
            st.experimental_rerun()

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
        # frame_image = Image.fromarray(frame.astype(np.uint8))

        # 이미지 업데이트
        placeholder.image(frame_image, use_column_width=True)  # 빈 공간에 프레임 이미지 업데이트

        # 탐지된 라벨 업데이트
        for label in labels:
            st.session_state.detected_labels.add(label)
        
        # 탐지된 라벨 표시
        label_placeholder.markdown(f"""
            <style>
                .text {{
                        font-size: 29px;
                        color: #f481512;
                        font-family: 'Fira Code';
                        font-weight: bold;
                        color: #727421;
                        border-radius: 8px;
                        background-color: #fdffeb;
                        border: 10px dotted #fdffb2;
                        text-shadow: 3px  3px 0 #fff;
                        margin: 10px 0px 50px 0px;
                        border-radius: 8px;
                        padding: 10px 0px 10px 0px;
                        text-align: center;
                        }}
            </style>
            <p class="text">
                {", ".join(st.session_state.detected_labels)}
            </p>""", unsafe_allow_html=True)
        
        # TensorBoard에 로깅
        # log_results_to_tensorboard(frame_image, boxes, confidences, labels) # PIL 형식 이미지를 전달해야해서 output_image 전달

        # "재료 인식 종료 및 수정" 버튼 생성
        if not st.session_state.finish_recognizing_button:
            st.button("재료 인식 종료 및 수정", use_container_width=True, on_click=end_modify)
            st.session_state.finish_recognizing_button = True
            button = st.markdown("""
                <style>
                .stButton>button {
                    background-color: #fdffeb;
                    color: #727421;
                    font-size: 25px;
                    font-weight: bold;
                    width: 100%;
                    height: 50px;
                    margin: 10px 0;
                    border: 7px outset #fdffb2;
                }
                .stButton>button:hover {
                    background-color: #ffffD3;
                    border: 7px outset #FFFF41;
                }
                </style>
            """, unsafe_allow_html=True)

        # 프레임 카운터 증가
        # st.session_state.frame_count += 1

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()
    # st.session_state.writer.close() # Writer 닫기

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
        col1, _ = st.columns([10,10])

        with col1:
            empty = """<div style="height: 70px;"></div>"""
            st.markdown(empty, unsafe_allow_html=True)
            st.image("app_gui/camera_icon.png", width=600)

        subheader = st.markdown("""
                <style>
                    .subheader {
                        font-size: 25px;
                        background-color: #fdffeb;
                        color: #727421;
                        text-align: center;
                        text-shadow: 3px  0px 0 #fff;
                        border-radius: 8px;
                        margin: 50px 0px 50px 0px;
                        border: 10px outset #fdffb2;
                        }
                </style>
                <p class=subheader>
                    재료를 준비해주시고 <br> 아래에 <strong>촬영 시작</strong> 버튼을 눌러주세요
                </p>""", unsafe_allow_html=True)

        _, col2, _ = st.columns([2, 3, 2])

        # '촬영 시작' 버튼 생성
        with col2:
            buttonCSS = st.markdown("""
                    <style>
                    .stButton>button {
                        background-color: #fdffeb;
                        color: #727421;
                        font-size: 25px;
                        font-weight: bold;
                        width: 100%;
                        height: 50px;
                        margin: 10px 0;
                        border: 7px outset #fdffb2;
                    }
                    .stButton>button:hover {
                        background-color: #ffffD3;
                        border: 7px outset #FFFF41;
                    }
                    </style>
                """, unsafe_allow_html=True)
            if st.button("촬영 시작"):
                st.session_state.camera_running = True
                st.experimental_rerun()