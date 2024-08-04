import pandas as pd
import re
from konlpy.tag import Okt
from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine

recipe_df = pd.read_csv("C:/Users/Seunghwan/Desktop/데이터/kr_recipe.csv")

# 전처리(전처리가 완료된 데이터프레임을 read_to_csv() 하고 위에서 다시 로드해야한다. 이후 아래 전처리 코드는 지운다.)

# 열 이름 변경
recipe_df.rename(columns={'RCP_SNO': '레시피일련번호', 'RCP_TTL': '레시피제목', 'CKG_NM': '요리명',
                          'RGTR_ID': '등록자ID', 'RGTR_NM': '등록자명', 'INQ_CNT': '조회수',
                          'RCMM_CNT': '추천수', 'SRAP_CNT': '스크랩수', 'CKG_MTH_ACTO_NM': '요리타입',
                          'CKG_STA_ACTO_NM': '음식분위기', 'CKG_MTRL_ACTO_NM': '재료타입', 'CKG_KND_ACTO_NM': '음식타입',
                          'CKG_IPDC': '요리소개', 'CKG_MTRL_CN': '재료리스트', 'CKG_INBUN_NM': '몇인분',
                          'CKG_DODF_NM': '요리난이도', 'CKG_TIME_NM': '요리시간', 'FIRST_REG_DT': '최초등록일시'}, inplace=True)

recipe_df = recipe_df.drop(columns=['레시피일련번호', '레시피제목', '등록자ID', '등록자명', '요리소개', '최초등록일시']) # 이 열들 제거

recipe_df = recipe_df.dropna(subset=['재료리스트', '요리명']) # 이 열들에서 결측치 제거

# 데이터 수정할 열 이름
modify_col_data = ['추천수', '스크랩수']

# 각 열에 대해 처리 수행
for col in modify_col_data:
    
    # 숫자로 변환할 수 없는 값 NaN으로 변경
    recipe_df[col] = pd.to_numeric(recipe_df[col], errors='coerce')
    
    # NaN => 0
    recipe_df[col].fillna(0, inplace=True)
    
    # object => int64
    recipe_df[col] = recipe_df[col].astype('int64')

def extraction_of_nouns(sentence):
    # 패턴
    pattern = r'\[\w+\]' # ex) [재료], [양념]

    # 패턴으로 분리
    parts = re.split(pattern, sentence)

    # 각 파트에서 양쪽 여백 제거, 비어있지 않은 리스트만 추출
    parts = [list(map(lambda x: x.strip(), part.split("|"))) for part in parts if part]

    # 2차원 리스트 평탄화
    flattend_parts = [item for part in parts for item in part]

    # Okt 형태소 분석기 로드
    okt = Okt()

    # 명사 추출
    result = []
    for part in flattend_parts:
        nouns = okt.nouns(part)
        # print(f"문장: '{part}' -> 명사: {nouns}")
        result.extend(nouns)
    
    return result

recipe_df['추출된명사'] = recipe_df['재료리스트'].apply(extraction_of_nouns)

# ===========================================================================================================================================

# 기능

# BERT 모델과 토크나이저 로드
model_name = 'bert-base-multilingual-cased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# 입력 문장 토크나이징 및 텐서 변환
def get_word_embedding(word):
    inputs = tokenizer(word, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    # [CLS] 토큰의 임베딩을 사용
    embedding = outputs.last_hidden_state[:, 0, :].squeeze()
    return embedding

def cosine_similarity():
    # ! 아래 실행문은 예시이며 '추출된명사' 열의 각 명사 리스트와 탐지된 식재료 리스트 간 유사도를 계산하는 코드를 작성해야한다.
    # 단어 임베딩 계산
    word1 = "후추"
    word2 = "후춧가루"
    embedding1 = get_word_embedding(word1)
    embedding2 = get_word_embedding(word2)

    # 코사인 유사도 계산
    similarity = 1 - cosine(embedding1.numpy(), embedding2.numpy())
    print(f"'{word1}' 와(과) '{word2}' 의 유사도 = {similarity}")

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