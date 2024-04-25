from django import forms
from django.forms import ModelForm
from .models import URL_dashboard,English_Domain,language_list, category_list





class idn_dashboard_form(forms.ModelForm):
    IDN_domain = forms.CharField(label="Enter Idn Domain", max_length=200, widget=forms.TextInput(
        attrs={"class": "form-control", 'id': 'inputIdnDomain', "placeholder": "Enter domain",
               'autocomplete': 'off', 'required': True}))
    English_domain = forms.ModelChoiceField(label="Select English Domain",
                                                           queryset=English_Domain.objects.all(),
                                                           widget=forms.Select(
                                                               attrs={"class": "form-control",
                                                                      'id': 'inputEnglishDomain',
                                                                      'autocomplete': 'off'}))
    
    Language = forms.ModelChoiceField(label="Select Language",
                                                           queryset=language_list.objects.all(),
                                                           widget=forms.Select(
                                                               attrs={"class": "form-control",
                                                                      'id': 'inputLanguage',
                                                                      'autocomplete': 'off'}))

    class Meta:
        model = URL_dashboard
        fields = ['IDN_domain','English_domain','Language']

    def clean(self):
        print("FORMS.PY FILE : CLEAN METHOD CALLING")
        super(idn_dashboard_form, self).clean()
        # validate_idn_dashboard_form(self)
        
class English_Domain_Form(forms.ModelForm):
   
    category = forms.ModelChoiceField(label="Select Website Category",
                                                           queryset=category_list.objects.all(),
                                                           widget=forms.Select(
                                                               attrs={"class": "form-control",
                                                                      'id': 'EnglishCategory',
                                                                      'autocomplete': 'off'}))
    
    domain_name = forms.CharField(label="Enter English Domain", max_length=256, widget=forms.TextInput(
                attrs={"class": "form-control", 'id': 'inputengDomain', "placeholder": "Enter english domain",
               'autocomplete': 'off', 'required': True}))

    class Meta:
        model = English_Domain
        fields = ['domain_name', 'category']

    def clean(self):
        print("FORMS.PY FILE : CLEAN METHOD CALLING")
        super(English_Domain_Form, self).clean()
        # validate_idn_dashboard_form(self)
