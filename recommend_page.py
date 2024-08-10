import streamlit as st
from recipe_recommend import *
from make_recommend_df import *
from personal_recipe import *

def recommend_page():
    st.title('레시피 추천 시스템')

    # 레시피 ID를 입력받는 텍스트 필드
    new_id = st.text_input("추가할 레시피 ID를 입력하세요:", "")

    # 레시피 ID 추가 버튼
    if st.button("레시피 ID 추가"):
        if new_id.isdigit():
            add_recipe_id(int(new_id))
            st.success(f"레시피 ID {new_id}이(가) 추가되었습니다.")
        else:
            st.error("유효한 숫자를 입력하세요.")

    # 현재 레시피 ID 리스트 보여주기
    st.subheader("현재 저장된 레시피 목록:")
    recipe_ids = get_recipe_ids()
    if recipe_ids:
        # 추천 데이터프레임 가져오기
        recommend_df = get_recommend_df()
        
        # 저장된 레시피 ID에 해당하는 요리명 가져오기
        saved_recipes = recommend_df[recommend_df['레시피일련번호'].isin(recipe_ids)]
        if not saved_recipes.empty:
            st.write("저장된 레시피:")
            st.dataframe(saved_recipes[['레시피일련번호', '요리명']])  # 요리명과 레시피 ID만 표시
        else:
            st.write("저장된 레시피가 없습니다.")
    else:
        st.write("저장된 레시피 ID가 없습니다.")

    # 레시피 ID 리스트 초기화 버튼
    if st.button("레시피 ID 리스트 초기화"):
        clear_recipe_ids()
        st.warning("레시피 ID 리스트가 초기화되었습니다.")

    # 추천 버튼 클릭 시 사용자 개인 데이터프레임 및 추천된 레시피 데이터프레임 표시
    if st.button("추천 레시피 보기"):
        recipe_ids = get_recipe_ids()
        if recipe_ids:
            # 사용자 개인의 레시피 DataFrame을 가져와서 표시
            recommend_df = get_recommend_df()
            user_recipe_df = get_user_recipe_df(recommend_df, recipe_ids)
            st.subheader("사용자 개인의 레시피 데이터프레임:")
            if not user_recipe_df.empty:
                st.dataframe(user_recipe_df)  # 사용자 개인 레시피 데이터프레임을 표시
            else:
                st.write("사용자 개인의 레시피가 없습니다.")

            # 추천된 레시피 데이터프레임을 가져와서 표시
            recipe_re = user_recipe_recommend(recipe_ids)
            if not recipe_re.empty:
                st.subheader("추천된 레시피:")
                st.dataframe(recipe_re)  # 추천된 레시피 데이터프레임을 표시
            else:
                st.warning("추천할 레시피가 없습니다.")
        else:
            st.warning("추천할 레시피 ID가 없습니다.")

if __name__ == '__main__':
    recommend_page()