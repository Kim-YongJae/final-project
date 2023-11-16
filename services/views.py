from django.shortcuts import render

# Create your views here.
def S_index(request):
    return render(request, 'services/S_index.html')