import logging
import random
import time
import requests

logger = logging.getLogger(__name__)
userdict = {}

class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.token = self.clients.get_token()
    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def setmylocation(self,channel_id,user_id,location):
        payload = {'token':self.token,'user':user_id}
        r = requests.get('https://slack.com/api/users.info', params=payload)
        username = str(r.json()['user']['name'])
        userdict[user_id]=[username,location,time.strftime("%H:%M:%S %m/%d/%y")]
        txt = "Your location was set to " + userdict[user_id][1] + " as of " + userdict[user_id][2]
        self.send_message(channel_id, txt)
        
    def viewmylocation(self,channel_id,user_id):
        try:
            txt = userdict[user_id][0] + " is at " + userdict[user_id][1] + " as of " + userdict[user_id][2]
            self.send_message(channel_id, txt)
        except KeyError:
            txt = "User has not inputted a location yet"
            self.send_message(channel_id, txt)
         
    def viewlocation(self,channel_id,user_id,user_find):
        if user_find.lower() == 'all':
            txtlist = []
            for k,v in userdict.iteritems():
                txtlist += [v[0] + " is at " + v[1] + " as of " + v[2]]
            for x in txtlist:
                self.send_message(channel_id, x)
        else:
            for k,v in userdict.iteritems():
                if v[0] == user_find:
                    txt = v[0] + " is at " + v[1] + " as of " + v[2]
                    self.send_message(channel_id, txt)
                    break
                txt = "User has not inputted a location yet or does not exist"
                self.send_message(channel_id, txt)
    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}\n{}'.format(
            "Available commands:",
            "> `setmylocation [location]` - Set your location",
            "> `viewmylocation` - View what your own location is set as",
            "> `viewlocation [username]` - View location of user",
            "> `viewlocation all` - View location of all users")
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "Type help for a list of commands"
        self.send_message(channel_id, txt)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

   