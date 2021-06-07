from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from .forms import (
    ContactForm,
    PersonForm,
    PersonForm0,
    PersonForm1,
    PersonPhotoForm
)
from .models import Person, Photo


def person_list(request):
    template_name = 'crm/person_list.html'
    object_list = Person.objects.all()
    form = PersonForm1
    context = {'object_list': object_list, 'form': form}
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


def person_update(request, pk):
    template_name = 'crm/person_form.html'
    instance = Person.objects.get(pk=pk)
    form = PersonForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('crm:person_list')

    context = {'form': form}
    return render(request, template_name, context)


def send_contact(request):
    template_name = 'crm/contact_form.html'
    form = ContactForm(request.POST or None)

    if request.method == 'POST':
        data = request.POST
        subject = data.get('subject')
        message = data.get('message')
        sender = data.get('sender')

        if form.is_valid():
            send_mail(
                subject,
                message,
                sender,
                ['localhost'],
                fail_silently=False,
            )
            return redirect('core:index')

    context = {'form': form}
    return render(request, template_name, context)


class PersonBootstrapCreate(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'crm/person_bootstrap_form.html'


class PersonCrispyCreate(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'crm/person_crispy_form.html'


# def photo_create(request):
#     template_name = 'crm/person_photo_form.html'
#     form = PersonPhotoForm(request.POST or None)

#     if request.method == 'POST':
#         photo = request.FILES.get('photo')

#         if form.is_valid():
#             person = form.save()
#             Photo.objects.create(person=person, photo=photo)
#             return redirect('crm:person_detail', person.pk)

#     context = {'form': form}
#     return render(request, template_name, context)


def photo_create(request):
    template_name = 'crm/person_photo_form.html'
    form = PersonPhotoForm(request.POST or None)

    if request.method == 'POST':
        photos = request.FILES.getlist('photo')

        if form.is_valid():
            person = form.save()

            for photo in photos:
                Photo.objects.create(person=person, photo=photo)

            return redirect('crm:person_detail', person.pk)

    context = {'form': form}
    return render(request, template_name, context)


def person_create_ajax(request):
    form = PersonForm1(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()
            data = [person.to_dict()]
            return JsonResponse({'data': data})


def person_vuejs_list(request):
    # Renderiza a página
    template_name = 'crm/person_vuejs_list.html'
    return render(request, template_name)


def person_json(request):
    # Retorna os dados
    persons = Person.objects.all()
    data = [person.to_dict() for person in persons]
    return JsonResponse({'data': data})


def person_vuejs_create(request):
    # Salva os dados
    form = PersonForm1(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()
            data = person.to_dict()
            return JsonResponse({'data': data})
