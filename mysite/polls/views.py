from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


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
