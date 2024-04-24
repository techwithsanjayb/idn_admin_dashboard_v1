from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'core/home.html')

def add_new_url(request):
    pass

def total_record_table(request):
    pass