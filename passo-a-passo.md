# Passo a passo

# django-forms-tutorial

![1400605](img/1400605.jpg)


## Criando projeto com boilerplate

```
git clone https://github.com/rg3915/django-boilerplate.git /tmp/django-boilerplate
cp /tmp/django-boilerplate/boilerplatesimple.sh .
source boilerplatesimple.sh
```


## Como o Django funciona?

![mtv1](img/mtv1.png)

---

![mtv3](img/mtv3.png)

---

### 1 - Admin - Login

![login.png](img/login.png)

```html
<form id="login-form" action="/admin/login/?next=/admin/" method="post">
  <input type="hidden" name="csrfmiddlewaretoken" value="n1RnvKj9peZB0XwpAFmuWjKHwotjBTjXEQMtSz1vYD6Vl8SUjpXG8s5YMHnkUZkq">
  <div class="form-row">

    <label class="required" for="id_username">Usuário:</label>
    <input id="id_username" type="text" name="username" autofocus="" autocapitalize="none" autocomplete="username" maxlength="150" required="">
  </div>
  <div class="form-row">

    <label class="required" for="id_password">Senha:</label>
    <input id="id_password" type="password" name="password" autocomplete="current-password" required="">
    <input type="hidden" name="next" value="/admin/">
  </div>

  <div class="submit-row">
    <input type="submit" value="Acessar">
  </div>
</form>
```

https://github.com/django/django/blob/master/django/contrib/admin/templates/admin/login.html#L44-L63

---

### 2 - [Building a form](https://docs.djangoproject.com/en/3.2/topics/forms/#building-a-form)

https://docs.djangoproject.com/en/3.2/topics/forms/#building-a-form

```html
<form action="." method="POST">
    <label for="first_name">Name: *</label>
    <input id="first_name" type="text" name="first_name" value="{{ current_first_name }}">
    <input type="submit" value="OK">
</form>
```

No nosso projeto:

Edite `crm/urls.py`

```python
urlpatterns = [
    path('', v.person_list, name='person_list'),
    path('<int:pk>/', v.person_detail, name='person_detail'),
    path('create/', v.person_create, name='person_create'),
]
```

Edite `crm/views.py`

```python
from django.shortcuts import redirect, render

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


def person_create(request):
    template_name = 'crm/person_form0.html'
    # import ipdb; ipdb.set_trace()
    return render(request, template_name)
```

```html
<!-- person_form0.html -->
{% extends "base.html" %}

{% block content %}
  <h1>Formulário</h1>
  <div class="cols-6">
    <form action="." method="POST">
      <div class="col-sm-6">
        <div>
          <label for="id_first_name">Nome</label>
          <input id="id_first_name" type="text" name="first_name">
        </div>

        <div>
          <label for="id_last_name">Sobrenome</label>
          <input id="id_last_name" type="text" name="last_name">
        </div>

        <div>
          <button type="submit">Salvar</button>
        </div>
      </div>
    </form>
  </div>
{% endblock content %}
```

Complemente o HTML com as classes.

```html
<!-- person_form0.html -->
{% extends "base.html" %}

{% block css %}
  <style>
    .required:after {
      content: "*";
      color: red;
    }
  </style>
{% endblock css %}

{% block content %}
  <h1>Formulário</h1>
  <div class="cols-6">
    <form class="form-horizontal" action="." method="POST">
      <div class="col-sm-6">
        <div class="form-group">
          <label for="id_first_name" class="required">Nome</label>
          <input id="id_first_name" type="text" name="first_name" class="form-control">
        </div>

        <div class="form-group">
          <label for="id_last_name">Sobrenome</label>
          <input id="id_last_name" type="text" name="last_name" class="form-control">
        </div>

        <div class="form-group">
          <button type="submit" class="btn btn-primary">Salvar</button>
        </div>
      </div>
    </form>
  </div>
{% endblock content %}
```

Em `crm/views.py`

Rodando a aplicação com ipdb, vemos que precisamos do

```html
{% csrf_token %}
```

E continuando o debug, precisamos separar GET de POST.

```python
def person_create(request):
    template_name = 'crm/person_form0.html'
    if request.method == 'GET':
        print('GET')
    else:
        print('POST')
    return render(request, template_name)
```

E depois pegamos os valores dos inputs com

```python
...
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    print(first_name, last_name)
```

Então podemos salvar os dados da seguinte forma:

```python
def person_create(request):
    template_name = 'crm/person_form0.html'
    if request.method == 'GET':
        print('GET')
    else:
        print('POST')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        print(first_name, last_name)

        Person.objects.create(first_name=first_name, last_name=last_name)

    return render(request, template_name)
```

