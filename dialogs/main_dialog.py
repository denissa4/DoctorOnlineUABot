from botbuilder.core import MessageFactory
from typing import List
from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    PromptOptions,
)
from botbuilder.dialogs.prompts import OAuthPrompt, OAuthPromptSettings, ConfirmPrompt, ChoicePrompt
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.dialogs.dialog_reason import DialogReason

from dialogs import LogoutDialog
from views import *

zero_stage = ("Дитячі Лікарі", "Дорослі лікарі", "Псих. допомога")

childs_doc = ["Алергологія",
              "Анестезіологія",
              "Гастроентерологія",
              "Гінекологія",
              "Дерматовенерологія",
              "Ендокринологія",
              "Імунологія",
              "Інфекційні хвороби",
              "Неврологія",
              "Неонатологія",
              "Пульмонологія",
              "Педіатрія",
              "Сімейна медицина",
              "Стоматологія"]

childs_url = ({"20": "https://calendly.com/d/cq9-29s-v8j/20"},  # Алергологія
              {"20": "https://calendly.com/d/cq5-jx7-n2w/20"},  # Анестезіологія
              {"20": "https://calendly.com/d/crw-y24-cqq/20"},  # Гастроентерологія
              {"20": "https://calendly.com/d/cq9-zq3-x5b/20"},  # Гінекологія
              {"20": "https://calendly.com/d/cn6-8zy-yf4/20"},  # Дерматовенерологія
              {"20": "https://calendly.com/d/crr-h6k-3mk/20"},  # Ендокринологія
              {"20": "https://calendly.com/d/crw-p9h-4qw/20"},  # Імунологія
              {"20": "https://calendly.com/d/crx-569-kd6/20"},  # Інфекційні хвороби
              {"20": "https://calendly.com/d/cpc-rjv-ytp/20"},  # Неврологія
              {"20": "https://calendly.com/d/cq4-frw-5dc/20"},  # Неонатологія
              {"20": "https://calendly.com/d/cq9-29q-zyv/20"},  # Пульмонологія
              {"20": "https://calendly.com/d/cnq-n2j-n38/20"},  # Педіатрія
              {"20": "https://calendly.com/d/cq8-v2z-ttb/20"},  # Сімейна медицина
              {"20": "https://calendly.com/d/crr-np9-rdg/20"},)  # Стоматологія
childs_url = dict(zip(childs_doc, childs_url))
adults_doc = ["Акушерство і гінекологія",
              "Гастроентерологія",
              "Дерматовенерологія",
              "Дієтологія",
              "Ендокринологія",
              "Інфекційні хвороби",
              "Кардіологія",
              "Неврологія",
              "Нефрологія",
              "Отоларингологія",
              "Онкологія",
              "Пульмонологія",
              "Ревматологія",
              "Сімейна медицина",
              "Стоматологія",
              "Терапія",
              "Урологія",
              "Фтизіатрія",
              "Хірургія",
              "Проф патологія",
              "Інше"]

surgery_doc = ("Проктологія", "Судинна хірургія", "Загальна хірургія")
surgery_url = ({"20": "https://calendly.com/d/cn7-27p-v5f/20"},  # "Проктологія"
               {"20": "https://calendly.com/d/cq8-8dz-wmn/20"},  # "Судинна хірургія"
               {"20": "https://calendly.com/d/cq5-jk9-m6f/20"},  # "Загальна хірургія"
               )
