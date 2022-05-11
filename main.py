import os
import discord
import requests
import json
import random
from replit import db

client = discord.Client()

# Bot will send cheerful message if anyone sends
# message including a word from following
sad_words = set(['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'failure', 'fail', 'depressing', 'bad', 'awful'])

starter_encouragements=['Cheer up!', 'Hang in there.', 'You are a great person!']

def get_quote():
  '''
  Return a quote from the API
  '''
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return quote



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

my_secret = os.environ['TOKEN']
client.run(my_secret)




