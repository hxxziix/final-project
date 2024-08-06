import streamlit as st
from Recipe import *

# 검색 모드가 활성화된 경우
def search_recipe_page():
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
        
        recipe_results = recipe_results.sort_values(by=selected[0], ascending=False)
        st.subheader(f"{selected[1]} 레시피🧑‍🍳")
        st.write(recipe_results)