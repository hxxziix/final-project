import streamlit as st
from PIL import Image
import cv2
from AvengersEnsemble import *
from Draw import *
from Recipe import *
import json
import random

# label 번역 위한 json 파일
with open('search_recipe/mapping_dict.json', 'r', encoding='UTF-8') as json_file:
    kor_label = json.load(json_file)

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

# 상태 변수 초기화
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False  # 카메라 상태 초기화
if 'detected_labels' not in st.session_state:
    st.session_state.detected_labels = set()  # 탐지된 라벨 상태 초기화
if 'all_ingredients' not in st.session_state:
    st.session_state.all_ingredients = False  # 체크박스 상태 초기화
if 'mode' not in st.session_state:
    st.session_state.mode = None  # 모드 상태 초기화

# 모드 변경 함수 정의
def change_mode(mode):
    st.session_state.mode = mode
    st.session_state.detected_labels = set()  # 모드 변경 시 탐지된 라벨 초기화

# 카메라 검색일 때 촬영 버튼 클릭 이벤트 처리
def start_camera():
    st.session_state.camera_running = True

def stop_camera():
    st.session_state.camera_running = False


# 체크박스 추가
st.session_state.all_ingredients = st.checkbox("모든 재료가 포함된 레시피만 보기")

# 촬영하여 검색 및 식재료 입력으로 검색 버튼 추가
col3, col4, col5 = st.columns(3)

# 카메라 검색 버튼
with col3:
    c3 = st.container()
    if c3.button("촬영하여 검색", use_container_width=True):
        change_mode('camera')

# 입력 검색 버튼
with col4:
    c4 = st.container()
    if c4.button("식재료 입력으로 검색", use_container_width=True):
        change_mode('input')

# 랜덤 추천 버튼
with col5:
    c5 = st.container()
    if c5.button("레시피 랜덤 추천", use_container_width=True):
        change_mode('random')


placeholder = st.empty()  # 영상 출력을 위한 빈 공간 정의


# 카메라 검색 함수
def show_camera():
        # 로컬 웹캠 열기
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("오류: 웹캠이 열려있지 않음.")
            return
        
        detected_labels = set()
        # placeholder = st.empty()  # 영상 출력을 위한 빈 공간 정의
        # label_placeholder = st.empty()  # 탐지된 라벨을 표시할 빈 공간 정의

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
                detected_labels.add(label)
            
            st.session_state.detected_labels = [kor_label[label] if label in kor_label else label for label in detected_labels]
            
            
            if st.session_state.detected_labels:
                label_placeholder.markdown(f"""
                    <style>
                        .text {{
                            font-size: 35px;
                            color: #f481512;
                            text-shadow: 3px  0px 0 #fff;}}
                    </style>
                    <p class="text">
                        📸탐지된 식재료 : {",".join(st.session_state.detected_labels)}
                    </p>""", unsafe_allow_html=True)



        # 자원 해제
        cap.release()
        cv2.destroyAllWindows()


# 촬영하여 검색 버튼 눌렀을 때
if st.session_state.mode == 'camera':
    
    # 카메라 버튼 추가
    if not st.session_state.camera_running:
        st.button("Camera Start", on_click=start_camera, use_container_width=True)

    if st.session_state.camera_running:
        st.button("Camera Stop", on_click=stop_camera, use_container_width=True)
    
    label_placeholder = st.empty()  # 탐지된 라벨을 표시할 빈 공간 정의  
      
    # 버튼이 클릭되었을 때 카메라 화면 표시 함수 호출
    if st.session_state.camera_running:
        show_camera()
        
    # 레시피 결과 업데이트
    if st.session_state.detected_labels:
        sort = st.radio(
            "정렬 기준",
            ["추천순", "조회순", "스크랩순"],
            captions=[
                "추천이 가장 많은 레시피 순서",
                "가장 많이 조회한 레시피 순서",
                "스크랩이 많이 된 레시피 순서",
            ], index=None)
        label_placeholder.markdown(f"""
            <style>
                .text {{
                    font-size: 35px;
                    color: #f481512;
                    text-shadow: 3px  0px 0 #fff;}}
            </style>
            <p class="text">
                📸탐지된 식재료 : {",".join(st.session_state.detected_labels)}
            </p>""", unsafe_allow_html=True)
        if sort == '추천순':
            if st.session_state.all_ingredients:
                # 모든 재료가 포함된 레시피 추천
                recipe_results = search_all_include(st.session_state.detected_labels)
            else:
                # 인식한 식재료 중 하나라도 포함된 레시피 추천
                recipe_results = search_include_at_least_one(st.session_state.detected_labels)
            
            recipe_results = recipe_results.sort_values(by='추천수', ascending=False)
            st.subheader("추천순 레시피🧑‍🍳")
            st.write(recipe_results)
        elif sort == '조회순':
            if st.session_state.all_ingredients:
                # 모든 재료가 포함된 레시피 추천
                recipe_results = search_all_include(st.session_state.detected_labels)
            else:
                # 인식한 식재료 중 하나라도 포함된 레시피 추천
                recipe_results = search_include_at_least_one(st.session_state.detected_labels)
            
            recipe_results = recipe_results.sort_values(by='조회수', ascending=False)
            st.subheader("조회순 레시피🧑‍🍳")
            st.write(recipe_results)
        elif sort == '스크랩순':
            if st.session_state.all_ingredients:
                # 모든 재료가 포함된 레시피 추천
                recipe_results = search_all_include(st.session_state.detected_labels)
            else:
                # 인식한 식재료 중 하나라도 포함된 레시피 추천
                recipe_results = search_include_at_least_one(st.session_state.detected_labels)
            
            recipe_results = recipe_results.sort_values(by='스크랩수', ascending=False)
            st.subheader("스크랩순 레시피🧑‍🍳")
            st.write(recipe_results)



