import streamlit as st

# 웹사이트 접속 명령어
# streamlit run streamlit/app.py

# 웹사이트 타이틀 설정
st.set_page_config(
    page_title="포켓몬 도감",
    page_icon='streamlit/images/monsterball.png')

st.title("Streamlit 포켓몬 도감") # 텍스트 크게 나옴(제목용)
# st.write('hello streamlit!') # 텍스트 작게 나옴

# st.text("포켓몬을 하나씩 추가해서 도감을 채워보세요!")
# st.subheader("포켓몬을 하나씩 추가해서 도감을 채워보세요!") # 소제목용
st.markdown("**포켓몬**을 하나씩 추가해서 도감을 채워보세요!") # 마크다운 형식으로 작성해주는 함수

type_emoji_dict = {
    "노말": "⚪",
    "격투": "✊",
    "비행": "🕊",
    "독": "☠️",
    "땅": "🌋",
    "바위": "🪨",
    "벌레": "🐛",
    "고스트": "👻",
    "강철": "🤖",
    "불꽃": "🔥",
    "물": "💧",
    "풀": "🍃",
    "전기": "⚡",
    "에스퍼": "🔮",
    "얼음": "❄️",
    "드래곤": "🐲",
    "악": "😈",
    "페어리": "🧚"
}

pokemons = [
    {
        "name": "피카츄",
        "types": ["전기"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/pikachu.webp"
    },
    {
        "name": "누오",
        "types": ["물", "땅"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/nuo.webp",
    },
    {
        "name": "갸라도스",
        "types": ["물", "비행"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/garados.webp",
    },
    {
        "name": "개굴닌자",
        "types": ["물", "악"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/frogninja.webp"
    },
    {
        "name": "루카리오",
        "types": ["격투", "강철"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/lukario.webp"
    },
    {
        "name": "에이스번",
        "types": ["불꽃"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/acebun.webp"
    },
]

for i in range(0, len(pokemons), 3):
    row_pokemons = pokemons[i:i+3]
    cols = st.columns(3) # 컬럼 3개
    for j in range(len(row_pokemons)):
        with cols[j]:
            pokemon = row_pokemons[j]
            with st.expander(label=f"**{i+j+1}. {pokemon['name']}**", expanded=True): # expanded=True: 기본적으로 펼쳐지도록 하는 옵션
                st.image(pokemon['image_url'])
                emoji_types = [f"{type_emoji_dict[t]} {t}" for t in pokemon['types']]
                st.subheader(" / ".join(emoji_types))