Refatorando o código

```python
def person_create(request):
    template_name = 'crm/person_form0.html'

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        Person.objects.create(first_name=first_name, last_name=last_name)

        return redirect('crm:person_list')

    return render(request, template_name)
```

Edite `crm/forms.py`

```python
class PersonForm0(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Person
        fields = ('first_name', 'last_name')
```

Edite `crm/views.py`

```python
from .forms import PersonForm0

def person_create(request):
    template_name = 'crm/person_form0.html'
    form = PersonForm0(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('crm:person_list')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, template_name, context)
```

Acrescente valores inválidos, como `first_name` vazio ou texto muito longo.

```html
...
.errorlist {
  list-style: none;
  color: red;
}
...
{{ form.first_name.errors }}
...
{{ form.last_name.errors }}
...
```

### form 1

Agora vamos renderizar todos os campos do formulário na mão.

https://docs.djangoproject.com/en/3.2/topics/forms/#rendering-fields-manually

Edite `crm/views.py`

```python
def person_create(request):
    template_name = 'crm/person_form1.html'
    form = PersonForm0(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('crm:person_list')

    context = {'form': form}
    return render(request, template_name, context)
```

```html
...
<div class="form-group">
  <!-- <label for="{{ form.first_name.id_for_label }}" class="required">Nome</label> -->
  {{ form.first_name.label_tag }}
  {{ form.first_name }}
  {{ form.first_name.errors }}
</div>

<div class="form-group">
  {{ form.last_name.label_tag }}
  {{ form.last_name }}
  {{ form.last_name.errors }}
</div>
...
```

Edite `crm/forms.py`

```python
class PersonForm1(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Person
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(PersonForm1, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
```

Renderizando todos os campos com loop.

```html
...
{% for field in form %}
  <div class="form-group">
    {{ field.errors }}
    {{ field.label_tag }}
    {{ field }}
    {% if field.help_text %}
      <small class="text-muted">{{ field.help_text|safe }}</small>
    {% endif %}
  </div>
{% endfor %}
...
```

Ou simplesmente

```html
{{ form.as_p }}
```

remova o estilo de `.required:after`

E finalmente o `PersonForm` completo

```python
# crm/views.py
def person_create(request):
    template_name = 'crm/person_form.html'
    form = PersonForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('crm:person_list')

    context = {'form': form}
    return render(request, template_name, context)
```

```python
# crm/forms.py
class PersonForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Person
        # fields = '__all__'
        fields = (
            'first_name',
            'last_name',
            'email',
            'address',
            'address_number',
            'complement',
            'district',
            'city',
            'uf',
            'cep',
            'country',
            'cpf',
            'rg',
            'cnh',
            'active',
        )

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['active'].widget.attrs['class'] = None
```

Mostrar `person_form.html` pronto.


### Tela de Contato com forms.py e Django Widget Tweaks

https://pypi.org/project/django-widget-tweaks/

```
pip install django-widget-tweaks
```

Editar `settings.py`

```python
INSTALLED_APPS = [
    ...
    'widget_tweaks',
    ...
]
```

```python
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
```



```html
{% extends "base.html" %}
{% load widget_tweaks %}

{% block title %}
  <title>Band Contact</title>
{% endblock title %}

{% block content %}

  <style>
    span.required:after {
      content: "*";
      color: red;
    }
  </style>

  <h1>Send e-mail with Widget Tweaks</h1>
  <form class="form" method="POST">
    {% csrf_token %}
    {% for field in form.visible_fields %}
      <div class="form-group{% if field.errors %} has-error {% endif %}">
        <label for="{{ field.id_for_label }}">
          {% if field.field.required %}
            <span class="required">{{ field.label }} </span>
          {% else %}
            {{ field.label }}
          {% endif %}
        </label>
        {% render_field field class="form-control" %}
        {% for error in field.errors %}
          <span class="text-muted">{{ error }}</span>
        {% endfor %}
      </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>

{% endblock content %}

{% block js %}
  <script>
    $(document).ready(function(){
      $('#id_cc_myself').removeClass('form-control');
    })
  </script>
{% endblock js %}
```

![band_contact](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/band_contact.png)

---

### 6 - `form.as_p`

```html
<form class="form" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
```

---

Jinja

http://jinja.pocoo.org/

---


