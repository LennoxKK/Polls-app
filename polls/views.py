from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.utils import timezone

# Create your views here.
from .models import Question,Choice
from django.db.models import F



class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
#Vote view
def vote(request,question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question,pk=question_id)
        try:
            selected_choice = question.choice_set.get(id=request.POST['choice'])
            selected_choice.votes=F('votes')+1
            selected_choice.save()
            context = {
                'selected_choice':selected_choice,
                'question':question,
            }
        except (KeyError,Choice.DoesNotExist):
            context = {
                'error_message' : "No choice selected",
                'question':question,
                'selected_choice':selected_choice

            }
    return render(request,"polls/vote.html",context)