surgery_url = dict(zip(surgery_doc, surgery_url))
adults_url = ({"20": "https://calendly.com/d/cnk-8hp-drx/20"},  # Акушерство і гінекологія
              {"20": "https://calendly.com/d/cn7-43v-mdp/20"},  # "Гастроентерологія"
              {"20": "https://calendly.com/d/crq-8s4-fkf/20"},  # "Дерматовенерологія"
              {"20": "https://calendly.com/d/cpd-mf6-v32/20"},  # Дієтологія
              {"20": "https://calendly.com/d/crb-cg6-qw3/20"},  # Ендокринологія
              {"20": "https://calendly.com/d/cnr-y6d-f8s/20"},  # "Інфекційні хвороби"
              {"20": "https://calendly.com/d/crw-yzy-38f/20"},  # "Кардіологія"
              {"20": "https://calendly.com/d/cnq-xx8-k2f/20"},  # "Неврологія"
              {"20": "https://calendly.com/d/cpd-v78-t79/20"},  # "Нефрологія"
              {"20": "https://calendly.com/d/cn8-7gr-bsx/20"},  # "Отоларингологія"
              {"20": "https://calendly.com/d/crr-h67-hwb/20"},  # "Онкологія"
              {"20": "https://calendly.com/d/cn6-9ns-wd2/20"},  # "Пульмонологія"
              {"20": "https://calendly.com/d/cnj-5dn-mkz/20"},  # "Ревматологія"
              {"20": "https://calendly.com/d/cq8-v2z-ttb/20"},  # "Сімейна медицина"
              {"20": "https://calendly.com/d/cpd-tcw-rkr/20"},  # "Стоматологія"
              {"20": "https://calendly.com/d/crs-f5r-qtk/20"},  # "Терапія"
              {"20": "https://calendly.com/d/cn7-42v-8xm/20"},  # "Урологія"
              {"20": "https://calendly.com/d/cn8-dzy-b55/20"},  # "Фтизіатрія"
              surgery_url,  # "Хірургія"
              {"20": "https://calendly.com/d/cnm-kwq-zvc/20"},  # "Проф патологія"
              {"20": "https://calendly.com/d/cq8-v2z-ttb/20"},)  # "Інше"

adults_url = dict(zip(adults_doc, adults_url))

psychology_doc = ["Дитяча та підліткова психологія",
                  "Психіатр / Наркологія",
                  "Перша психологічна допомога",
                  "Психіатрія",
                  "Психологія / Психотерапія",
                  "Сексолог"]

psychology_url = ({"20": "https://calendly.com/d/cq4-gfs-f2t/20"},  # Дитяча та підліткова психологія
                  {"20": "https://calendly.com/d/cpc-p6q-6f3/20"},  # Психіатр / Наркологія
                  {"20": "https://calendly.com/d/cnk-dqc-wmt/20"},  # Перша психологічна допомога
                  {"20": "https://calendly.com/d/crw-sv8-26b/20"},  # Психіатрія
                  {"20": "https://calendly.com/d/cnk-htg-8vy/20"},  # Психологія / Психотерапія
                  {"20": "https://calendly.com/d/crx-tzn-35n/20"})  # Сексолог

psychology_url = dict(zip(psychology_doc, psychology_url))
url_dict = {"Дитячі Лікарі": childs_url, "Дорослі лікарі": adults_url, "Псих. допомога": psychology_url}
first_stage = {"Дитячі Лікарі": childs_doc, "Дорослі лікарі": adults_doc, "Псих. допомога": psychology_doc}


