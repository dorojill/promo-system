from django.shortcuts import render


def calculator_view(request):
    return render(request, 'calculator.html')