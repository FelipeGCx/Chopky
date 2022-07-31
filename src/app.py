import os
import irc.bot
import requests
from dotenv import load_dotenv
load_dotenv()

class MyBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel ):
        self.client_id = client_id
        self.token = token
        self.channel = f'#{channel}'
        # Get the channel id, we will need it for the API calls
        url = f'https://api.twitch.tv/kraken/users?login={channel}'
        headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        response = requests.get(url, headers=headers).json()
        self.channel_id = response['users'][0]['id']
        # Create the IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print(f'🚀 Connecting to {server} on port {port}')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + self.token)], username, username)
        
    def on_welcome(self, c, e):
        print(f'🎉 Connected to {c.get_server_name()}')
        # you must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        print(f'🎉 Joined {self.channel}')
        
    def on_pubmsg(self,c,e):
        print(e)
    
def main():
    # get the env variables we need
    username = os.getenv('TWITCH_USERNAME')
    client_id = os.getenv('TWITCH_CLIENT_ID')
    token = os.getenv('TWITCH_TOKEN')
    channel = os.getenv('TWITCH_CHANNEL')
    # create the bot
    bot = MyBot(username, client_id, token, channel)
    bot.start()
    
if __name__ == '__main__':
    main()