# 식재료 입력을 통한 검색
elif st.session_state.mode == 'input':

    sort = st.radio(
    "정렬 기준",
    ["추천순", "조회순", "스크랩순"],
    captions=[
        "추천이 가장 많은 레시피 순서",
        "가장 많이 조회한 레시피 순서",
        "스크랩이 많이 된 레시피 순서",
    ], index=None)
    
    if sort == "추천순":
        input_ingredients = st.text_input(":eggplant: 식재료를 입력하세요 (쉼표로 구분)")
        if st.button("검색"):
            ingredients = [ingredient.strip() for ingredient in input_ingredients.split(',')]
            st.session_state.detected_labels = ingredients

            if st.session_state.all_ingredients:
                # 모든 재료가 포함된 레시피 추천
                recipe_results = search_all_include(st.session_state.detected_labels)
            else:
                # 인식한 식재료 중 하나라도 포함된 레시피 추천
                recipe_results = search_include_at_least_one(st.session_state.detected_labels)
            recipe_results = recipe_results.sort_values(by='추천수', ascending=False)
            st.subheader("추천순 레시피🧑‍🍳")
            st.write(recipe_results)
    elif sort == '조회순':
        input_ingredients = st.text_input(":mushroom: 식재료를 입력하세요 (쉼표로 구분)")
        if st.button("검색"):
            ingredients = [ingredient.strip() for ingredient in input_ingredients.split(',')]
            st.session_state.detected_labels = ingredients

            if st.session_state.all_ingredients:
                # 모든 재료가 포함된 레시피 추천
                recipe_results = search_all_include(st.session_state.detected_labels)
            else:
                # 인식한 식재료 중 하나라도 포함된 레시피 추천
                recipe_results = search_include_at_least_one(st.session_state.detected_labels)
            recipe_results = recipe_results.sort_values(by='조회수', ascending=False)
            st.subheader("조회순 레시피🧑‍🍳")
            st.write(recipe_results)

    else:
        input_ingredients = st.text_input(":fork_and_knife: 식재료를 입력하세요 (쉼표로 구분)")
        if st.button("검색"):
            ingredients = [ingredient.strip() for ingredient in input_ingredients.split(',')]
            st.session_state.detected_labels = ingredients

            if st.session_state.all_ingredients:
                # 모든 재료가 포함된 레시피 추천
                recipe_results = search_all_include(st.session_state.detected_labels)
            else:
                # 인식한 식재료 중 하나라도 포함된 레시피 추천
                recipe_results = search_include_at_least_one(st.session_state.detected_labels)
            recipe_results = recipe_results.sort_values(by='스크랩수', ascending=False)
            st.subheader("스크랩순 레시피🧑‍🍳")
            st.write(recipe_results)










# 랜덤 추천
elif st.session_state.mode == 'random':
    random_number = random.randint(0, 184990)
    recipe_results = random_recipe(random_number)
    st.subheader("랜덤 추천 레시피🧑‍🍳")
    st.write(recipe_results)
