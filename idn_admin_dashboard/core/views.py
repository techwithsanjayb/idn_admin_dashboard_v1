from django.shortcuts import render,redirect
import pandas as pd
from .forms import idn_dashboard_form,English_Domain_Form
from django.contrib import messages
from .models import *
from core.tasks import crawler_task,check_all_idn_domains_task
from .helper import *






def home(request):
    return render(request,'core/home.html')
    
# -----ADDED BY SANJAYB -------

def idn_domain_record(request):
    logs("Hello Sanjay")
    English_Domain_total_records = English_Domain.objects.count()
    URL_dashboard_total_records = URL_dashboard.objects.count()
    URL_dashboard_total_records_governmnet = English_Domain.objects.filter(category__category_name="Government").count()
    URL_dashboard_total_records_private = English_Domain.objects.filter(category__category_name="Private").count()
    URL_dashboard_obj = URL_dashboard.objects.all()
    return render(request,'core/idn_domain_record.html', {'URL_dashboard_obj':URL_dashboard_obj,'URL_dashboard_total_records':URL_dashboard_total_records,'English_Domain_total_records':English_Domain_total_records,'URL_dashboard_total_records_governmnet':URL_dashboard_total_records_governmnet,'URL_dashboard_total_records_private':URL_dashboard_total_records_private})
        

def idn_domain_forms(request):
    English_Domain_Form_obj = English_Domain_Form()
    idn_dashboard_form_obj = idn_dashboard_form()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'IDNDOMAINFORM':
            form = idn_dashboard_form(request.POST)
             # Check if form is valid or not and any params is not null
            if form.is_valid():
                try:
                    # Extract URL
                    URL_extracted = form.cleaned_data['IDN_domain']

                    # Check URL Protocal and updating
                    URL_extracted =  check_protocol(URL_extracted)
                    print('URL_extracted',URL_extracted)
                    # Extracting only URL part 
                    # URL_extracted =  extract_domain(URL_extracted)
                                
                    exists = URL_dashboard.objects.filter(IDN_domain=URL_extracted).exists()
                    if not exists:        
                        print("Check Exisitance of Domain : ", exists)
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
                        return redirect('core:idn_domain_record')
                    else:
                        messages.info(request,"Entered IDN domain already exists !!")
                        return redirect('core:idn_domain_forms')
                except Exception as e :
                    messages.error(request, 'Some error occured .Please try after sometime ')    
                    return redirect('core:idn_domain_record')    
            else:
                print("due to errors not submitted", form.errors)
                messages.error(request, 'Please correct errors')
                return render(request,'core/idn_domain_forms.html', {'idn_dashboard_form_obj': idn_dashboard_form_obj,'English_Domain_Form_obj':English_Domain_Form_obj})
            
        elif form_type == 'ENGDOMAINFORM':
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
                    return redirect('core:idn_domain_record')
                except Exception as e :
                    messages.error(request, 'Some error occured .Please try after sometime ')    
                    return redirect('core:idn_domain_forms')    
            else:
                print("due to errors not submitted", eng_form.errors)
                messages.error(request, 'Please correct errors')
                return render(request,'core/idn_domain_forms.html', {'idn_dashboard_form_obj': idn_dashboard_form_obj,'English_Domain_Form_obj':English_Domain_Form_obj})
    else:
        return render(request, 'core/idn_domain_forms.html', {'idn_dashboard_form_obj': idn_dashboard_form_obj,'English_Domain_Form_obj':English_Domain_Form_obj})
    

def cron_function():
    check_all_idn_domains_task.delay()
    return redirect('core:idn_domain_record')