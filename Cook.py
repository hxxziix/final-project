import requests
from bs4 import BeautifulSoup
import streamlit as st

def get_valid_recipe_url(recipe_name):
    # 검색 페이지 URL
    search_url = f"https://www.10000recipe.com/recipe/list.html?q={recipe_name}"
    search_response = requests.get(search_url)
    search_soup = BeautifulSoup(search_response.content, 'html.parser')

    # 검색 결과에서 유효한 레시피 링크를 찾기
    for i in range(1, 11):  # 첫 10개의 검색 결과를 확인
        recipe_link = search_soup.select_one(f'#contents_area_full > ul > ul > li:nth-child({i}) > div.common_sp_thumb > a')
        if recipe_link and recipe_link.find('span'):
            recipe_url = "https://www.10000recipe.com" + recipe_link['href']
            return recipe_url
    return None

def get_recipe_info(recipe_url):
    recipe_response = requests.get(recipe_url)
    recipe_soup = BeautifulSoup(recipe_response.content, 'html.parser')

    # 요리 사진
    photo_url = recipe_soup.select_one('#main_thumbs')['src']

    # 재료
    ingredients = []
    ingredient_number = 2
    while True:
        ingredient_li = recipe_soup.select_one(f'#divConfirmedMaterialArea > ul > li:nth-child({ingredient_number})')
        if not ingredient_li:
            break
        ingredients.append(ingredient_li.get_text(strip=True))
        ingredient_number += 1
    ingredients_text = "\n".join(ingredients).replace("구매", "")

    # 요리 영상
    video_iframe = recipe_soup.select_one('#ifrmRecipeVideo')
    video_url = None
    if video_iframe:
        video_url = video_iframe.get('org_src')

    # 조리 순서
    steps = []
    step_number = 1
    while True:
        step_descr = recipe_soup.select_one(f'#stepdescr{step_number}')

        if not step_descr:
            break
        
        step_text = step_descr.get_text()

        p_tags = step_descr.select('p')
        if p_tags:
            sub_text = ""
            for p_tag in p_tags:
                p_text = p_tag.get_text()
                sub_text += ("\n" + p_text)

                parts = step_text.rsplit(p_text, 1)
                step_text = "".join(parts)
            step_text += ("\n" + sub_text)
        
        step_img = recipe_soup.select_one(f'#stepimg{step_number} > img')
        step_image_url = step_img['src'] if step_img else None

        steps.append({
            "text": step_text,
            "image_url": step_image_url
        })
        step_number += 1

    # 팁/주의사항
    tips = recipe_soup.select_one('#obx_recipe_step_start > dl > dd')
    tips_text = tips.get_text() if tips else "팁/주의사항이 없습니다."

    return {
        "photo_url": photo_url,
        "ingredients": ingredients_text,
        "video_url": video_url,
        "steps": steps,
        "tips": tips_text
    }

# ==================================================================================================================================

# 상태 변수 초기화
if 'selected_recipe' not in st.session_state:
    st.session_state.selected_recipe = None

# 검색 기능
st.title("요리 레시피 검색")
recipe_name = st.text_input("요리명을 입력하세요:")

# 빈 자리표시자 생성
status_placeholder = st.empty()

if st.button("검색"):
    if recipe_name:
        # "검색중입니다" 텍스트 표시
        status_placeholder.text("검색 중입니다...")

        recipe_url = get_valid_recipe_url(recipe_name)
        if recipe_url:
            recipe_info = get_recipe_info(recipe_url)
            st.session_state.selected_recipe = recipe_info
        else:
            st.text("유효한 요리 레시피를 찾을 수 없습니다.")
        
        # 검색 완료 후 텍스트 제거
        status_placeholder.empty()

# 검색 결과 표시
if st.session_state.selected_recipe:
    st.text("\n")
    st.text("\n")
    st.subheader("요리 정보")
    
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
