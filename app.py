import streamlit as st
from streamlit_option_menu import option_menu
from camera_page import *
from input_page import *
from random_page import *

# =========================================================================================================
# 세션 상태 변수

if 'search_type' not in st.session_state:
    st.session_state.search_type = "메인 화면" # 검색 타입 변수
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False # 카메라 활성화 상태
if 'detected_labels' not in st.session_state:
    st.session_state.detected_labels = set() # 탐지된 라벨 집합
if 'finish_recognizing' not in st.session_state:
    st.session_state.finish_recognizing_button = False # 인식 마치기 버튼 활성화 상태
if 'labels_modify_page' not in st.session_state:
    st.session_state.labels_modify_page = False # 라벨 수정 페이지 활성화 상태
if 'edit_label' not in st.session_state:
    st.session_state.edit_label = {} # 라벨별 수정 가능여부 상태
if 'all_ingredients_include' not in st.session_state:
    st.session_state.all_ingredients_include = False # "모든 재료가 포함된 레시피만 보기" 체크박스 상태
if 'search_recipe_page' not in st.session_state:
    st.session_state.search_recipe_page = False # 검색 페이지 활성화 상태
if 'cook' not in st.session_state:
    st.session_state.cook = False # "요리하기" 단계 진입 활성화 상태
if 'selected_recipe' not in st.session_state:
    st.session_state.selected_recipe = None # 상세 레시피 정보 변수
if 'reset' not in st.session_state:
    st.session_state.reset = False # 처음으로 돌아가기
if 'random_recipe' not in st.session_state:
    st.session_state.random_recipe = random_recipe() # 초기 랜덤 레시피 로드
if 'hide_random_recipe_details' not in st.session_state:
    st.session_state.hide_random_recipe_details = False # 랜덤 레시피 상세안내 목록 숨기기 상태

# =========================================================================================================
# 함수

# 모든 세션 상태 변수 초기화 함수
def reset_session_state():
    st.session_state.search_type = "메인 화면"
    st.session_state.camera_running = False
    st.session_state.detected_labels = set()
    st.session_state.finish_recognizing_button = False
    st.session_state.labels_modify_page = False
    st.session_state.edit_label = {}
    st.session_state.all_ingredients_include = False
    st.session_state.search_recipe_page = False
    st.session_state.cook = False
    st.session_state.selected_recipe = None
    st.session_state.reset = False
    st.session_state.random_recipe = random_recipe()
    st.session_state.hide_random_recipe_details = False

def change_page(selected_search_type):
    st.session_state.search_type = selected_search_type
    
# def home():
#         # time.sleep(2)

#         # 글자 중앙으로 내리기 위해 공백 생성
#         empty = st.empty()
#         empty.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

#         # 이미지와 제목을 한 줄에 나란히 표시하기 위해 column 두개로 나눔
#         col1, col2 = st.columns([3, 8])

#         # col1 위치에 이미지
#         with col1:
#             st.image('app_gui/1.png', width=150)

#         # col2 위치에 프젝 이름
#         with col2:
#             # 홈페이지 중앙 제목
#             title = st.markdown("""
#             <style>
#                 .title {
#                     font-size: 65px;
#                     font-weight: bold;
#                     color: #f481512;
#                     text-shadow: 3px  0px 0 #fff;
#                     }
#             </style>
#             <p class=title>
#                 AI 요리 비서 ✨
#             </p>""", unsafe_allow_html=True)

#         # 위치 조정을 위한 공백
#         empty1 = st.empty()
#         empty1.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)


#         # 첫 화면 아래 설명글 첫번째
#         subtitle = st.markdown("""
#                     <style>
#                         .subtitle {
#                             font-size: 20px;
#                             color: #f481512;
#                             font-family: 'Fira Code';
#                             font-weight: bold;
#                             background-color: #CDBDEB;
#                             color: #9A81B0;
#                             border-radius: 8px;
#                             border: 2px solid #fff;
#                             margin: 50px 0px 50px 0px;
#                             border-radius: 8px;
#                             padding: 10px 0px 10px 0px;
#                             text-align: center;
#                             }
#                     </style>
#                     <p class=subtitle>
#                         옵션 선택 창에서 사용하실 메뉴를 선택해주세요.
#                     </p>
#                             """, unsafe_allow_html=True)

#         # 첫 화면 아래 설명글 두번째
#         explanation = st.markdown("""
#                         <style>
#                             .explanation {
#                                 font-size: 20px;
#                                 color: #9A81B0;
#                                 font-weight: bold;
#                                 background-color: #CDBDEB;
#                                 font-family: 'Fira Code';
#                                 text-align: left;
#                                 padding: 10px 40px 10px 40px;
#                                 border-radius: 8px;
#                                 margin: 0px 0px 0px 0px;
#                                 }
#                         </style>
#                         <p class=explanation>
#                             카메라: 사용자의 식재료를 카메라로 실시간 인식하여 레시피 추천 <br>
#                             직접 입력: 사용자가 직접 입력하여 레시피 추천<br>
#                             랜덤 추천: 랜덤으로 하나의 레시피 추천 
#                         </p>""", unsafe_allow_html=True)

