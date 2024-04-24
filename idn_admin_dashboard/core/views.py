from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'core/home.html')

def add_new_url(request):
    return render(request,'core/url_add_form.html')

def total_record_table(request):
    return render(request,'core/total_record_table.html')