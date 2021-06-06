from django.urls import path

from myproject.crm import views as v

app_name = 'crm'


urlpatterns = [
    path('', v.person_list, name='person_list'),
    path('<int:pk>/', v.person_detail, name='person_detail'),
    path('create/', v.person_create, name='person_create'),
    path('bootstrap/create/', v.PersonBootstrapCreate.as_view(), name='person_bootstrap_create'),
    path('<int:pk>/update/', v.person_update, name='person_update'),
    path('contact/send/', v.send_contact, name='send_contact'),
]