# 첫 화면 함수
def home():

    st.image('app_gui/title.png', width=650)

    # 첫 화면 아래 설명글 첫번째
    subtitle = st.markdown("""
                <style>
                    .subtitle {
                        font-size: 29px;
                        color: #f481512;
                        font-family: 'Fira Code';
                        font-weight: bold;
                        color: #4f704b;
                        border-radius: 8px;
                        background-color: #e3fedb;
                        border: 10px outset #c0fdb4;
                        text-shadow: 3px  3px 0 #fff;
                        margin: 50px 0px 50px 0px;
                        border-radius: 8px;
                        padding: 10px 0px 10px 0px;
                        text-align: center;
                        }
                </style>
                <p class=subtitle>
                    사용하실 메뉴를 선택해 주세요
                </p>
                        """, unsafe_allow_html=True)


    # # 첫 화면 아래 설명글 두번째
    explanation = st.markdown("""
                <style>
                    .explanation {
                        font-size: 20px;
                        color: #4f704b;
                        font-weight: bold;
                        background-color: #e3fedb;
                        border: 10px outset #c0fdb4;
                        text-shadow: 2px  2px 0 #fff;
                        font-family: 'Fira Code';
                        text-align: left;
                        padding: 10px 40px 10px 40px;
                        border-radius: 8px;
                        margin: 0px 0px 0px 0px;
                        }
                </style>
                <p class=explanation>
                    카메라: 사용자의 식재료를 카메라로 실시간 인식하여 레시피 추천 <br>
                    직접 입력: 사용자가 직접 입력하여 레시피 추천<br>
                    랜덤 추천: 랜덤으로 하나의 레시피 추천 
                </p>""", unsafe_allow_html=True)

# def main():
#     side, main = st.columns([1, 9])

#     with side:
#         st.sidebar.title("메뉴")
#         menu = ["옵션 선택", "카메라", "직접 입력", "랜덤 추천"]
#         selected_search_type = st.sidebar.selectbox("", options=menu, index=menu.index(st.session_state.search_type))
#         change_page(selected_search_type)
        
#         page_bg_img = '''
#             <style>
#             .stApp {
#                 background-color: #ff0;
#                 background-size: cover;
#             }
#             .stApp > header {
#                 background-color: #ff0;
#                 background-size: cover;
#             }

#             .st-emotion-cache-6qob1r {
#                 background-color: #90EE90;  /* 연한 녹색 */
#                 background-size: cover;
#             }
#             </style>
#             '''
#         st.markdown(page_bg_img, unsafe_allow_html=True)
#     with main:
#         if st.session_state.search_type == "옵션 선택":
#             home()
            
#         if st.session_state.search_type == "카메라":
#             st.sidebar.button("**처음으로 돌아가기**")
#             camera_page()
        
#         if st.session_state.search_type == "직접 입력":
#             st.sidebar.button("**처음으로 돌아가기**")
#             text_input()
        
#         if st.session_state.search_type == "랜덤 추천":
#             st.sidebar.button("**처음으로 돌아가기**")
#             random_page()

# side, main 영역별 기능
def main():
    if st.session_state.reset:
        st.session_state.reset = False
        st.experimental_rerun()

    side, main = st.columns([1, 9])

    with side:
        with st.sidebar:
            menu = option_menu("메뉴", ["메인 화면", "카메라", "직접 입력", "랜덤 추천"], icons=['house', 'camera', 'pencil', 'shuffle'], # 아이콘 추가
        menu_icon="cast", # 기본 메뉴 아이콘
        default_index=0, # 기본 선택된 인덱스
        )
            change_page(menu)
    with main:
        if st.session_state.search_type == "메인 화면":
            reset_session_state() # 모든 세션 상태 변수 초기화
            home()
            
        if st.session_state.search_type == "카메라":
            camera_page()
        
        if st.session_state.search_type == "직접 입력":
            if not st.session_state.search_recipe_page:
                st.session_state.labels_modify_page = True
            
            text_input()
        
        if st.session_state.search_type == "랜덤 추천":
            random_page()

# =========================================================================================================
# 페이지 함수 호출

# 페이지 기본 설정
st.set_page_config(
    page_title='MultiCampus AvengersEnsemble',
    page_icon='app_gui/1.png'
)

# background
background = '''
    <style>
    .stApp {
        background-image: url("https://github.com/Seunghwan-Ji/final-project/blob/jin/app_gui/table-wood-fresh-organic.jpg?raw=true");
        background-color: #dcd0c3;
        background-size: cover;
        background-position: center;
        min-height: 100vh;
    }
    .stApp > header {
        background-color: #f2e4d7;
        background-size: cover;
    }

    .st-emotion-cache-6qob1r {
        background-color: #dcd0c3;
        background-size: cover;
    }
    </style>
    '''
st.markdown(background, unsafe_allow_html=True)

# 시작
if __name__ == "__main__":
    main()