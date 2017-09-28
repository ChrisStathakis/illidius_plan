from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.template.context_processors import csrf
from .models import *
from .forms import *
# Create your views here.


def program(exercise):
    exercise = float(exercise)
    get_data = []
    first_set = [(exercise*0.65, '5'), (exercise*0.7, '3'), (exercise*0.75, '5'), (exercise*0.4, '5')]
    second_set = [(exercise*0.75, '5'), (exercise*0.8, '3'), (exercise*0.85, '3'),(exercise*0.5, '5'), ]
    third_set = [(exercise*0.85, '5+'), (exercise*0.9, '3+'), (exercise*0.95, '1+'),(exercise*0.6, '5')]
    get_data.append(first_set)
    get_data.append(second_set)
    get_data.append(third_set)
    return get_data


class GymPage(ListView):
    model = GymPerson
    template_name = 'gym/index.html'

    def get_context_data(self, **kwargs):
        context = super(GymPage, self).get_context_data(**kwargs)
        return context


def gym_person_page(request, dk):
    person = get_object_or_404(GymPerson, id=dk)
    if request.POST:
        form = GymPersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
    else:
        form = GymPersonForm(instance=person)
    deadlift = program(person.deadlift)
    squats = program(person.squats)
    shoulder_press = program(person.shoulder_press)
    bench_press = program(person.bench_press)
    context = locals()
    context.update(csrf(request))
    return render(request, 'gym/gym_person_page.html', context)