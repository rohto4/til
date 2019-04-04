import os
from slackclient import SlackClient
import datetime

# get token
slack_token = os.environ["SLACK_TOKEN"]
sc = SlackClient(slack_token)

# get time

now = datetime.datetime.now()
fixed = datetime.datetime(now.year, now.month, now.day, 17, 30, 0)

fixedStr = fixed.strftime('%H:%M:%S')
nowStr = now.strftime('%H:%M:%S')

text = "定時 : "

# choice API methods and hikisu
sc.api_call(
  "chat.postMessage",
  channel="#yayoibot",
  text=text
)