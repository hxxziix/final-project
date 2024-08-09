def get_recommend_df():
    import re
    import pandas as pd

    # 레시피 가져오기
    recipe_df = pd.read_csv("C:/Users/ryun1/ds/food_recipe_pandas/kr_recipe.csv", encoding='UTF-8')

    # 레시피 한글로 변환
    recipe_df.rename(columns={'RCP_SNO': '레시피일련번호', 'RCP_TTL': '레시피제목', 'CKG_NM': '요리명',
                            'RGTR_ID': '등록자ID', 'RGTR_NM': '등록자명', 'INQ_CNT': '조회수',
                            'RCMM_CNT': '추천수', 'SRAP_CNT': '스크랩수', 'CKG_MTH_ACTO_NM': '요리타입',
                            'CKG_STA_ACTO_NM': '음식분위기', 'CKG_MTRL_ACTO_NM': '재료타입', 'CKG_KND_ACTO_NM': '음식타입',
                            'CKG_IPDC': '요리소개', 'CKG_MTRL_CN': '재료리스트', 'CKG_INBUN_NM': '몇인분',
                            'CKG_DODF_NM': '요리난이도', 'CKG_TIME_NM': '요리시간', 'FIRST_REG_DT': '최초등록일시'}, inplace=True)

    # 결측치 제거
    recipe_df.dropna(inplace=True)

    # ?? 견과류 부분 삭제
    recipe_df.drop(recipe_df[recipe_df['재료타입']=='??견과류'].index, inplace=True)

    # 차/?슘?술 부분 삭제
    recipe_df.drop(recipe_df[recipe_df['음식타입']=='차/?슘?술'].index, inplace=True)

    # 재료리스트 재료부분만 남기고 기타 문자 제거
    def remain_food_name(food):
        # food가 str 타입이 아니면 빈문자열 반환
        if not isinstance(food, str):
            return ""
        
        # 정규식 패턴
        pattern = r'\[\w+\]'

        # 정규식으로 '[한글]' 형식의 부분을 찾아 분리
        parts = re.split(pattern, food)
        
        # [한글] 형식 제외한 부분 저장
        parts = [part.strip() for part in parts]
        
        # '| ' 부분을 제거해서 재료들을 각각 result에 저장
        result = []
        for i in parts:
            result.extend(i.split('| '))
            
        return ', '.join(result[1:])

    recipe_df['재료리스트'] = recipe_df['재료리스트'].apply(remain_food_name)

    # 특징으로 사용할 열 선택
    select_columns = ['레시피일련번호', '조회수', '요리명', '요리타입', '음식분위기', '재료타입', '음식타입', '몇인분', '요리난이도', '요리시간','재료리스트']

    # 추천 데이터 프레임 만들기
    recommend_df = recipe_df[select_columns]
    
    return recommend_df