from django.apps import AppConfig
from django.conf import settings

import logging


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):

        logger = logging.getLogger(__name__)

        if settings.SCHEDULER_AUTOSTART:       

            from tradingBot.admin.site   import site
            from tradingBot.admin.user   import user
            from tradingBot.admin.account import account                
            from tradingBot.utils.line_norify import lineNotifyMessage
            
            try:

                from . import scheduler                   

                scheduler.site_refresh_monitorlist('mysite')           

                with site('mysite') as mysite:
                    user_list =  mysite.get_user_list()   
                    for user_name in user_list:
                        with user(user_name=user_name, site=mysite) as this_user:
                            account_list = this_user.get_account_list()
                            for account_name in account_list:
                                with account(this_user, account_name) as this_account:
                                    scheduler.account_update_position('mysite', user_name, account_name)
                                    scheduler.account_trade('mysite', user_name, account_name)     

                logger.info('Service Ready!!')

                import django.core.management.commands.runserver as runserver

                cmd = runserver.Command()

                service_info = 'http://' + cmd.default_addr + ':' + cmd.default_port

                import socket

                hostname = socket.gethostname()

                logger.info('Service Ready on Host: %s URL: %s ' % (hostname, service_info))

                lineNotifyMessage('Dijango Service Ready on Host: %s URL: %s' % (hostname, service_info))

            except Exception as ex:
                logger.exception(ex)
                pass        
      
