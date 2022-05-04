from botbuilder.core import MessageFactory, CardFactory
from botbuilder.schema import (
    Activity,
    CardAction,
    ActionTypes,
    HeroCard
)


async def create_help_activity_reply():
    buttons = [CardAction(type=ActionTypes.open_url,
                          title="Правила користування",
                          value="https://doctoronline.bsmu.edu.ua/terms"),
               CardAction(type=ActionTypes.open_url,
                          title="Політика конфіденційності",
                          value="https://doctoronline.bsmu.edu.ua/privacy"),
               CardAction(type=ActionTypes.open_url,
                          title="Як це працює",
                          value="https://doctoronline.bsmu.edu.ua/#how-it-works"),
               CardAction(type=ActionTypes.open_url,
                          title="Часті запитання",
                          value="https://doctoronline.bsmu.edu.ua/#faq"),
               ]
    # here in place of `hero` you can specify `thumbnail` to send thumnail card.
    attachments = await create_hero_card('', buttons,
                                         text="Виберіть що вам потрібно")
    return MessageFactory.carousel([attachments], text=None)


async def create_welcome_activity():
    attachments = await create_adaptive_card()
    return MessageFactory.carousel([attachments], text=None)


async def create_adaptive_card():
    card = {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "Ласкаво просимо до **DoctorOnlineInUA** бота. "
                                "Напишіть _вийти_ щоб вийти. "
                                "Напишіть _допомога_ щоб отримати більше інформації. "
                                "Продовжуючи користуватись ботом ви погоджуєтесь з [правилами користування](https://doctoronline.bsmu.edu.ua/terms) та [політикою конфіденційності](https://doctoronline.bsmu.edu.ua/privacy) сервісу.",
                        "wrap": True
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Почати",
                        "data": {
                                    "msteams": {
                                        "type": "messageBack",
                                        "displayText": "Почати",
                                        "text": "Почати",
                                    }
                                  }
                    },
                    {
                        "type": "Action.Submit",
                        "title": "Отримати більше інформації",
                        "data": {
                                    "msteams": {
                                        "type": "messageBack",
                                        "displayText": "Допомога",
                                        "text": "Допомога",
                                    }
                                  }
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3"
            }
    return CardFactory.adaptive_card(card)


async def create_hero_card(title, buttons, images=None, subtitle=None, text=None):
    card = HeroCard(title=title,
                    subtitle=subtitle,
                    text=text,
                    images=images,
                    buttons=buttons,
                    )
    return CardFactory.hero_card(card)
