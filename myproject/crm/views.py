from django.shortcuts import redirect, render

from .forms import PersonForm0, PersonForm1, PersonForm
from .models import Person


def person_list(request):
    template_name = 'crm/person_list.html'
    object_list = Person.objects.all()
    context = {'object_list': object_list}
    return render(request, template_name, context)


def person_detail(request, pk):
    template_name = 'crm/person_detail.html'
    obj = Person.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


# def person_create(request):
#     template_name = 'crm/person_form0.html'

#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')

#         Person.objects.create(first_name=first_name, last_name=last_name)

#         return redirect('crm:person_list')

#     return render(request, template_name)


# def person_create(request):
#     template_name = 'crm/person_form0.html'
#     form = PersonForm0(request.POST or None)

#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('crm:person_list')
#         else:
#             print(form.errors)

#     context = {'form': form}
#     return render(request, template_name, context)


# def person_create(request):
#     template_name = 'crm/person_form1.html'
#     form = PersonForm1(request.POST or None)

#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('crm:person_list')

#     context = {'form': form}
#     return render(request, template_name, context)


def person_create(request):
    template_name = 'crm/person_form.html'
    form = PersonForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('crm:person_list')

    context = {'form': form}
    return render(request, template_name, context)
