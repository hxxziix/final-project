# 스크래핑한 주소
https://www.10000recipe.com/


## 태그

- **검색창**:
  
  #srhRecipeText

- **검색결과(요리영상이 포함된것만)**:

  #contents_area_full > ul > ul > li:nth-child({i}) > div.common_sp_thumb > a > span

- **요리영상이 포함된것이 없는 경우:**:
  #contents_area_full > ul > ul > li:nth-child({i}) > div.common_sp_thumb > a > img

- **요리된 사진**:
  
  #main_thumbs

- **재료**:
  
  #divConfirmedMaterialArea > ul > li:nth-child({i+2})

- **요리영상**:
  
  #ifrmRecipeVideo

- **조리순서**:
  
  #stepdescr{i}
  
  #stepimg1 > img

- **팁/주의사항**:
  
  #obx_recipe_step_start > dl > dd