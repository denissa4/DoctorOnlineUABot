from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, ConversationState
from botbuilder.schema import ChannelAccount, Attachment, Activity, ActivityTypes
from .ConversationData import ConversationData
from views import *
import traceback


class Bot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState):
        self.conversation_state = conversation_state
        self.conversation_data_accessor = self.conversation_state.create_property("ConversationData")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)
        await self.conversation_state.save_changes(turn_context, False)

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                hello_msg = "Продовжуючи користуватись ботом ви погоджуєтесь з " \
                            "[правилами користування](https://doctoronline.bsmu.edu.ua/terms) та " \
                            "[політикою конфіденційності](https://doctoronline.bsmu.edu.ua/privacy) сервісу."
                await turn_context.send_activity(hello_msg)
                zero_stage = ("Дитячі Лікарі", "Дорослі лікарі", "Псих. допомога")
                await zero_stage_funct(zero_stage, turn_context)
                return web.Response(status=200)

    async def on_message_activity(self, turn_context: TurnContext):
        try:
            try:
                conversation_data = await self.conversation_data_accessor.get(turn_context, ConversationData)
                return await dialog_view(turn_context, conversation_data)
            except Exception:
                var = traceback.format_exc()
                print(var)
                response = "Трапилась помилка, спробуйте пізніше"
                await turn_context.send_activity(response)

        except KeyError:
            pass
