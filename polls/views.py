from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# Create your views here.

# index view without using generic views
'''
def index(request):
    #simplest

    return HttpResponse("Hello, world. You're at the polls index.")
    
    
    
    #read records from database

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
 
    
    
    #read records from a database AND render using template

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
   
    
    
    #using shortcut: render()

    The render() function takes the request object as its first argument,
    a template name as its second argument
    and a dictionary as its optional third argument.
    It returns an HttpResponse object of the given template rendered with the given context.

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
'''


#Index view using generic views
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


# detail view without using generic views
'''
def detail(request, question_id):
    #simple. uses template variable
    #return HttpResponse("You're looking at question %s." % question_id)
    
    
    #raise 404 if the requested ID does not exist
   
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

    
    
    #using shortcut: get_object_or_404()
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
'''

#Detail view using generic views
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


# results view without using generic views
'''
def results(request, question_id):
    # simplest output 
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)

    # view for the results page of a particular question
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''
    
#Results view using generic views
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    #simplest output
    #return HttpResponse("You're voting on question %s." % question_id)

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))