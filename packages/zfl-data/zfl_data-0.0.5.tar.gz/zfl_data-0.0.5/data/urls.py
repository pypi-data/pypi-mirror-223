from django.urls import path
from . import views



app_name = 'data'

urlpatterns = [
    path('', views.index, name='index'),
    # path('blogs_plot/', views.blogs_plot, name='blogs_plot')
]
