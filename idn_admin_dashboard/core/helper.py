import json
import ssl
from celery import shared_task
from .models import *
from django.shortcuts import get_object_or_404
import requests
import certifi
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os



def create_text_file(filename, content):
    with open(filename, "w",encoding='utf-8') as file:
        file.write(content)

def check_and_update(url):
    print("calling celery")
    timeout_seconds = 10  # Set the timeout period to 10 seconds
    try:
        instance = get_object_or_404(URL_dashboard, IDN_domain=url)
    except Exception as e:
         print("exception", e)
    # CHECK IF DOMAIN IS FUNCTIONAL OR NOT 
    try:    
        response = requests.get(url, verify=False,timeout=timeout_seconds)
        if response.status_code == 200:
            instance.idn_domain_running_status = 'True'
           
   
    except requests.ConnectionError as e:
           instance.idn_domain_running_status = 'Connection Error'
          

   # CHECK IF SSL IS VALID OR NOT 
    try:
        response = requests.get(url,verify=True)
        # print('response',response)
        if response.status_code == 200:
            instance.ssl_configuration_status = 'True'
        else:
            instance.ssl_configuration_status = 'Failed to fetch URL'                   
    except requests.ConnectionError as e:
            instance.ssl_configuration_status = 'Connection Error'
    except ssl.SSLError:
            instance.ssl_configuration_status = 'SSL Error'

    # CHECK LANGUAGE OF HOMEPAGE OF WESBITE  

    try:
        # Fetch HTML content from the URL
        response = requests.get(url,verify=False)

        if response.status_code == 200:
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
                    
            # Extract text content from HTML
            text = soup.get_text()
            
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            
            filename = '1.txt'
            
            create_text_file(filename, text)
               
            # Detect language of the text
            try:
                service_url = 'http://gist-nlp-cip:8080/languageIdentify'
                headers = {'User-Agent': 'Mozilla/5.0'}  # Example of headers
                myobj = {"ip_text": text}
                x = requests.post(service_url, headers=headers, json= myobj)
                # WRITE CONTENT IN FILE 
                lang_received = json.loads(x.text)['Output']
                if (lang_received == 'latin'):
                    instance.content_language = 'English'
                    
                else:
                    instance.content_language = lang_received 
                
            except requests.ConnectionError as e:
                instance.content_language = 'Language Service API Error'
        else:
            instance.content_language = 'Failed to Fetch URL'
    except requests.ConnectionError as e:
            instance.content_language = 'Connection Error'
    # Save the instance to persist the changes
    instance.save()  


def check_protocol(url):
    if url.__contains__("https" or "http"):
        print("URL_extracted contain https or http",url)
        updated_url =  url
    else:
        print("URL_extracted does'nt contain https or http",url)
        updated_url = "https://" + url
    return updated_url 

