import json
import logging
import re
import requests
import time
import os

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        os.system("pip install apscheduler")
        from apscheduler.schedulers.background import BackgroundScheduler

        sched = BackgroundScheduler()
        sched.start()
        job = sched.add_job(self.msg_writer.sendReminder(), 'cron', day_of_week='mon-fri', hour=20, minute=32)
        
   
        
        
   
        
        
    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            try:
                self.msg_writer.write_error(event['channel'], json.dumps(event))
            except:
                pass
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself
        if not self.clients.is_message_from_me(event['user']):

            msg_txt = event['text']
            
            
            #if self.clients.is_bot_mention(msg_txt):
                # e.g. user typed: "@pybot tell me a joke!"
            if msg_txt.lower()=='help':
                self.msg_writer.write_help_message(event['channel'])
            elif msg_txt.lower().split(' ')[0] == 'view':
                self.msg_writer.viewlocation(event['channel'], event['user'],msg_txt.rstrip().split(' ')[-1])
            else:
                self.msg_writer.setmylocation(event['channel'], event['user'],msg_txt)
            #elif 'setmylocation' in msg_txt:
            #    self.msg_writer.setmylocation(event['channel'], event['user'],msg_txt.split(' ')[-1])
            #elif 'viewmylocation' in msg_txt:
                #self.msg_writer.viewmylocation(event['channel'], event['user'])
            #elif 'viewlocation' in msg_txt:
                #self.msg_writer.viewlocation(event['channel'], event['user'],msg_txt.split(' ')[-1])
                    
            #else:
            #    self.msg_writer.write_prompt(event['channel'])