```html
<form class="form" method="POST">
  <input type="hidden" name="csrfmiddlewaretoken" value="zoQhKvyhfA6wJjagdIFK4ofxsJfHAEgJbBu3QyaIMaFfXRYrPeaMdPDgRlqGUyPT">
  <p>
    <label for="id_subject">Subject:</label>
    <input type="text" name="subject" maxlength="100" required id="id_subject">
  </p>
  <p>
    <label for="id_message">Message:</label>
    <textarea name="message" cols="40" rows="10" required id="id_message"></textarea>
  </p>
  <p>
    <label for="id_sender">Sender:</label>
    <input type="email" name="sender" required id="id_sender">
  </p>
  <p>
    <label for="id_cc_myself">Cc myself:</label>
    <input type="checkbox" name="cc_myself" id="id_cc_myself">
  </p>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

---

Live Code

![t](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/dr_strange_failure.gif)

---

Live Code - Fazer ele pegar os valores na view

Segundo https://simpleisbetterthancomplex.com/series/2017/09/18/a-complete-beginners-guide-to-django-part-3.html#how-not-implement-a-form

este é o jeito **errado** de implementar um formulário

Perai... mas a doc... fala do template

https://docs.djangoproject.com/en/2.2/topics/forms/#building-a-form

---

```python
#views.py
def my_send_email(request):
    email = request.POST
    # import ipdb; ipdb.set_trace()
    subject = email.get('subject')
    message = email.get('message')
    sender = email.get('sender')
    cc_myself = email.get('cc_myself')
    # enviar email
    pass
```

---


### 7 - Live Code completo

![diagrama](https://raw.githubusercontent.com/rg3915/tutoriais/master/django-basic/img/diagrama.png)

1. Criar url em urls.py
2. Criar função em views.py
3. Criar formulário em forms.py
4. Criar template

---

1. Criar url em urls.py

```
# urls.py
path('band/create/', v.band_create, name='band_create'),
```

---

2. Criar função em views.py

```python
# views.py
def band_create(request):
    ''' https://coderwall.com/p/o8tida/better-way-to-initialize-django-forms '''
    form = BandForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Process the data in form.cleaned_data
        form.save()
        return HttpResponseRedirect(resolve_url('bands'))
    return render(request, 'bands/band_create.html', {'form': form})
```
---

3. Criar formulário em forms.py

```python
# forms.py
class BandForm(forms.ModelForm):

    class Meta:
        model = Band
        fields = '__all__'
```

---

4. Criar template

```html
# band_create.html
{% extends "base.html" %}

{% block title %}
  <title>Band Create</title>
{% endblock title %}

{% block content %}

  <h1>Band Create</h1>
  <form class="form" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>

{% endblock content %}
```

---

### 8 - `form.as_table`

```html
<form class="form" method="POST">
    {% csrf_token %}
    {{ form.as_table }}
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
```

```html
<form class="form" method="POST">
  <input type="hidden" name="csrfmiddlewaretoken" value="jKXg5XBxZoKCH8wJxDC8DDC48ofPUZrxVXB2b0dYwYjlVGkU997aM40Nx0qOeT0H">

  <tr>
    <th>
      <label for="id_subject">Subject:</label>
    </th>
    <td>
      <input type="text" name="subject" maxlength="100" required id="id_subject">
    </td>
  </tr>

  <tr>
    <th>
      <label for="id_message">Message:</label>
    </th>
    <td>
      <textarea name="message" cols="40" rows="10" required id="id_message">
      </textarea>
    </td>
  </tr>

  <tr>
    <th>
      <label for="id_sender">Sender:</label>
    </th>
    <td>
      <input type="email" name="sender" required id="id_sender">
    </td>
  </tr>

  <tr>
    <th>
      <label for="id_cc_myself">Cc myself:</label>
    </th>
    <td>
      <input type="checkbox" name="cc_myself" id="id_cc_myself">
    </td>
  </tr>

  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

---

Seguir

https://simpleisbetterthancomplex.com/tag/forms/

---


### 9 - Manualmente

*Mostrar* https://docs.djangoproject.com/en/2.2/topics/forms/#rendering-fields-manually

---


### 10 - Creating Forms The Right Way

https://simpleisbetterthancomplex.com/series/2017/09/18/a-complete-beginners-guide-to-django-part-3.html#creating-forms-the-right-way

Usando forms.py

```python
# forms.py
class BandContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
```

```python
# views.py
def band_contact(request):
    """ A example of form """
    if request.method == 'POST':
        form = BandContactForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: Implementar o send_email
            return redirect('home')
    else:
        form = BandContactForm()
    return render(request, 'bands/band_contact.html', {'form': form})
```

---

### 11 - django-widget-tweaks

```
pip install django-widget-tweaks==1.4.3
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'widget_tweaks',
```

