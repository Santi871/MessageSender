import praw
from OAuth2Util import OAuth2Util
import configparser
from time import sleep


class MessageSender:

    def __init__(self, config):

        self.config_name = config
        self.config = configparser.ConfigParser()
        self.config.read(self.config_name)

        user_agent = self.config.get('bot', 'user_agent')

        self.r = praw.Reddit(user_agent)
        self._authenticate()

    def _authenticate(self):

        o = OAuth2Util(self.r, configfile=self.config_name)
        o.refresh(force=True)
        self.r.config.api_request_delay = 1
        print("Running...")

    def test_message(self):
        subject = self.config.get('message', 'subject')
        body = self.config.get('message', 'body')
        target = self.r.get_me().name
        self.r.send_message(target, subject, body)

    def send_messages(self, cooldown=0):
        targets = self.config.get('message', 'targets').split(',')
        subject = self.config.get('message', 'subject')
        body = self.config.get('message', 'body')
        sent_to = list()

        for target in targets:
            self.r.send_message(target, subject, body)
            print("Sent message to " + target)
            sent_to.append(target)
            sleep(cooldown)

        self.config['bot', 'last_sent_to'] = ','.join(sent_to)
        with open(self.config_name, 'w') as configfile:
            self.config.write(configfile)


