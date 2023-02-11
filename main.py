
import discord
import os
import requests
import json
from keep_alive import keep_alive


client = discord.Client()

@client.event
async def on_ready():
  print('I have logged in as {0.user}'.format(client))


def resolveNames(name):
  response = requests.get(url="https://api.prd.space.id/v1/getAddress?tld=&domain="+name+".bnb")
  result = json.loads(response.text)
  return result

def makeEmbed(code, name, **msg):
  if code == "00":
    description = "Domain **{0}.bnb** is available :raised_hands: \n\nuse the link below to mint:\nhttps://app.space.id/name/{1}.bnb/register\n ".format(name,name)
  if code == "01":
    description = "Domain {0}.bnb is not available :slight_frown:   \n\nTry another name".format(name)
  if code == "1":
    description = msg['msg']+" :x: \n\nTry another name"
    
  embed = discord.Embed(title="Search Result", description= description, color=0x29f9b2)
  embed.set_footer(text="powered by space id api")
  return embed

@client.event
async def on_message(message):
  zeroAddress = "0x0000000000000000000000000000000000000000"
  if message.author == client.user:
    return

  if message.content.startswith('!name'):
    name = message.content.split(' ')[1].lower()
    result = resolveNames(name)
    if result["code"] == 0:
      if result["address"] == zeroAddress:
        code = "00"
        embed = makeEmbed(code,name)
        await message.reply(embed=embed)
      else:
        code = "01"
        embed = makeEmbed(code,name)
        await message.reply(embed=embed)
    if result["code"] == 1:
      code = "1"
      msg = result['msg']
      embed = makeEmbed(code=code, name=name, msg=msg)
      await message.reply(embed=embed)

keep_alive()
try:
  client.run(os.getenv("BOT_TOKEN"))
except discord.HTTPException as e:
  if e.status == 429:
    print("The Discord servers denied the connection for making too many requests")
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system('kill 1')
        #print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
  else:
    raise e
