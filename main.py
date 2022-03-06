#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
import ssl
from botbuilder.schema import Activity
from aiohttp import web
import asyncio
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState, MemoryStorage)
from bots import Bot
import os
import traceback
import argparse


# Bot App Credentials
APP_ID = os.getenv('AppId', '')
APP_PASSWORD = os.getenv('AppPassword', '')
# Configuration
PORT = 8000
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)
memory = MemoryStorage()
CONVERSATION_STATE = ConversationState(memory)
BOT = Bot(CONVERSATION_STATE)


async def messages(request) -> web.Response:
    if "application/json" in request.headers["Content-Type"]:
        body = await request.json()
    else:
        return web.Response(status=415)
    activity = Activity().deserialize(body)
    auth_header = request.headers['Authorization'] if 'Authorization' in request.headers else ''
    try:
        if activity.type != 'typing':
            await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        return web.Response(status=201)
    except Exception as e:
        var = traceback.format_exc()
        print(var)


async def init_app():
    APP = web.Application()
    APP.add_routes([web.post('/api/messages', messages)])

    return APP


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        app = loop.run_until_complete(init_app())
        web.run_app(app, host='0.0.0.0', port=PORT)
    except Exception as e:
        print("App error:", e)
