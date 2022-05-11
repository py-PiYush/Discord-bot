import os
import discord
import requests
import json
import random
from replit import db

client = discord.Client()

# Bot will send cheerful message if anyone sends
# message including a word from following
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'failure', 'fail', 'depressing', 'bad', 'awful']

starter_encouragements=['Cheer up!', 'Hang in there.', 'You are a great person!']

def get_quote():
  '''
  Return a quote from the API
  '''
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return quote

def update_encouragements(en_msg):
  '''
  Update encouragements in the database. Return true if successfully deleted
  '''
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(en_msg)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [en_msg]

def delete_encouragement(index):
  '''
  delete the encouraging message at given index
  '''
  encouragements = db['encouragements']
  if len(encouragements)>index:
    del encouragements[index]
    db['encouragements'] = encouragements
    return 1
  else:
    return 0

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

  options = starter_encouragements
  if 'encouragements' in db.keys():
    options = options + list(db['encouragements'])
  
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith('$new'):
    en_msg = msg.split('$new ', 1)[1]
    update_encouragements(en_msg)
    await message.channel.send('New encouraging message added.')

  if msg.startswith('$del'):
    encouragements=[]
    if 'encouragements' in db.keys():
      index = int(msg.split('$del',1)[1])
      if delete_encouragement(index):
        encouragements = db['encouragements']
        await message.channel.send(f'Successfully deleted!\n{list(encouragements)}')
      else:
        encouragements = db['encouragements']
        await message.channel.send(f'Index limit: 0 - {len(encouragements)-1}')
    else:
      await message.channel.send(encouragements)
    
  
my_secret = os.environ['TOKEN']
client.run(my_secret)




