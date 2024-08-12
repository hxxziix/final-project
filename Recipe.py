import pandas as pd
import random

recipe_df = pd.read_csv("C:/Users/hj/Desktop/FINAL/YHJ/final-project/preprocessed_kr_recipe.csv")
recipe_df = recipe_df[['레시피일련번호', '요리명', '조회수', '추천수', '스크랩수',
                       '재료리스트', '요리타입', '음식분위기', '재료타입', '음식타입',
                       '몇인분', '요리난이도', '요리시간']]

# 재료가 하나 이상 포함된 행들 반환하는 함수
def search_include_at_least_one(detected_ingredients):
    # '재료리스트' 열에서 각 값을 람다함수 적용, 값은 x에 해당됨, any(): 위에서 인식된 재료 리스트중 하나라도 x에 포함되어있으면 true 반환
    search_results = recipe_df[recipe_df['재료리스트'].apply(lambda x: any(ingredient in x for ingredient in detected_ingredients))]
    return search_results

# 재료가 모두 포함된 행들 반환하는 함수
def search_all_include(detected_ingredients):
    # 모든 재료를 포함하는 행 필터링, all(): 위에서 인식된 재료 리스트 전부가 x에 포함되어있으면 true 반환
    search_results = recipe_df[recipe_df['재료리스트'].apply(lambda x: all(ingredient in x for ingredient in detected_ingredients))]
    return search_results

# 랜덤 추천
def random_recipe():
    # recipe_df의 행 수를 사용하여 랜덤 숫자 생성
    random_number = random.randint(0, recipe_df.shape[0] - 1) # 0부터 (행 수 - 1)까지의 숫자 생성
    search_results = recipe_df.iloc[random_number]
    return search_results