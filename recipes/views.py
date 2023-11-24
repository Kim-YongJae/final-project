from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from recipes.models import Recipe


# Create your views here.
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


# class RecipeReset(LoginRequiredMixin, View):
#     login_url = 'login'  # 로그인 페이지 URL 설정
#
#     def get(self, request):
#         return render(request, 'recipes/recipe_reset.html')
#
#     def post(self, request):
#         clear_password = 'qwer1234'
#         get_password = request.POST.get('clear_password')
#         if clear_password == get_password:
#             Recipe.objects.all().delete()        ### 기존 데이터 모두 삭제
#             with connection.cursor() as cursor:
#                 cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'recipes_recipe'")
#
#             try:
#                 sql_file_path = 'base/recipe_data_insert.sql'  # SQL 파일 경로 설정
#                 with open(sql_file_path, 'r', encoding='utf-8') as f:
#                     sql_queries = f.read()
#
#                 with connection.cursor() as cursor:  ## 데이터 베이스에 저장
#                     cursor.execute(sql_queries)
#             except Exception as e:
#                 print(e)
#
#             return redirect('recipe_list')  # Redirect to the desired URL
#         else:
#             return get_system_message_render(request, "비밀번호 오류 ", 'recipes')
#
#
# def get_system_message_render(request, error_message, set_urls):
#     context = {'system_message': error_message, 'set_urls': set_urls}
#     return render(request, 'system_message.html', context)
#
#
# '''1. 육수는 무 넙적하게 썰어주고, 다시마 4~5장, 무가 잠길정도의 물로 끓여줍니다. 끓기시작하면 다시마는 빼주세요.
# 2. 남대문표양념장 : 간장8, 설탕1, 물엿1, 고추가루3, 다진마늘1, 다진생강 약간, 여기에 맛술2, 후추조금 더 추가했네요.
# 3. 갈치는 내장과 비늘을 깨끗하게 손질하여 물기를 빼줍니다~생선비린내는 물에 깨끗하게 씻어야 없어집니다
# 4. 끓어오른 육수에 바로 갈치올리고, 양념장 두둑하게 올려줍니다.
# 5. 양파,청양고추,대파까지 올리고, 뚜껑닫고 한소끔 끓입니다.
# 6. 중간에 갈치위로 양념국물 덮어줘가며 끓이면 완성^^'''