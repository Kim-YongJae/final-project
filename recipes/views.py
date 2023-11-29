from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from recipes.models import Recipe


# Create your views here.
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import torch

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

            # YOLOv5 모델 불러오기
            model = torch.hub.load('ultralytics/yolov5', 'custom', path='model_path')

            # 이미지 불러오기 및 객체 탐지 수행
            img = Image.open(img_path)
            results = model(img)

            # 탐지된 객체 정보
            if len(results.pred) > 0:
                predictions = results.pred[0]
                classes = predictions[:, -1].cpu().numpy().astype(int)

                class_names = ['garlic', 'welsh_Onion', 'onion', 'chili_Pepper', 'carrot', 'kimchi', 'Egg', 'potato', 'TOFU', 'radish']  # 클래스에 맞게 변경
                detected_classes = [class_names[class_idx] for class_idx in classes]

                unique_detected_classes = list(set(detected_classes))
            else:
                unique_detected_classes = []  # 또는 예외 처리에 맞게 적절한 처리를 수행하세요

            return render(request, 'recipes/recommend_recipe.html', {'form': form, 'detected_classes': unique_detected_classes})
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
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)  # 주어진 recipe_id에 해당하는 Recipe 객체를 가져오거나, 객체가 없으면 404 에러를 나타냄
        context = {'recipe': recipe}
        return render(request, 'recipes/recipe_detail.html', context)