```html
# band_contact.html
<form class="form" method="POST">
{% csrf_token %}

{% for field in form.visible_fields %}
    <label for="{{ field.id_for_label }}">{{ field.label }}</label>

    {% render_field field class="form-control" %}

{% endfor %}

<button type="submit" class="btn btn-primary">Submit</button>
</form>
```

---


### 12 - Setting arguments for widgets

Mostrar

https://docs.djangoproject.com/en/2.2/ref/forms/widgets/#setting-arguments-for-widgets

---

### 13 - Django Bootstrap

https://github.com/zostera/django-bootstrap4

```
pip install django-bootstrap4
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'bootstrap4',
```

https://getbootstrap.com/

```html
# base.html
<!-- Bootstrap core CSS -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css">

<!-- jQuery -->
<script src="https://code.jquery.com/jquery-3.4.0.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"></script>

<!-- Bootstrap core JS -->
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"></script>
```

```html
# band_contact_bootstrap.html
{% extends "base.html" %}
{% load bootstrap4 %}

{% block content %}

  <form class="form" method="POST">
    {% csrf_token %}

    {% bootstrap_form form %}

    {% buttons %}
        <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
  </form>

{% endblock content %}
```

---

### 14 - Django Crispy Forms

https://django-crispy-forms.readthedocs.io/en/latest/


```
pip install django-crispy-forms
```

https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html

```python
# settings.py
INSTALLED_APPS = [
    ...
    'crispy_forms',
    ...
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
```

```html
# band_contact_crispy.html
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}

  <form class="form" method="POST">
    {% csrf_token %}

    {{ form|crispy }}

    <button type="submit" class="btn btn-primary">Submit</button>
  </form>

{% endblock content %}
```

---


### 15 - CreateView

https://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/CreateView/

```python
class BandCreate(CreateView):
    model = Band
    form_class = BandForm
    template_name = 'bands/band_form.html'
    success_url = reverse_lazy('bands')
```

---


### 16 - UpdateView

https://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/UpdateView/


---

### 17 - Upload File

https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

implementar
    one file
    multiple files

---

### 18 - inline_formset_factory

Felipe Frizzo

http://felipefrizzo.github.io/post/form-inline-cbv/

http://felipefrizzo.github.io/post/form-inline/

https://github.com/rg3915/vendas

rg-vendas.herokuapp.com

---

### 19 - django-registration-redux

https://django-registration-redux.readthedocs.io/en/latest/

![registration](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/SgFlV.jpg)

![login](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/262249cf7d76163b5573bd325b3bd9674948ca8e.png)

![reset password](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/password-change-form.png)

Implementar, mostrar rodando


---

![ajax](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/strange_ajax.jpg)

---

![img Dr. Strange kickout](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/kickout.gif)

---

![thor](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/strange_book.gif)

Comecei a estudar...

---

![dr_strange_failure](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/dr_strange_failure.gif)

Agora eu faço um POST via Ajax!

---

### 20 - POST via Ajax (Live Code)

1. Requer jQuery
2. Criar um template com ListView
3. Criar formulário num Modal
4. Criar uma url para fazer o Post
5. Criar View que salva os dados
6. Fazer o Post via Ajax
7. Retornar os novos dados na tabela

---

1. Requer jQuery

```html
# base.html
<script src="https://code.jquery.com/jquery-3.4.0.min.js"></script>
```

---

2. Criar um template com ListView

* 2.1. url
* 2.2. view
* 2.3. template

---

2.1. url

```python
# urls.py
path('members/', v.MemberList.as_view(), name='members'),
```

---


2.2. view

```python
# views.py
class MemberList(ListView):
    model = Member
    # template_name =
    # context_object_name =
    paginate_by = 10
```


---

2.3. template

```html
# member_list.html
{% extends "base.html" %}

{% block title %}
    <title>Member List</title>
{% endblock title %}

{% block content %}
    <h1>All Members</h1>

    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Instrument</th>
          <th>Band</th>
        </tr>
      </thead>
      <tbody>
        {% for object in object_list %}
          <tr>
            <td>{{ object.name }}</td>
            <td>{{ object.get_instrument_display }}</td>
            <td>{{ object.band }}</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>

{% endblock content %}
```


---


3. Criar formulário com Modal

```html
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="myModalLabel">Add Member</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <!-- Formulario -->
      <form action="">
        <div class="modal-body">
          <div class="form-group">
            {{ form.name.label }}
            {% render_field form.name class="form-control" %}
          </div>

          <div class="form-group">
            {{ form.instrument.label }}
            {% render_field form.instrument class="form-control" %}
          </div>

          <div class="form-group">
            {{ form.band.label }}
            {% render_field form.band class="form-control" %}
          </div>

        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save</button>
        </div>
      </form>

    </div>
  </div>
</div>
```

