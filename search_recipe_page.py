import streamlit as st
from Recipe import *
from Cook import *

# 검색 모드가 활성화된 경우
def search_recipe_page():
    # button CSS
    st.markdown("""
        <style>
            .stButton > button {
                background-color: #fdffeb;
                color: #727421;
                font-size: 25px;
                font-weight: bold;

                height: 50px;
                border:5px outset #fdffb2;
            }
            .stButton > button:hover {
                background-color: #ffffD3;
                border: 7px outset #FFFF41;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.image("app_gui/user.png", width=650)
    st.markdown(f"""
    <style>
        .user_ingredients {{
            font-size: 30px;
            color: #f481512;
            font-family: 'Fira Code';
            font-weight: bold;
            color: #727421;
            border-radius: 8px;
            background-color: #fdffeb;
            border: 5px dotted  #fdffb2;
            text-shadow: 3px  3px 0 #fff;
            text-align: center;
            padding: 5px 5px 5px 5px;
            margin: 50px 0px 50px 0px;
            }}
    </style>
    <p class=user_ingredients>
        {", ".join(st.session_state.detected_labels)}
    </p>
    """, unsafe_allow_html=True)
    
    
    # checkbox CSS
    st.markdown("""
        <style>
            .stCheckbox > label {
                font-size: 20px;
                font-weight: bold;
                color: #4f704b;
                background-color: #fdffeb;
                padding: 5px;
                border-radius: 8px;
                border: 5px dotted #fdffb2;
                display: flex;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Streamlit 체크박스 생성
    st.session_state.all_ingredients_include = st.checkbox("모든 재료를 포함한 레시피 보기")

    # st.markdown("""
    # <style>
    #      .stRadio > div > label {
    #         font-size: 20px;
    #         font-weight: bold;
    #         color: #4f704b;
    #         background-color: #fdffeb;
    #         padding: 0px 5px 0px 5px;
    #         border-radius: 10px;
    #         border: 2px solid #fdffb2;

    #         transition: background-color 0.3s ease;
    #     }
    #     .stRadio label div {
    #         font-size: 20px;
    #         color: #4f704b;
    #         padding: 0px 5px 0px 5px;
    #         display: flex;
    #         flex-direction: column;
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)

    # sort = st.radio(
    #     "",
    #     ["추천순", "조회순", "스크랩순"],
    #     captions=[
    #         "추천이 가장 많은 레시피 순서",
    #         "가장 많이 조회한 레시피 순서",
    #         "스크랩이 많이 된 레시피 순서",
    #     ], index=None)
    
    # selected = ()
    # if sort == '추천순':
    #     selected = ("추천수", "추천순")
    # elif sort == '조회순':
    #     selected = ("조회수", "조회순")
    # elif sort == '스크랩순':
    #     selected = ("스크랩수", "스크랩순")
    
    col1, col2, col3 = st.columns([5, 5, 5])
# stHorizontalBlock
    # 버튼 클릭 처리
    selected = None
    with col1:
        st.markdown("""
        <style>
            .stHorizontalBlock.stButton > button {
                background-color: #fdffeb;
                color: #727421;
                font-size: 25px;
                font-weight: bold;
                width: 100%;
                margin: 0px 0;
                border: 7px outset #fdffb2;
            }
            .stButton>button:hover {
                background-color: #ffffD3;
                border: 7px outset #FFFF41;
            }
            </style>
        </style>
        """, unsafe_allow_html=True)
        if st.button("추천순"):
            selected = ("추천수")
    with col2:
        if st.button("조회순"):
            selected = ("조회수", "조회순")
    
    with col3:
        if st.button("스크랩순"):
            selected = ("스크랩수", "스크랩순")

    if selected:
        if st.session_state.all_ingredients_include:
            # 모든 재료가 포함된 레시피 추천
            recipe_results = search_all_include(st.session_state.detected_labels)
        else:
            # 인식한 식재료 중 하나라도 포함된 레시피 추천
            recipe_results = search_include_at_least_one(st.session_state.detected_labels)
        
        if recipe_results.shape[0] > 0:
            recipe_results = recipe_results.sort_values(by=selected[0], ascending=False)
            recipe_results = recipe_results.set_index('요리명') # '요리명' 열을 인덱스로 전환


            st.markdown(f"""
                <style>
                    .recipe_subheader {{
                        font-size: 25px;
                        background-color: #fdffeb;
                        color: #727421;
                        text-align: center;
                        text-shadow: 3px  0px 0 #fff;
                        border-radius: 8px;
                        margin: 50px 0px 10px 0px;
                        border: 2px outset #fdffb2;
                        width: 300px;
                        }}
                </style>
                <p class=recipe_subheader>
                    {selected[1]} 레시피🧑‍🍳
                </p>""", unsafe_allow_html=True)
            
            st.markdown("""
                        <style>
                            .dvn-scroller.glideDataEditor {
                                border: 10px outset #fdffb2;
                            }
                        </style>
                        """,  unsafe_allow_html=True)
            st.write(recipe_results)
            st.session_state.cook = True
            
        else:
            st.write("검색 결과가 없습니다.")

        

    

    if st.session_state.cook == False:

        if st.button("뒤로 가기"):
            st.session_state.search_recipe_page = False
            st.session_state.labels_modify_page = True
            if st.session_state.selected_recipe: # 검색 내역 확인
                st.session_state.hide_random_recipe_details = True # 검색 내역 숨기기
            st.experimental_rerun()

def cook(random_recipe=False, recipe_name=None):
    # st.text("\n")
    # st.text("\n")
    # st.title("레시피를 시각적으로 보여드리겠습니다!")
    st.image("app_gui/show_recipe.png")

    if not random_recipe:
        # 검색 기능
        recipe_name = st.text_input("요리할 '요리명'을 입력하세요:")

    clicked = False
    if not random_recipe:
        if st.button("검색"):
            if recipe_name:
                st.session_state.hide_random_recipe_details = False
                clicked = True
                status_placeholder = st.empty() # 빈 자리표시자 생성
                status_placeholder.text("검색 중입니다...")
        if st.button("뒤로 가기"):
            st.session_state.search_recipe_page = False
            st.session_state.labels_modify_page = True
            if st.session_state.selected_recipe: # 검색 내역 확인
                st.session_state.hide_random_recipe_details = True # 검색 내역 숨기기
            st.experimental_rerun()
    elif random_recipe:
        if st.button(f"'{recipe_name}' 레시피 상세안내 보기"):
            st.session_state.hide_random_recipe_details = False
            clicked = True
            status_placeholder = st.empty() # 빈 자리표시자 생성
            status_placeholder.text("로드 중입니다...")

    if clicked:
        recipe_url = get_valid_recipe_url(recipe_name)
        if recipe_url:
            recipe_info = get_recipe_info(recipe_url)
            st.session_state.selected_recipe = recipe_info
        else:
            st.session_state.selected_recipe = None
            st.text(f"'{recipe_name}' 레시피의 시각적인 정보를 찾지 못했습니다.")
        
        # 검색 완료 후 텍스트 제거
        status_placeholder.empty()

    # 검색 결과 표시
    if st.session_state.selected_recipe and not st.session_state.hide_random_recipe_details:
        st.text("\n")
        st.text("\n")
        st.subheader("요리 안내")
        
        # 요리된 사진
        st.image(st.session_state.selected_recipe["photo_url"], caption=recipe_name)
        
        # 재료
        st.text("\n")
        st.text("\n")
        st.subheader("재료")
        st.text(st.session_state.selected_recipe["ingredients"])

        # 요리 영상
        st.text("\n")
        st.text("\n")
        st.subheader("요리 영상")
        if st.session_state.selected_recipe["video_url"]:
            st.video(st.session_state.selected_recipe["video_url"])
        else:
            st.text("요리 영상이 없습니다.")

        # 조리 순서
        st.text("\n")
        st.text("\n")
        st.subheader("조리 순서")
        for step in st.session_state.selected_recipe["steps"]:
            st.text(step["text"])
            if step["image_url"]:
                st.image(step["image_url"])
            st.text("\n")
            st.text("\n")
            st.text("\n")
            st.text("\n")
            st.text("\n")
        
        # 팁/주의사항
        st.text("\n")
        st.text("\n")
        st.subheader("팁/주의사항")
        st.text(st.session_state.selected_recipe["tips"])
        
