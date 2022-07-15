from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("estas en la pagina principal de premios Platzi")

def detail(request, question_id):
    return HttpResponse(f"estás viendo la pregunta número {question_id}")

def results(request, question_id):
    return HttpResponse(f"estas iendo los resultados de la pregunta numero {question_id}")

def vote(request, question_id):
    return HttpResponse(f"Estas votando a la pregunta número {question_id}")

