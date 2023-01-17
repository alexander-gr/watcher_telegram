import json
import logging
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser

from config import API_ID, API_HASH, CONFIG, ADMIN_ID
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

client = TelegramClient('anon', API_ID, API_HASH)


@client.on(events.NewMessage(chats=list(CONFIG.keys())))
async def handler(event):
    '''
    This function is an event handler for new messages on Telegram. It listens for new messages in specific channels (specified in the 'chats' parameter of the events.NewMessage() decorator) and checks for a specific pattern in the message text. If the pattern is found, the message is forwarded to a specified target channel.

    Parameters:
    - event (telegram.events.NewMessage): The event object containing metadata about the new message.

    Returns: None
    '''

    # get new message event metadata
    channel_id = event.message.peer_id.channel_id
    # message_text = event.message.message
    message_text = event.raw_text

    # check if the new message satisfies given conditions
    for pattern in CONFIG[channel_id]["pattern"]:
        if pattern in message_text:
            print(f"Pattern: <{pattern}> met <{message_text}>")
            await client.forward_messages(CONFIG[channel_id]["target_id"], event.message)


@client.on(events.NewMessage(pattern="ping"))
async def handler(event):
    """
    This function is an event handler for new messages on Telegram that match a specific pattern. It listens for new messages that contain the text "ping" (specified in the 'pattern' parameter of the events.NewMessage() decorator) and reply to the message with "pong".
    
    Parameters:
    - event (telegram.events.NewMessage): The event object containing metadata about the new message.
    
    Returns: None
    """

    await event.reply("pong")


@client.on(events.NewMessage(pattern="get_ids", chats=[ADMIN_ID]))
async def handler(event):
    """
    This function is an event handler for new messages on Telegram that match a specific pattern. It listens for new messages that contain the text "get_ids" (specified in the 'pattern' parameter of the events.NewMessage() decorator) in a specific chat (specified in the 'chats' parameter of the events.NewMessage() decorator) and reply to the message with a list of chat titles and their corresponding ids.

    Parameters:
    - event (telegram.events.NewMessage): The event object containing metadata about the new message.

    Returns: None
    """
    message = ""
    async for dialog in client.iter_dialogs():
        message += f"-> `{dialog.title}` -> `{dialog.entity.id}`\n"
    await event.reply(message)


@client.on(events.NewMessage(pattern="get_config", chats=[ADMIN_ID]))
async def handler(event):
    """
    This function is an event handler for new messages on Telegram that match a specific pattern. It listens for new messages that contain the text "get_config" (specified in the 'pattern' parameter of the events.NewMessage() decorator) in a specific chat (specified in the 'chats' parameter of the events.NewMessage() decorator) and reply to the message with the current configuration in json format.

    Parameters:
    - event (telegram.events.NewMessage): The event object containing metadata about the new message.

    Returns: None
    """

    await event.reply(json.dumps(CONFIG, indent=4, ensure_ascii=False).encode('utf8').decode())


@client.on(events.NewMessage(pattern="help"))
async def handler(event):
    """
    This function is an event handler for new messages on Telegram that match a specific pattern. It listens for new messages that contain the text "help" (specified in the 'pattern' parameter of the events.NewMessage() decorator) and reply to the message with a list of available commands and contact info. The reply will be different for regular users and admin users.

    Parameters:
    - event (telegram.events.NewMessage): The event object containing metadata about the new message.

    Returns: None
    """

    message = '''\
Ping: `ping`
Help: `help`
--------------------
Contact: @grablevski
'''
    message_admin = '''
--- ADMIN ---
Show ids: `get_ids`
Show config: `get_config`
--- ADMIN --- \n
''' + message

    peer = event.message.peer_id
    if isinstance(peer, PeerUser) and peer.user_id == ADMIN_ID:
        await event.reply(message_admin)
    else:
        await event.reply(message)


def main():
    logging.info('Started!')
    client.start()
    client.run_until_disconnected()


if __name__ == '__main__':
    main()
