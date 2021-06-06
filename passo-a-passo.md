# Passo a passo

# django-forms-tutorial

![1400605](img/1400605.jpg)

![dr_strange_failure](img/dr_strange_failure.gif)



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


### Editar

Edite `crm/urls.py`

```python
...
path('<int:pk>/update', v.person_update, name='person_update'),
...
```

Edite `crm/views.py`

```python
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
```


## Tela de Contato com forms.py e Django Widget Tweaks

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
# crm/forms.py
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
```



```html
<!-- contact_form.html -->
{% extends "base.html" %}
{% load widget_tweaks %}

{% block title %}
  <title>Contact</title>
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
    });
  </script>
{% endblock js %}
```

![band_contact](img/band_contact.png)

Editar `crm/urls.py`

```python
path('contact/send/', v.send_contact, name='send_contact'),
```

Editar `crm/views.py`

```python
from django.core.mail import send_mail


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
```

Editar `nav.html`

```html
<li class="nav-item">
  <a class="nav-link" href="{% url 'crm:send_contact' %}">Contato</a>
</li>
```

Editar `base.html`

```html
{% block js %}{% endblock js %}
```

Enviar o e-mail com MailHog.

```
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

Configurar `settings.py`

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
EMAIL_HOST = config('EMAIL_HOST', '0.0.0.0')  # localhost
EMAIL_PORT = config('EMAIL_PORT', 1025, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
```



### Django Bootstrap

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

Edite `base.html`

```html
<!-- base.html -->
  <!-- Bootstrap core CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">

  <!-- jQuery -->
  <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
  <!-- Bootstrap core JS -->
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
```


Edite `person_bootstrap_form.html`

```html
<!-- person_bootstrap_form.html -->
{% extends "base.html" %}
{% load bootstrap4 %}

{% block content %}
  <h1>Bootstrap form</h1>

  <form class="form" method="POST">
    {% csrf_token %}

    {% bootstrap_form form %}

    {% buttons %}
        <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
  </form>

{% endblock content %}
```

Editar `nav.html`

```html
<li class="nav-item">
  <a class="nav-link" href="{% url 'crm:person_bootstrap_create' %}">Bootstrap Create</a>
</li>
```

Edite `crm/urls.py`

```python
path('bootstrap/create/', v.PersonBootstrapCreate.as_view(), name='person_bootstrap_create'),
```

Edite `crm/views.py`

```python
from django.views.generic import CreateView


class PersonBootstrapCreate(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'crm/person_bootstrap_form.html'
```

Leia [django-cbv-tutorial](https://github.com/rg3915/django-cbv-tutorial)

E veja a Live [Django Class Based View como você nunca viu](https://youtu.be/C7Ecugxa7ic)


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

AQUI


---

### 17 - Upload File


YouTube: 

Github: 



implementar
    one file
    multiple files

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
