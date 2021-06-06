from django.urls import path

from myproject.crm import views as v

app_name = 'crm'


urlpatterns = [
    path('', v.person_list, name='person_list'),
    path('<int:pk>/', v.person_detail, name='person_detail'),
    path('create/', v.person_create, name='person_create'),
]
