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