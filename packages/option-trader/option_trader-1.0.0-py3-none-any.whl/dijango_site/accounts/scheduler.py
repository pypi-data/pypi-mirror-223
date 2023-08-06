from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from apscheduler.triggers.cron import CronTrigger

from django.conf import settings

from pytz import timezone

import logging

from tradingBot.settings import app_settings

logging.basicConfig()

logger = logging.getLogger('apscheduler').setLevel(logging.DEBUG)


from tradingBot.jobs.site import refresh_monitorlist
from tradingBot.jobs.account import update_position, trade

def site_refresh_monitorlist(site_name):
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(refresh_monitorlist(site_name).execute, 
                    'interval', hours=24,
                    #trigger=CronTrigger(
                    #day_of_week="mon-fri", hour="09-16", minute="00",
                    #timezone=timezone(app_settings.TIMEZONE), # Midnight on Monday, before start of the next work week.                        
                    #),                     
                    id= '%s [Refresh Watchlist]' % ('mysite'), 
                    jobstore='default',
                    max_instances=1,
                    replace_existing=True)                      
    register_events(scheduler)
    scheduler.start()

def account_update_position(site_name, user_name, account_name):
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(update_position(site_name, user_name, account_name).execute, 
                        'interval', hours=1, 
                        #trigger=CronTrigger(
                        #day_of_week="mon-fri", hour="09-15", minute="30",
                        #timezone=timezone(app_settings.TIMEZONE), # Midnight on Monday, before start of the next work week.                        
                        #),                         
                        id= '%s [ %s Update/Roll Positions]' % (user_name, account_name), 
                        jobstore='default',
                        max_instances=1,
                        replace_existing=True)                      
        register_events(scheduler)
        scheduler.start()
    except Exception as ex:
        logger.exception(ex)
        pass      


def account_trade(site_name, user_name, account_name):
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(trade(site_name, user_name, account_name).execute, 
                        'interval', hours=2, 
                        #trigger=CronTrigger(
                        #day_of_week="mon", hour="09-16", minute="00",
                        #timezone=timezone(app_settings.TIMEZONE), # Midnight on Monday, before start of the next work week.                        
                        #), 
                        id= '%s [%s Create New Positions]' % (user_name, account_name), 
                        jobstore='default',
                        max_instances=1,
                        replace_existing=True)                      
        register_events(scheduler)
        scheduler.start()
    except Exception as ex:
        logger.exception(ex)
        pass   