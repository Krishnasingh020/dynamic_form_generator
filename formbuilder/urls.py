from django.urls import path
from . import views

app_name = 'formbuilder'

urlpatterns = [
    path('forms/<int:pk>/', views.render_form, name='render_form'),
    path('forms/<int:pk>/submit/', views.submit_form, name='submit_form'),
]

