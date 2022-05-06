from botbuilder.dialogs import DialogTurnResult, ComponentDialog, DialogContext, DialogTurnStatus
from botbuilder.core import BotFrameworkAdapter
from botbuilder.schema import ActivityTypes
from helpers.activity_helper import create_help_activity


class LogoutDialog(ComponentDialog):
    def __init__(self, dialog_id: str, connection_name: str):
        super(LogoutDialog, self).__init__(dialog_id)

        self.connection_name = connection_name

    async def on_begin_dialog(self, inner_dc: DialogContext, options: object) -> DialogTurnResult:
        result = await self._interrupt(inner_dc)
        if result:
            return result
        return await super().on_begin_dialog(inner_dc, options)

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        result = await self._interrupt(inner_dc)
        if result:
            return result
        return await super().on_continue_dialog(inner_dc)

    async def _interrupt(self, inner_dc: DialogContext):
        if inner_dc.context.activity.type == ActivityTypes.message:
            text = inner_dc.context.activity.text.lower().strip()
            if text in ["logout", "вийти", "вихід"]:
                bot_adapter: BotFrameworkAdapter = inner_dc.context.adapter
                await bot_adapter.sign_out_user(inner_dc.context, self.connection_name)
                await inner_dc.context.send_activity("Ви вийшли з облікового запису.")
                return await inner_dc.cancel_all_dialogs()
            elif text in ["help", "?", "допомога"]:
                help_message = await create_help_activity()
                await inner_dc.context.send_activity(help_message)
                return DialogTurnResult(DialogTurnStatus.Waiting)
        return None
