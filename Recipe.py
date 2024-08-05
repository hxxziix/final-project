import pandas as pd

recipe_df = pd.read_csv("C:/Users/Seunghwan/Desktop/데이터/kr_recipe.csv")
# recipe_df = pd.read_csv("kr_recipe.csv")

# 재료가 하나 이상 포함된 행들 반환하는 함수
def search_include_at_least_one(detected_ingredient):
    # 재료 열에서 각 값을 람다함수 적용, 값은 x에 해당됨, any(): 위에서 인식된 재료 리스트중 하나라도 x에 포함되어있으면 true 반환
    search_results = recipe_df[recipe_df['추출된명사'].apply(lambda x: any(ingredient in x for ingredient in detected_ingredient))]
    return search_results

# 재료가 모두 포함된 행들 반환하는 함수
def search_all_include(detected_ingredient):
    # 모든 재료를 포함하는 행 필터링, all(): 위에서 인식된 재료 리스트 전부가 x에 포함되어있으면 true 반환
    search_results = recipe_df[recipe_df['추출된명사'].apply(lambda x: all(ingredient in x for ingredient in detected_ingredient))]
    return search_results

# 랜덤 추천
def random_recipe(random):
    search_results = recipe_df.iloc[random]
    return search_results