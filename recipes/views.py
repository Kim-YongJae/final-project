from django.shortcuts import render

# Create your views here.
def R_index(request):
    return render(request, 'recipes/R_index.html')