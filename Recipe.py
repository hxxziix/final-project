import pandas as pd

recipe_df = pd.read_csv("C:/Users/Seunghwan/Desktop/데이터/kr_recipe.csv")

recipe_df.rename(columns={'RCP_SNO': '레시피일련번호', 'RCP_TTL': '레시피제목', 'CKG_NM': '요리명',
                          'RGTR_ID': '등록자ID', 'RGTR_NM': '등록자명', 'INQ_CNT': '조회수',
                          'RCMM_CNT': '추천수', 'SRAP_CNT': '스크랩수', 'CKG_MTH_ACTO_NM': '요리타입',
                          'CKG_STA_ACTO_NM': '음식분위기', 'CKG_MTRL_ACTO_NM': '재료타입', 'CKG_KND_ACTO_NM': '음식타입',
                          'CKG_IPDC': '요리소개', 'CKG_MTRL_CN': '재료리스트', 'CKG_INBUN_NM': '몇인분',
                          'CKG_DODF_NM': '요리난이도', 'CKG_TIME_NM': '요리시간', 'FIRST_REG_DT': '최초등록일시'}, inplace=True)

# 재료가 하나 이상 포함된 행들 반환하는 함수
def search_include_at_least_one(detected_ingredient):
    # 재료 열에서 각 값을 람다함수 적용, 값은 x에 해당됨, any(): 위에서 인식된 재료 리스트중 하나라도 x에 포함되어있으면 true 반환
    search_results = recipe_df[recipe_df['재료리스트'].apply(lambda x: any(ingredient in str(x) for ingredient in detected_ingredient))]
    return search_results

# 재료가 모두 포함된 행들 반환하는 함수
def search_all_include(detected_ingredient):
    # 모든 재료를 포함하는 행 필터링, all(): 위에서 인식된 재료 리스트 전부가 x에 포함되어있으면 true 반환
    search_results = recipe_df[recipe_df['재료리스트'].apply(lambda x: all(ingredient in str(x) for ingredient in detected_ingredient))]
    return search_results

# 랜덤 추천
def random_recipe(random):
    search_results = recipe_df.iloc[random]
    return search_results