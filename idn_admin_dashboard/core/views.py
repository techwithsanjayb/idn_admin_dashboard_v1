from django.shortcuts import render,redirect
import pandas as pd
from .forms import idn_dashboard_form,English_Domain_Form
from django.contrib import messages
from .models import *
from core.tasks import crawler_task
from .helper import *


def home(request):
    return render(request,'core/home.html')

def add_new_url(request):
    idn_dashboard_form_obj = idn_dashboard_form()
    
    if request.method == 'POST':
        form = idn_dashboard_form(request.POST)

        # Check if form is valid or not and any params is not null
        if form.is_valid():
            try:
                # Extract URL
                URL_extracted = form.cleaned_data['IDN_domain']

                # Check URL Protocal and updating
                URL_extracted =  check_protocol(URL_extracted)
                
                # Extracting only URL part 
                # URL_extracted =  extract_domain(URL_extracted)
                               
                
                form_obj = form.save(commit=False)
                print('form_OBJ',form_obj)
                form_obj.content_language = 'NA'
                form_obj.ssl_configuration_status='NA'
                form_obj.idn_domain_running_status='NA'
                form_obj.Remark='NA'
                form_obj.IDN_domain = URL_extracted
                form_obj.save()
              
                # Call function celery
                crawler_task.delay(URL_extracted)
                messages.info(request, 'Record Added Successfully ! Your data would be updated soon.')
                return redirect('core:total_record_table')
            except Exception as e :
                messages.error(request, 'Some error occured .Please try after sometime ')    
                return redirect('core:add_new_url')    
        else:
            print("due to errors not submitted", form.errors)
            messages.error(request, 'Please correct errors')
            return render(request, 'core/url_add_form.html', {'idn_dashboard_form_obj': idn_dashboard_form_obj}) 
    else:
        return render(request, 'core/url_add_form.html', {'idn_dashboard_form_obj': idn_dashboard_form_obj})
    
    

def total_record_table(request):
    URL_dashboard_obj = URL_dashboard.objects.all()
    return render(request,'core/total_record_table.html',{'URL_dashboard_obj':URL_dashboard_obj})

def add_new_url_english(request):
    English_Domain_Form_obj = English_Domain_Form()
    if request.method == 'POST':
        eng_form = English_Domain_Form(request.POST)

        # Check if form is valid or not and any params is not null
        if eng_form.is_valid():
            try:
                # Extract URL
                URL_extracted = eng_form.cleaned_data['domain_name']

                # Check URL Protocal and updating
                URL_extracted =  check_protocol(URL_extracted)
                
                eng_form.save()
                messages.success(request, 'Record Added Successfully ')
                return redirect('core:add_new_url')
            except Exception as e :
                messages.error(request, 'Some error occured .Please try after sometime ')    
                return redirect('core:add_new_url_english')    
        else:
            print("due to errors not submitted", eng_form.errors)
            messages.error(request, 'Please correct errors')
            return render(request, 'core/url_add_english_form.html', {'English_Domain_Form_obj': English_Domain_Form_obj}) 
    
    else:
        
        return render(request,'core/url_add_english_form.html', {'English_Domain_Form_obj':English_Domain_Form_obj})