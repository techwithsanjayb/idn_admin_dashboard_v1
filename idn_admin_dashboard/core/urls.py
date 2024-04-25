from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
   
    path('', views.home, name="home"),
    path('add_new_url', views.add_new_url, name="add_new_url"),
    path('add_new_url_english', views.add_new_url_english, name="add_new_url_english"),
    path('total_record_table', views.total_record_table, name="total_record_table")
]