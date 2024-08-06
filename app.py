
import streamlit as st
from AvengersEnsemble import *
from Draw import *
from Recipe import *
from camera_page import *
from input_page import *
from random_page import *


# 페이지 기본 설정
st.set_page_config(
    page_title='MultiCampus AvengersEnsemble',
    page_icon='app_gui/1.png'
)


# 상태 변수 초기화
if 'page' not in st.session_state:
    st.session_state.page = "옵션 선택"
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False  # 카메라 상태 초기화
if 'detected_labels' not in st.session_state:
    st.session_state.detected_labels = set()  # 탐지된 라벨 상태 초기화
if 'all_ingredients' not in st.session_state:
    st.session_state.all_ingredients = False  # 체크박스 상태 초기화
if 'modify_mode' not in st.session_state:
    st.session_state.modify_mode = False
if 'edit_label' not in st.session_state:
    st.session_state.edit_label = {}
if 'search_mode' not in st.session_state:
    st.session_state.search_mode = False
if 'first_page' not in st.session_state:
    st.session_state.first_page = False


def change_page(select_page):
    st.session_state.page = select_page
    
def home():
        # time.sleep(2)

        # 글자 중앙으로 내리기 위해 공백 생성
        empty = st.empty()
        empty.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

        # 이미지와 제목을 한 줄에 나란히 표시하기 위해 column 두개로 나눔
        col1, col2 = st.columns([3, 8])

        # col1 위치에 이미지
        with col1:
            st.image('app_gui/1.png', width=150)

        # col2 위치에 프젝 이름
        with col2:
            # 홈페이지 중앙 제목
            title = st.markdown("""
            <style>
                .title {
                    font-size: 65px;
                    font-weight: bold;
                    color: #f481512;
                    text-shadow: 3px  0px 0 #fff;
                    }
            </style>
            <p class=title>
                AI 요리 비서 ✨
            </p>""", unsafe_allow_html=True)

        # 위치 조정을 위한 공백
        empty1 = st.empty()
        empty1.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)


        # 첫 화면 아래 설명글 첫번째
        subtitle = st.markdown("""
                    <style>
                        .subtitle {
                            font-size: 20px;
                            color: #f481512;
                            font-family: 'Fira Code';
                            font-weight: bold;
                            background-color: #CDBDEB;
                            color: #9A81B0;
                            border-radius: 8px;
                            border: 2px solid #fff;
                            margin: 50px 0px 50px 0px;
                            border-radius: 8px;
                            padding: 10px 0px 10px 0px;
                            text-align: center;
                            }
                    </style>
                    <p class=subtitle>
                        옵션 선택 창에서 사용하실 메뉴를 선택해주세요.
                    </p>
                            """, unsafe_allow_html=True)

        # 첫 화면 아래 설명글 두번째
        explanation = st.markdown("""
                        <style>
                            .explanation {
                                font-size: 20px;
                                color: #9A81B0;
                                font-weight: bold;
                                background-color: #CDBDEB;
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

def main():
    side, main = st.columns([1, 9])

    with side:
        st.sidebar.title("메뉴")
        menu = ["옵션 선택", "카메라", "직접 입력", "랜덤 추천"]
        select_page = st.sidebar.selectbox("", options=menu, index=menu.index(st.session_state.page))
        change_page(select_page)
        

        st.markdown(page_bg_img, unsafe_allow_html=True)
    with main:
        # time.sleep(1) 
        if st.session_state.page == "옵션 선택":
            home()
            
        if st.session_state.page == "카메라":
            st.session_state.all_ingredients = st.sidebar.checkbox("모든 재료를 포함한 레시피 보기")
            camera()
            st.sidebar.button("**처음으로 돌아가기**")
        
        if st.session_state.page == "직접 입력":
            st.session_state.all_ingredients = st.sidebar.checkbox("모든 재료를 포함한 레시피 보기")
            st.sidebar.button("**처음으로 돌아가기**")
            text_input()
        
        if st.session_state.page == "랜덤 추천":
            st.sidebar.button("**처음으로 돌아가기**")
            random_page()



# 배경 부분
page_bg_img = '''
    <style>
    .stApp {
        background-color: #ff0;
        background-size: cover;
    }
    .stApp > header {
        background-color: #ff0;
        background-size: cover;
    }

    .st-emotion-cache-6qob1r {
        background-color: #90EE90;  /* 연한 녹색 */
        background-size: cover;
    }
    </style>
    '''


if __name__ == "__main__":
    main()