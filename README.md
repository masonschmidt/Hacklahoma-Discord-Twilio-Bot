# Hacklahoma Discord/Twilio Bot
 A Discord bot that was created for Hacklahoma that allows users to send sms
 messages through discord and discord messages through sms.

## Discord BOT
The Discord Bot runs as a user on a discord server and listens for commands that
begin with '!' or '?'. Users can interact with this bot to add their phone numbers
(in private chats with the bot) and the bot will then remember that phone number
and relay text messages from other users to the twilio Flask server and outputs
replies to the last place that user received a message. This uses the discord API.

## Twilio/flask
This runs a flask server that interacts with the twilio api and the discord bot
to relay messages back and forth from the discord bot and the user's sms messaging
using it's own twilio phone number.


### Interacting with the bot, adding a number, and sending a text
![Creating Number](/Censored1.png)

### Getting a text and sending a reply
![Texts](/FirstTexts.jpg)

### Interactions with other users
![Additional Interactions 1](/Censored2.png)
![Additional Interactions 2](/Censored4.png)
