import json

# 원본파일 로드
with open('translation_names.json', 'r', encoding='utf-8') as json_file:
    translation_names = json.load(json_file)

# 키와 값을 서로 바꾸기
translation_names_swap = {value: key for key, value in translation_names.items()}

# 변경한 딕셔너리를 JSON 파일로 저장
with open('translation_names_swap.json', 'w', encoding='utf-8') as file:
    json.dump(translation_names_swap, file, ensure_ascii=False, indent=4)