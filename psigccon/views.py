from django.shortcuts import render

# Create your views here.


def vista_conocim(request):
    return render(request, "psigccon/basesdatos.html")

def vista_mapindicad(request):
    return render(request, "psigccon/mapindicad.html")

def vista_mapindice(request):
    return render(request, "psigccon/mapindicad.html")