class MainDialog(LogoutDialog):
    def __init__(self, connection_name: str):
        super(MainDialog, self).__init__(MainDialog.__name__, connection_name)
        self.history = []
        self.add_dialog(
            OAuthPrompt(
                OAuthPrompt.__name__,
                OAuthPromptSettings(
                    connection_name=connection_name,
                    text="Будь ласка, увійдіть",
                    title="Увійти",
                    timeout=300000,
                ),
            )
        )
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.prompt_step,
                    self.login_step,
                    self.phase1,
                    self.phase2,
                    self.phase3,
                    self.phase4,
                    self.phase5,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def prompt_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.begin_dialog(OAuthPrompt.__name__)

    async def login_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Get the token from the previous step. Note that we could also have gotten the
        # token directly from the prompt itself. There is an example of this in the next method.
        if step_context.result:
            await step_context.context.send_activity("Ви ввійшли в систему.")
            hello_msg = "Продовжуючи користуватись ботом ви погоджуєтесь з " \
                        "[правилами користування](https://doctoronline.bsmu.edu.ua/terms) та " \
                        "[політикою конфіденційності](https://doctoronline.bsmu.edu.ua/privacy) сервісу."
            options = ["Так", "Ні"]
            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(hello_msg),
                    choices=self._to_choices(options),
                ),
            )

        await step_context.context.send_activity(
            "Login was not successful please try again."
        )
        return await step_context.end_dialog()

    async def phase1(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        choice: FoundChoice = step_context.result
        if choice.value == 'Так':
            self.history.append(choice.value)
            options = ["Дитячі Лікарі", "Дорослі лікарі", "Псих. допомога"]
            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Виберіть необхідну категорію"),
                    choices=self._to_choices(options),
                ),
            )

        return await step_context.end_dialog()

    async def phase2(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        choice: FoundChoice = step_context.result
        if choice.value:
            self.history.append(choice.value)
            options = first_stage.get(choice.value).copy()
            options.append("Назад")
            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Виберіть необхідну категорію"),
                    choices=self._to_choices(options),
                ),
            )

    async def phase3(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        choice: FoundChoice = step_context.result
        first_choice = first_stage.get(self.history[1])
        if choice.value == 'Назад':
            # len(history) >= 2
            self.history.pop()
            previous_choice = self.history.pop()
            dialog: WaterfallDialog = await self.find_dialog(step_context.active_dialog.id)
            state = step_context.active_dialog.state
            return await dialog.run_step(step_context, state['stepIndex'] - 2, DialogReason.ReplaceCalled, Choice(value=previous_choice))

        elif choice.value in first_choice:
            url_dict_in_stage = url_dict.get(self.history[-1])
            self.history.append(choice.value)
            if choice.value == "Хірургія":
                res_urls = url_dict_in_stage.get("Хірургія")
                options = list(res_urls.keys()).copy()
                options.append("Назад")
                return await step_context.prompt(
                    ChoicePrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Виберіть необхідну категорію"),
                        choices=self._to_choices(options),
                    ),
                )
            else:
                res_urls = url_dict_in_stage.get(choice.value)
                response = await create_finish_buttons(res_urls, "msteams", back=False)
                return await step_context.prompt(
                    ChoicePrompt.__name__,
                    PromptOptions(
                        prompt=response,
                        choices=self._to_choices(["Назад"]),
                    ),
                )

        else:
            return await step_context.end_dialog()

    async def phase4(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        choice: FoundChoice = step_context.result
        if choice.value == 'Назад':
            # len(history) >= 2
            self.history.pop()
            previous_choice = self.history.pop()
            dialog: WaterfallDialog = await self.find_dialog(step_context.active_dialog.id)
            state = step_context.active_dialog.state
            return await dialog.run_step(step_context, state['stepIndex'] - 2, DialogReason.ReplaceCalled,
                                         Choice(value=previous_choice))

        elif choice.value in surgery_doc:
            self.history.append(choice.value)
            res_urls = surgery_url.get(choice.value)
            response = await create_finish_buttons(res_urls, "msteams", back=False)
            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=response,
                    choices=self._to_choices(["Назад"]),
                ),
            )
        else:
            return await step_context.end_dialog()

    async def phase5(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        choice: FoundChoice = step_context.result
        if choice.value == 'Назад':
            # len(history) >= 2
            self.history.pop()
            previous_choice = self.history.pop()
            dialog: WaterfallDialog = await self.find_dialog(step_context.active_dialog.id)
            state = step_context.active_dialog.state
            return await dialog.run_step(step_context, state['stepIndex'] - 2, DialogReason.ReplaceCalled,
                                         Choice(value=previous_choice))
        else:
            return await step_context.end_dialog()

    def _to_choices(self, choices: [str]) -> List[Choice]:
        choice_list: List[Choice] = []
        for choice in choices:
            choice_list.append(Choice(value=choice))
        return choice_list

    async def _phase_generator(self, step_context: WaterfallStepContext, choice: Choice, options: List):
        choice: FoundChoice = step_context.result

        if choice.value == 'Назад':
            dialog: WaterfallDialog = await self.find_dialog(step_context.active_dialog.id)
            state = step_context.active_dialog.state
            return await dialog.run_step(step_context, state['stepIndex'] - 2, DialogReason.ReplaceCalled,
                                         choice)
        else:
            options = ["Назад"]
            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Виберіть необхідну категорію"),
                    choices=self._to_choices(options),
                ),
            )
