from decouple import config

API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION", default=None) #pyro session
AUTH = config("AUTH", default=None, cast=int)

import os, asyncio, logging
from pyrogram import Client, filters, idle
from pyrogram.types import ChatJoinRequest
from pyrogram.errors import FloodWait, MessageNotModified

client = Client(
    session_name=SESSION, 
    api_hash=API_HASH, 
    api_id=API_ID)


logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    datefmt="[%d/%m/%Y %H:%M:%S]",
    format=" %(asctime)s - [INDOAPPROVEBOT] >> %(levelname)s << %(message)s",
    handlers=[logging.FileHandler("indoapprovebot.log"), logging.StreamHandler()])

@client.on_chat_join_request(filters.chat(chat_id))
async def approve(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        logging.info(f"Sleeping for {e.x + 2} seconds due to floodwaits!")
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)

@client.on_message(filters.user(AUTH))
async def alive(c, m):
    if m.text == '!alive':
        await m.reply_text("I'm alive!")

client.run()
