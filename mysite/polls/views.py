from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.http import Http404
from django.db.models import F


def index(request):
    # Obtiene las 5 preguntas más recientes ordenadas por fecha de publicación descendente
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    # Renderiza la plantilla 'index.html' con la lista de preguntas
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # Intenta obtener la pregunta según el ID, o lanza un error 404 si no existe
    question = get_object_or_404(Question, pk=question_id)
    # Renderiza la plantilla 'detail.html' con los datos de la pregunta
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    # Muestra un mensaje simple con el ID de la pregunta (esto se puede mejorar)
    response = "Estás viendo los resultados de la pregunta %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    # Intenta obtener la pregunta correspondiente al ID
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Intenta obtener la opción seleccionada usando el ID que viene del formulario POST
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Si no se seleccionó una opción o no existe, vuelve a mostrar el formulario con un mensaje de error
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "No seleccionaste una opción.",
            },
        )
    else:
        # Si se seleccionó correctamente, incrementa el contador de votos usando una expresión F (evita condiciones de carrera)
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Redirige al usuario a la página de resultados de la pregunta
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
