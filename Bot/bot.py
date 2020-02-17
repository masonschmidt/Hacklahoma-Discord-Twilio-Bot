# Work with Python 3.6
import asyncio
from discord import Game
from discord.ext.commands import Bot
from collections import namedtuple
import pickle
from twilio.rest import Client
import os

account_sid = 'ACf00185389bcca9a08a1054ae2fb8b0aa'
auth_token = '762c895aa5a06f146170800567241c9d'
twilioClient = Client(account_sid, auth_token)

BOT_PREFIX = ("?", "!")
TOKEN = "NTQzODQ3MjY4MzYxNTY4MjU3.D0ClbQ.Y21LMtlJcLnsjjWLoM6eB85ql_I"  # Get at discordapp.com/developers/applications/me
User_Number = namedtuple('User_Number', ['user_id', 'user_name', 'number', 'last_received_message', 'received_message'])
Message_Info = namedtuple('Message_Info', ['message', 'number', 'message_present'])
user_numbers = []
NUMBER_FILE_DEST = 'number'

if os.path.isfile(NUMBER_FILE_DEST):
    with open(NUMBER_FILE_DEST, 'rb') as file:
        user_numbers = pickle.load(file)
else:
    user_numbers = []

discord_client = Bot(command_prefix=BOT_PREFIX)


@discord_client.command(description="Texts another user using a mention.",
                        brief="Text another user with the format !text <mention target user> <message in \\"">",
                        pass_context=True)
async def text(context, username, messageToSend):

    if context.message.author == discord_client.user:
        return

    print(context.message.mentions)
    target_user = findUser(context.message.mentions[0])

    if checkDataBase(target_user):
        messageTwilio = twilioClient.messages \
        .create(
        body="Discord message from " + context.message.author.name + ": " + messageToSend + "\nText back to send reply",
        from_='+12562911218',
        to=target_user.number)
        await discord_client.send_message(context.message.channel, "Thank you " + context.message.author.mention + ". Your message has been sent")
        updateUser(User_Number(target_user.user_id, target_user.user_name, target_user.number, context.message.channel.id, True))
        print(user_numbers)
    else:
        msg = 'Hello, that users Phone number is not yet set up. They need to use !change_number <number here>.'.format(context.message)
        await discord_client.send_message(context.message.channel, msg)

@discord_client.event
async def on_ready():
    await discord_client.change_presence(game=Game(name="the drums"))
    print("Logged in as " + discord_client.user.name)


@discord_client.async_event
async def on_server_join(server):
    print(str(list(server.channels)[1]))
    await discord_client.send_message(list(server.channels)[1], "Hi I am the test discord bot.\nIt's nice to meet all of you!")


@discord_client.command(description="Changes a users phone number, if they are not in the database then it adds their info",
                        brief="Change/Add a number Number should include country and area code as well as a + at the beggining",
                        pass_context=True)
async def change_number(context, number):
    is_dup = False
    for i in range(0, len(user_numbers)):
        if user_numbers[i].user_id == context.message.author.id:
            is_dup = True
            user_info = user_numbers.pop(i)
            new_info = User_Number(user_info.user_id, user_info.user_name, number, user_info.last_received_message,
                                   user_info.received_message)
            user_numbers.append(new_info)

    if is_dup:
        await discord_client.say("Your number has been updated!" + context.message.author.mention)
    else:
        user_numbers.append(User_Number(context.message.author.id, context.message.author.name, number, "", False))

        await discord_client.say("Thank you, your number has been added! " + context.message.author.mention)

    with open(NUMBER_FILE_DEST, 'wb') as file:
        pickle.dump(user_numbers, file)

    print(user_numbers)


@discord_client.command(description="Sends a user their stored number using private message",
                        brief="Get your number sent via private message",
                        pass_context=True)
async def my_number(context):
    num_found = False
    for i in user_numbers:
        if i.user_name == context.message.author.name:
            num_found = True
            await discord_client.send_message(context.message.author, "Your number is: " + i.number)

    if not num_found:
        await discord_client.send_message(context.message.author, "Sorry we could not find your number")

    print(user_numbers)

async def check_messages():
    await discord_client.wait_until_ready()
    while not discord_client.is_closed:
        print("Checking for messages:")
        found_message = False
        with open('C:\\Users\\mason\\Dropbox\\Hacklahoma\\Twilio\\Info', 'rb') as file:
            info = pickle.load(file)
            if info.message_present:
                print("Message Found")
                target_user = find_by_number(info.number)
                target_channel = discord_client.get_channel(target_user.last_received_message)
                await discord_client.send_message(target_channel, "Message from: " + target_user.user_name + "\n" + info.message)
                found_message = True

        if found_message:
            with open('C:\\Users\\mason\\Dropbox\\Hacklahoma\\Twilio\\Info', 'wb') as file:
                new_info = Message_Info('', '', False)
                pickle.dump(new_info, file)
        else:
            print("Message not found")

        await asyncio.sleep(1)


def checkDataBase(user):
    for current_user in user_numbers:
        if current_user.user_id == user.user_id:
            return True

    return False

def findUser(user):
    for current_user in user_numbers:
        if current_user.user_id == user.id:
            return current_user

    return False

def find_by_number(number):
    print(number)
    for current_user in user_numbers:
        if current_user.number == str(number):
            return current_user

    return False

def updateUser(user):
    for i in range(0, len(user_numbers)):
        if user_numbers[i].user_id == user.user_id:
            user_numbers.pop(i)
            new_info = User_Number(user.user_id, user.user_name, user.number, user.last_received_message,
                                   user.received_message)
            user_numbers.append(new_info)

    with open(NUMBER_FILE_DEST, 'wb') as file:
        pickle.dump(user_numbers, file)

    return False


discord_client.loop.create_task(check_messages())
discord_client.run(TOKEN)