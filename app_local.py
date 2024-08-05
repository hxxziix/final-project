import streamlit as st
from AvengersEnsemble import *
from Draw import *
from Recipe import *
import random

# =========================================================================================================
# 세션 상태 변수

if 'all_ingredients_include' not in st.session_state:
    st.session_state.all_ingredients_include = False  # "모든 재료가 포함된 레시피만 보기" 체크박스 상태 초기화
if 'search_type' not in st.session_state:
    st.session_state.search_type = None  # 검색 타입 초기화
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False  # 카메라 활성화 상태 초기화
if 'detected_labels' not in st.session_state:
    st.session_state.detected_labels = set()  # 탐지된 라벨 집합 초기화
if 'finish_recognizing' not in st.session_state:
    st.session_state.finish_recognizing_button = False # 인식 마치기 버튼 활성화 상태 초기화
if 'labels_modify_mode' not in st.session_state:
    st.session_state.labels_modify_mode = False # 라벨 수정모드 상태 초기화
if 'edit_label' not in st.session_state:
    st.session_state.edit_label = {} # 라벨별 수정 가능여부 상태 초기화
if 'search_mode' not in st.session_state:
    st.session_state.search_mode = False # 검색 모드 상태 초기화

# =========================================================================================================
# 함수

# 모드 변경 함수
def change_mode(mode):
    st.session_state.search_type = mode
    st.session_state.detected_labels = set()  # 모드 변경 시 탐지된 라벨 초기화

# 카메라 활성화 함수
def start_camera():
    st.session_state.camera_running = True
    st.session_state.detected_labels.clear()
    st.session_state.labels_modify_mode = False

# 카메라 비활성화 함수
def stop_camera():
    st.session_state.camera_running = False

# 카메라 시작 함수
def show_camera():
    # 로컬 웹캠 열기
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("오류: 웹캠이 열려있지 않음.")
        return

    def end_modify(): # "재료 인식 종료 및 수정" 버튼을 클릭하면 호출되는 함수
        st.session_state.camera_running = False
        st.session_state.finish_recognizing_button = False
        st.session_state.labels_modify_mode = True

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

# =========================================================================================================
# UI

# 페이지 기본 설정
st.set_page_config(
    page_title='MultiCampus Avengers Ensemble',
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

# 체크박스 추가
st.session_state.all_ingredients_include = st.checkbox("모든 재료가 포함된 레시피만 보기")

if st.session_state.search_type == None:
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

# 수정 모드가 활성화된 경우
if st.session_state.labels_modify_mode:
    def back_to_main():
        st.session_state.labels_modify_mode = False
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

    if st.button("다음"):
        st.session_state.labels_modify_mode = False
        st.session_state.search_mode = True
        st.experimental_rerun()

# 검색 모드가 활성화된 경우
if st.session_state.search_mode and st.session_state.detected_labels:
    def back_to_main():
        st.session_state.labels_modify_mode = True
        st.session_state.search_mode = False
    
    st.button("🔙", on_click=back_to_main)

    sort = st.radio(
        "정렬 기준",
        ["추천순", "조회순", "스크랩순"],
        captions=[
            "추천이 가장 많은 레시피 순서",
            "가장 많이 조회한 레시피 순서",
            "스크랩이 많이 된 레시피 순서",
        ], index=None)
    if sort == '추천순':
        if st.session_state.all_ingredients_include:
            # 모든 재료가 포함된 레시피 추천
            recipe_results = search_all_include(st.session_state.detected_labels)
        else:
            # 인식한 식재료 중 하나라도 포함된 레시피 추천
            recipe_results = search_include_at_least_one(st.session_state.detected_labels)
        
        recipe_results = recipe_results.sort_values(by='추천수', ascending=False)
        st.subheader("추천순 레시피🧑‍🍳")
        st.write(recipe_results)

    elif sort == '조회순':
        if st.session_state.all_ingredients_include:
            # 모든 재료가 포함된 레시피 추천
            recipe_results = search_all_include(st.session_state.detected_labels)
        else:
            # 인식한 식재료 중 하나라도 포함된 레시피 추천
            recipe_results = search_include_at_least_one(st.session_state.detected_labels)
        
        recipe_results = recipe_results.sort_values(by='조회수', ascending=False)
        st.subheader("조회순 레시피🧑‍🍳")
        st.write(recipe_results)

    elif sort == '스크랩순':
        if st.session_state.all_ingredients_include:
            # 모든 재료가 포함된 레시피 추천
            recipe_results = search_all_include(st.session_state.detected_labels)
        else:
            # 인식한 식재료 중 하나라도 포함된 레시피 추천
            recipe_results = search_include_at_least_one(st.session_state.detected_labels)
        
        recipe_results = recipe_results.sort_values(by='스크랩수', ascending=False)
        st.subheader("스크랩순 레시피🧑‍🍳")
        st.write(recipe_results)

# 촬영하여 검색 버튼 눌렀을 때
if st.session_state.search_type == 'camera':

    # 카메라 시작 버튼
    if not st.session_state.camera_running and not st.session_state.labels_modify_mode and not st.session_state.search_mode:
        st.button("Camera Start", on_click=start_camera, use_container_width=True)
    
    placeholder = st.empty()  # 영상 출력을 위한 빈 공간 정의
    label_placeholder = st.empty()  # 탐지된 라벨을 표시할 빈 공간 정의

    # 버튼이 클릭되었을 때 카메라 화면 표시 함수 호출
    if st.session_state.camera_running:
        show_camera()


# 식재료 입력을 통한 검색
elif st.session_state.search_type == 'input':

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

            if st.session_state.all_ingredients_include:
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

            if st.session_state.all_ingredients_include:
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

            if st.session_state.all_ingredients_include:
                # 모든 재료가 포함된 레시피 추천
                recipe_results = search_all_include(st.session_state.detected_labels)
            else:
                # 인식한 식재료 중 하나라도 포함된 레시피 추천
                recipe_results = search_include_at_least_one(st.session_state.detected_labels)
            recipe_results = recipe_results.sort_values(by='스크랩수', ascending=False)
            st.subheader("스크랩순 레시피🧑‍🍳")
            st.write(recipe_results)

# 랜덤 추천
elif st.session_state.search_type == 'random':
    random_number = random.randint(0, 184990)
    recipe_results = random_recipe(random_number)
    st.subheader("랜덤 추천 레시피🧑‍🍳")
    st.write(recipe_results)