import streamlit as st
from Recipe import *
from Cook import *

# 검색 모드가 활성화된 경우
def search_recipe_page():
    st.write("나의 식재료:")
    st.write(", ".join(st.session_state.detected_labels))

    st.session_state.all_ingredients_include = st.checkbox("모든 재료를 포함한 레시피 보기")

    sort = st.radio(
        "정렬 기준",
        ["추천순", "조회순", "스크랩순"],
        captions=[
            "추천이 가장 많은 레시피 순서",
            "가장 많이 조회한 레시피 순서",
            "스크랩이 많이 된 레시피 순서",
        ], index=None)
    
    selected = ()
    if sort == '추천순':
        selected = ("추천수", "추천순")
    elif sort == '조회순':
        selected = ("조회수", "조회순")
    elif sort == '스크랩순':
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

            st.subheader(f"{selected[1]} 레시피🧑‍🍳")
            st.write(recipe_results)

            st.session_state.cook = True
        else:
            st.write("검색 결과가 없습니다.")

def cook(random_recipe=False, recipe_name=None):
    st.text("\n")
    st.text("\n")
    st.title("레시피를 시각적으로 보여드리겠습니다!")

    if not random_recipe:
        # 검색 기능
        recipe_name = st.text_input("요리할 '요리명'을 입력하세요:")

    clicked = False
    if not random_recipe:
        if st.button("검색"):
            if recipe_name:
                clicked = True
                status_placeholder = st.empty() # 빈 자리표시자 생성
                status_placeholder.text("검색 중입니다...")
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
        if st.session_state.selected_recipe["video_url"]:
            st.text("\n")
            st.text("\n")
            st.subheader("요리 영상")
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