---


4. Criar uma url para fazer o Post

```python
# urls.py
path('members/add/ajax', v.members_add_ajax, name='members_add_ajax'),
```

---


5. Criar View que salva os dados

```python
def members_add_ajax(request):
    data = request.POST
    # import ipdb; ipdb.set_trace()
    name = data.get('name')
    instrument = data.get('instrument')
    band_pk = data.get('band')
    band = Band.objects.get(pk=band_pk)

    member = Member.objects.create(name=name, instrument=instrument, band=band)
    data = [member.to_dict_json()]
    return JsonResponse({'data': data})
```


---



6. Fazer o Post via Ajax

Requer `django-ajax-setup.js`

https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax

```js
// set up jQuery ajax object to always send CSRF token in headers
// https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
var getCookie = function (name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrfSafeMethod = function (method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  }
});
```

---


```js
<script>
  $('#save').on('click', function(e) {
      let url = '/members/add/ajax/'
      let postData = $('form').serialize();
      $.ajax({
        url: url,
        type: 'POST',
        data: postData,
        success: function(response) {
          // TODO
        },
        error: function(xhr) {
          console.log('Erro');
        },
        complete: function() {
          // TODO
        }
      });
    e.preventDefault();
  });
</script>
```

---



7. Retornar os novos dados na tabela

```js
success: function(response) {
  var template = '<tr>' +
      '<td>' + response.data[0].name + '</td>' +
      '<td>' + response.data[0].instrument + '</td>' +
      '<td>' + response.data[0].band + '</td>' +
      '</tr>'

  $('#table tbody').append(template)
},
error: function(xhr) {
  console.log('Erro');
},
complete: function() {
  // Fecha modal
  $('#myModal').modal('hide');
  // Limpa os campos
  $('#id_name').val('');
  $('#id_instrument').val('');
  $('#id_band').val('');
}
```



---




### 21 - POST com VueJS

1. Requer VueJS + Axios
2. Criar um template com função
3. Usar View `members_add_ajax`
4. Fazer o Post via Axios

---

1. Requer VueJS + Axios

```
<!-- Vue -->
<script src="https://cdn.jsdelivr.net/npm/vue"></script>
<!-- Axios -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js"></script>
```

---

2. Criar um template com função

```python
# views.py
def members_vue(request):
    return render(request, 'bands/members_vue.html')
```

```python
# urls.py
path('members_vue/', v.members_vue, name='members_vue'),
```

---

O template é members_vue.html

```html
# members_vue.html
{% extends "base.html" %}

{% block title %}
    <title>Members Vue</title>
{% endblock title %}

{% block content %}

<!-- Vue -->
<script src="https://cdn.jsdelivr.net/npm/vue"></script>
<!-- Axios -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js"></script>

<div id="app">

  <div class="float-left">
    <h1>Members with Vue</h1>
  </div>

  <table id="table" class="table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Instrument</th>
        <th>Band</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="member in members" :key="member.id">
        <td>${ member.name }</td>
        <td>${ member.instrument }</td>
        <td>${ member.band }</td>
      </tr>
    </tbody>
  </table>

</div>

{% endblock content %}
```



---

3. Usar View `members_add_ajax`

---

4. Fazer o Post via Axios

```vue
<script>
  axios.defaults.xsrfHeaderName = "X-CSRFToken";
  axios.defaults.xsrfCookieName = "csrftoken";
  var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
      members: [],
      name: '',
      instrument: '',
      band: '',
      url: '/members/json/',
      url_add: '/members/add/ajax/'
    },
    created () {
      axios.get(this.url)
      .then(result => {
        this.members = result.data.data
      })
    },
    methods: {
      add () {
        let bodyFormData = new FormData()
        bodyFormData.append('name', this.name)
        bodyFormData.append('instrument', this.instrument)
        bodyFormData.append('band', this.band)
        axios.post(this.url_add, bodyFormData)
        .then(response => {
          this.members.push(
            {
              name: response.data.data[0].name,
              instrument: response.data.data[0].instrument,
              band: response.data.data[0].band,
            }
          )
          this.name = ''
          this.instrument = ''
          this.band = ''
        })
      }
    }
  });
</script>
```

---

![thor](https://raw.githubusercontent.com/rg3915/django-grupy-jundiai/master/img/thor.gif)

Obrigado!
