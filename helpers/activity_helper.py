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
                          title="Як це пряцює",
                          value="https://doctoronline.bsmu.edu.ua/#how-it-works"),
               CardAction(type=ActionTypes.open_url,
                          title="Часті запитання",
                          value="https://doctoronline.bsmu.edu.ua/#faq"),
               ]
    # here in place of `hero` you can specify `thumbnail` to send thumnail card.
    attachments = await create_hero_card('', buttons,
                                         text="Виберіть що вам потрібно")
    response = MessageFactory.carousel([attachments], text=None)

    return response


async def create_hero_card(title, buttons, images=None, subtitle=None, text=None):
    card = HeroCard(title=title,
                    subtitle=subtitle,
                    text=text,
                    images=images,
                    buttons=buttons,
                    )
    return CardFactory.hero_card(card)
