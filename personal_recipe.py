# recipe_list.py

# 레시피 ID 리스트
recipe_ids = []

def add_recipe_id(new_id):
    """레시피 ID 추가"""
    recipe_ids.append(new_id)

def get_recipe_ids():
    """현재 레시피 ID 리스트 반환"""
    return recipe_ids

def clear_recipe_ids():
    """레시피 ID 리스트 초기화"""
    recipe_ids.clear()