from django.urls import path
from . import views

app_name = 'demos'
urlpatterns = [
    path('', views.index, name='index'),
    path('subData/', views.subData, name='data'),
    path('drop/', views.drop, name='drop'),
    path('delete/', views.deleteData, name='delete'),
    path('success/',views.success,name='success'),
]
