from celery import shared_task
from .helper import *


@shared_task(bind=True)
def crawler_task(self,url):
   check_and_update(url)
   return "Task Completed"

@shared_task(bind=True)
def check_all_idn_domains_task(self):
   check_all_idn_domains()
   return "Cron Task Completed"
