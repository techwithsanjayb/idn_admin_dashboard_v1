from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
   
    path('', views.home, name="home"),
    path('idn_domain_record', views.idn_domain_record, name="idn_domain_record"),
    path('idn_domain_forms', views.idn_domain_forms, name="idn_domain_forms"),
    path('cron',views.cron_function,name='cron_function')
   
]