import json
import ssl
from celery import shared_task
from .models import *
from django.shortcuts import get_object_or_404,Http404
import requests
import certifi
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from idn_admin_dashboard.logger import log, logs

def check_protocol(url):
    print("Inside check protocol-------")
    if url.__contains__("https" or "http"):
        print(f"If {url} contains https")
        #logs(f"{url} contain https or http ")
        updated_url =  url
    else:
        print(f"If {url} does not contains https")
        # logs(f" Adding https or http in {url} ")
        updated_url = "https://" + url
        # logs(f"returning Updated url")
    return updated_url 


def create_text_file(filename, content):
    with open(filename, "w",encoding='utf-8') as file:
        file.write(content)

def check_all_services(url):
    timeout_seconds = 10  # Set the timeout period to 10 seconds
    # CHECK IF DOMAIN IS FUNCTIONAL OR NOT 
    try:
        logs(f"Fetching Domain instance from Databse based on URL provided {url} ")
        instance = get_object_or_404(URL_dashboard, IDN_domain=url)
        print("Instance Found : ",instance)
    except Exception as e:
        logs(f"Exception Occured {e}--- Fetching Domain {url} instance from Database based on URL provided")
        print("Error occured...")

    try:
        logs(f"Checking that Fetched Domain {url} is running or not by request.get method")
        instance = get_object_or_404(URL_dashboard, IDN_domain=url)  
        response = requests.get(url, verify=False,timeout=timeout_seconds)
        print("Response : ", response)
        if response.status_code == 200:
            logs(f"{url} Domain Status is 200 IT is running")
            instance.idn_domain_running_status = True 
            logs(f"{url} Domain Status has been updated to true") 
   
    except requests.ConnectionError as e:
        logs(f"Connection Error occured {e}--- Fetching Domain {url} ") 
        instance.idn_domain_running_status = 'Connection Error'
        logs(f"Domain Status has been updated to Connection Error")
          

   # CHECK IF SSL IS VALID OR NOT 
    try:
        instance = get_object_or_404(URL_dashboard, IDN_domain=url)
        logs(f"Checking that Fetched Domain {url} for SSL check is running or not by request.get method ")
        response = requests.get(url,verify=True)
        
        # print('response',response)
        if response.status_code == 200:
            logs(f"{url} Domain Status for SSL check is 200 IT is running") 
            instance.ssl_configuration_status = 'True'
            logs(f"{url} SSL Status has been updated to true") 
        else:
            logs(f"Domain {url} for SSL check is not running") 
            instance.ssl_configuration_status = 'Failed to fetch URL'
            logs(f"{url} SSL Status has been updated to Failed to fetch URL")                   
    except requests.ConnectionError as e:
            logs(f"Connection Error occured {e}--- Fetching SSL for {url} ") 
            instance.ssl_configuration_status = 'Connection Error' 
            logs(f"SSL Status has been updated to Connection Error")
    except ssl.SSLError:
            instance.ssl_configuration_status = 'SSL Error'  
            logs(f"SSL Status has been updated to SSL Error")

    
    # CHECK LANGUAGE OF HOMEPAGE OF WESBITE  
    try:
        logs(f"Checking that Fetched Domain {url} is running or not by request.get method to content language check") 
        # Fetch HTML content from the URL
        response = requests.get(url,verify=False)
        
        if response.status_code == 200:
            logs(f"{url} Domain Status for Content check is 200") 
            # Parse HTML content
            logs(f"{url} is being parsed by beautiful soap ") 
            soup = BeautifulSoup(response.content, 'html.parser')
                    
            # Extract text content from HTML
            logs(f"Extract text content from HTML") 
            text = soup.get_text()
            logs(f"Extract text content from HTML") 
            
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            logs(f"break into lines and remove leading and trailing space on each") 
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            logs(f"break multi-headlines into a line each") 
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            logs(f"drop blank lines") 
            filename = '1.txt'
            create_text_file(filename, text)               
            logs(f"File Created -- ") 
            # Detect language of the text
            try:
                service_url = 'http://gist-nlp-cip:8080/languageIdentify'
                headers = {'User-Agent': 'Mozilla/5.0'}  # Example of headers
                myobj = {"ip_text": text}
                logs(f"Service For checking content is being called ")
                x = requests.post(service_url, headers=headers, json= myobj)
                # WRITE CONTENT IN FILE 
                lang_received = json.loads(x.text)['Output']
                logs(f"Service For checking content is being called and language received is {lang_received} ")
                if (lang_received == 'latin'):
                    instance.content_language = 'English'
                    logs(f"language content language is set ")
                else:
                    instance.content_language = lang_received      
                    logs(f"language content language is set to other than english ")
                
            except requests.ConnectionError as e:
                instance.content_language = 'Language Service API Error'   
                logs(f"language content language is set to other than english ")
        else:
            instance.content_language = 'Failed to Fetch URL'    
            logs(f"language content language is not set because of Failed to Fetch URL")
    except requests.ConnectionError as e:
            instance.content_language = 'Connection Error'
            logs(f"language content language is not set because of Connection Error")


    # Save the instance to persist the changes
    logs(f"Parameters have been updated and instance has been saved ")
    instance.save()
   

def check_and_update(url):
    logs(f"++++================================={url}==========================================++++")
    logs(f"Check and Update Function called to update status of domain parameter {url}")
    print("Url Found : ", url)
    try:
        logs(f"Fetching Domain instance from Databse based on URL provided {url} ")
        instance = get_object_or_404(URL_dashboard, IDN_domain=url)
        print("Instance Found : ",instance)
    except Exception as e:
        logs(f"Exception Occured {e}--- Fetching Domain {url} instance from Database based on URL provided")
        print("Error occured...")
    
    check_all_services(url)
    
  
    


def check_all_idn_domains():    
    all_idn_domain_objects = URL_dashboard.objects.values_list('IDN_domain', flat=True)
     # CHECK IF DOMAIN IS FUNCTIONAL OR NOT 
    for url in all_idn_domain_objects:
        print("domain url ----------------------",url)
        check_all_services(url)
            

   