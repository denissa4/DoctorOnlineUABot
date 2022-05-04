#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
import sys
import traceback
from datetime import datetime
from http import HTTPStatus
import asyncio
import os

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState, TurnContext,
                             MemoryStorage,
                             UserState)
from bots import Bot
from dialogs import MainDialog

# Bot App Credentials
APP_ID = os.getenv('AppId', '')
APP_PASSWORD = os.getenv('AppPassword', '')
CONNECTION_NAME = os.environ.get("ConnectionName", "")
# Configuration
PORT = 8000

# Create adapter.
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}")
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )

    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)

ADAPTER.on_turn_error = on_error

# Create MemoryStorage and state
MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

# Create dialog
DIALOG = MainDialog(CONNECTION_NAME)

# Create Bot
BOT = Bot(CONVERSATION_STATE, USER_STATE, DIALOG)


async def messages(request: Request) -> Response:
    if "application/json" in request.headers["Content-Type"]:
        body = await request.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    activity = Activity().deserialize(body)
    print("[DoctorOnlineUABot]: ", body)
    auth_header = request.headers['Authorization'] if 'Authorization' in request.headers else ''
    if activity.type != 'typing':
        response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        if response:
            return json_response(data=response.body, status=response.status)
        return Response(status=HTTPStatus.OK)


APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == '__main__':
    try:
        web.run_app(APP, host="0.0.0.0", port=PORT)
    except Exception as error:
        raise error
