import requests

import logging

from tradingBot.settings import app_settings    


def lineNotifyMessage(msg, token=app_settings.LINE_NOTIFICATION_TOKEN):

    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code


if __name__ == "__main__":

  #'Df0tC09dtPoshq3psJaeen3ubXXH5e94u74FezQEalb'
  message = '基本功能測試'
  status = lineNotifyMessage(message)
  print(status)