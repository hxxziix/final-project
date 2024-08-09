import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
from make_recommend_df import *

# pip install scikit-learn
# pip install numpy

def user_recipe_recommend(user_recipe_number):
    # 유저 레시피에 중복있으면 중복제거
    user_recipe_number = list(set(user_recipe_number))
    
    # 레시피 데이터 가져오기
    recommend_df = get_recommend_df()

    # 텍스트 벡터화
    text_vectorizer = CountVectorizer()

    # 범주형 인코딩
    categorical_encoder = OneHotEncoder(handle_unknown='ignore') # 존재하지 않는 새로운 범주가 데이터에 나타나면 새로운 범주는 무시

    # ColumnTransformer를 사용하여 텍스트와 범주형 변수 처리
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', text_vectorizer, '재료리스트'),
            ('cat', categorical_encoder, ['요리타입', '음식분위기', '재료타입', '음식타입', '몇인분', '요리난이도', '요리시간'])
        ]
    )

    # 데이터 전처리 및 벡터화
    X = preprocessor.fit_transform(recommend_df)

    # 사용자가 사용한 적 있던 레시피를 따로 DataFrame으로 변환
    user_recipe_df = recommend_df[recommend_df['레시피일련번호'].isin(user_recipe_number)]

    # 예외 처리: 해당하는 레시피가 없다면 조회수 높은 상위 5개 레시피 반환
    if user_recipe_df.empty:
        print("해당하는 레시피 번호가 없습니다. 조회수 높은 레시피를 추천합니다.")
        top_viewed_recipes = recommend_df.sort_values(by='조회수', ascending=False).head(5)
        return top_viewed_recipes
    
    # 사용자 레시피 벡터화
    user_recipe_vec = preprocessor.transform(user_recipe_df)

    # 사용자 레시피와 모든 레시피 간의 유사도 계산
    similarity_scores = cosine_similarity(user_recipe_vec, X)

    # 평균 유사도 점수 계산 (각  레시피의 유사도 점수 평균)
    avg_similarity_scores = np.mean(similarity_scores, axis=0)

    # 유사도에 따라 레시피 추천 (자기 자신 제외)
    # user_recipe_df의 인덱스를 제외하기 위해 길이+5 (인덱스 조정)
    avg_result = avg_similarity_scores.argsort()[::-1][len(user_recipe_number):len(user_recipe_number)+5]  # 유사도가 높은 상위 5개 레시피 추천

    recommended_recipes = recommend_df.iloc[avg_result]

    # 추천된 레시피 
    return recommended_recipes

print(user_recipe_recommend([1]))