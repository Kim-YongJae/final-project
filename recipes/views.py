from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from recipes.models import Recipe

import json

# Create your views here.
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import torch
import ast

Ingredient_List = ['마늘', '대파', '양파', '고추', '당근', '김치', '통깨', '계란', '감자', '두부', '무',
                   '콩나물', '애호박', '생강', '멸치', '깻잎', '양배추', '부추','다시마', '어묵',
                   '소면', '당면', '떡', '배추', '고구마줄기', '오이', '우유', '미역', '숙주', '김',
                   '단무지', '맛살', '피망', '견과류', '순두부', '염장 미역줄기', '연근', '시금치',
                   '사과', '새우', '고사리', '황태채', '치즈', '열무', '호박', '만두', '순대', '데친 얼갈이배추',
                   '파래', '식빵', '닭고기', '돼지고기', '돼지고기 목살', '대패삼겹살', '삼겹살', '소불고기',
                   '소고기', '비엔나', '스팸', '햄', '소시지', '갈치', '참치', '수육용 삼겹살', '불고기감 소고기',
                   '감자탕용 돼지등뼈', '오징어', '고등어', '꽃게', '느타리 버섯', '펭이버섯', '표고버섯',' 목이버섯',
                   '가지', '카레가루', '파프리카', '쪽파', '월계수 잎', '진미채', '메추리알', '고구마', '순두부',
                   '오미자(매실)청', '도토리묵', '상추','디포리']



Ingredient_List = ['마늘', '대파', '양파', '고추', '당근', '김치', '통깨', '계란', '감자', '두부', '무',
                   '콩나물', '애호박', '생강', '멸치', '깻잎', '양배추', '부추','다시마', '어묵',
                   '소면', '당면', '떡', '배추', '고구마줄기', '오이', '우유', '미역', '숙주', '김',
                   '단무지', '맛살', '피망', '견과류', '순두부', '염장 미역줄기', '연근', '시금치',
                   '사과', '새우', '고사리', '황태채', '치즈', '열무', '호박', '만두', '순대', '데친 얼갈이배추',
                   '파래', '식빵', '닭고기', '돼지고기', '돼지고기 목살', '대패삼겹살', '삼겹살', '소불고기',
                   '소고기', '비엔나', '스팸', '햄', '소시지', '갈치', '참치', '수육용 삼겹살', '불고기감 소고기',
                   '감자탕용 돼지등뼈', '오징어', '고등어', '꽃게', '느타리 버섯', '펭이버섯', '표고버섯',' 목이버섯','',
                   '가지', '카레가루', '파프리카', '쪽파', '월계수 잎', '진미채', '메추리알', '고구마', '순두부',
                   '오미자(매실)청', '도토리묵', '상추','디포리']



def detect_ingredients(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']

            # 저장된 이미지 경로
            img_path = f'media/{uploaded_image.name}'

            # 이미지 저장
            with open(img_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            uploaded_image_url = f'/media/{uploaded_image.name}'

            # YOLOv5 모델 불러오기

            model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/chqh1/Desktop/yolov5x 2차 결과/yolov5x 2차 결과/best.pt')

            # 이미지 불러오기 및 객체 탐지 수행
            img = Image.open(img_path)
            results = model(img)

            # 탐지된 객체 정보
            if len(results.pred) > 0:
                predictions = results.pred[0]
                classes = predictions[:, -1].cpu().numpy().astype(int)
                classes = list(set(classes))

                class_names = ['garlic', 'welsh_Onion', 'onion', 'chili_Pepper', 'carrot', 'kimchi', 'Egg', 'potato', 'TOFU', 'radish']  # 클래스에 맞게 변경
                class_names_korean = ['마늘', '대파', '양파', '고추', '당근', '김치', '계란', '감자', '두부', '무']

                detected_classes = [class_names[class_idx] for class_idx in classes]
                detected_classes_korean = [class_names_korean[class_names.index(detected)] for detected in
                                           detected_classes]

                # Recommendation algorithm
                recommended_recipes = recommend_recipes(classes)

                unique_detected_classes = list(detected_classes_korean)

            else:
                detected_classes = []  # 또는 예외 처리에 맞게 적절한 처리를 수행하세요


            return render(request, 'recipes/recommend_recipe.html', {'form': form, 'detected_classes': unique_detected_classes, 'recommended_recipes': recommended_recipes, 'uploaded_image_url': uploaded_image_url})

    else:
        form = ImageUploadForm()
    return render(request, 'recipes/recommend_recipe.html', {'form': form})

class RecipeList(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by('id')    # 모든 Recipe 객체를 가져와서 ID 기준으로 오름차순 정렬
        paginator = Paginator(recipes, 10)      # Paginator를 사용하여 10개씩 페이지로 나눔
        page_number = request.GET.get("page")           # URL에서 'page' 매개변수를 가져와서 현재 페이지 번호를 설정
        recipe_list = paginator.get_page(page_number)    # 현재 페이지의 Recipe 객체들을 가져옴
        context = {'recipe_list': recipe_list}             # templet에 넣을 데이터 설정
        return render(request, 'recipes/recipes_list.html', context) # 렌더링

class RecipeDetail(View):
    def upload_image(self, request):
        recipe_photo = Recipe.objects.all()
        return render(request, 'recipes/recipe_detail.html',{'recipe_photo': recipe_photo})
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)  # 주어진 recipe_id에 해당하는 Recipe 객체를 가져오거나, 객체가 없으면 404 에러를 나타냄
        context = {'recipe': recipe}
        return render(request, 'recipes/recipe_detail.html', context)

def recommend_recipes(classes):

    # 레시피 모델에서 원하는 데이터 가져오기
    recipes = Recipe.objects.all()
    # 결과를 저장할 빈 리스트
    model_label = []
    recommended_recipes = []
    # 리스트를 순회하면서 조건을 확인하고 결과를 저장
    for number in classes:
        if number >= 6:
            model_label.append(number + 1)
        else:
            model_label.append(number)

    for recipe in recipes:
        label = recipe.label

        requirement = []

        count = 0
        for model_idx in model_label:
            if model_idx in label:
                count += 1

        for i in label:
            if i not in model_label:
                requirement.append(Ingredient_List[i])
        if count >= len(label) * 0.5:
            recommended_recipes.append({
            'id': recipe.id,
            'food_name': recipe.food_name,
            'requirement': requirement,
            'count_ratio': count / len(label)
            # 필요한 경우 다른 속성도 추가가능
        })

    recommended_recipes.sort(key=lambda x: x['count_ratio'], reverse=True)

    return recommended_recipes