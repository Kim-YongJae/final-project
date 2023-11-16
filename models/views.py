from django.shortcuts import render

# Create your views here.
def M_index(request):
    return render(request, 'models/M_index.html')