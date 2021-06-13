from django.urls import path

from myproject.crm import views as v

app_name = 'crm'


urlpatterns = [
    path('', v.person_list, name='person_list'),
    path('<int:pk>/', v.person_detail, name='person_detail'),
    path('create/', v.person_create, name='person_create'),
    path('<int:pk>/update/', v.person_update, name='person_update'),
    path('contact/send/', v.send_contact, name='send_contact'),
    path('bootstrap/create/', v.PersonBootstrapCreate.as_view(), name='person_bootstrap_create'),
    path('crispy/create/', v.PersonCrispyCreate.as_view(), name='person_crispy_create'),
    path('photo/create/', v.photo_create, name='photo_create'),
    path('create/ajax/', v.photo_create_ajax, name='photo_create_ajax'),
    path('vuejs/', v.person_vuejs_list, name='person_vuejs_list'),
    path('vuejs/json/', v.person_json, name='person_json'),
    path('vuejs/create/', v.person_vuejs_create, name='person_vuejs_create'),
    path('<int:pk>/vuejs/delete/', v.person_vuejs_delete, name='person_vuejs_delete'),
]
