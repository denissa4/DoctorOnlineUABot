# -*- coding: utf-8 -*-

from botbuilder.core import TurnContext, MessageFactory, CardFactory
from botbuilder.schema import (Attachment, Activity, ActivityTypes, CardAction, ActionTypes,
                               HeroCard, CardImage)
from aiohttp import web
import os


async def create_typing_activity(request_activity: Activity) -> Activity:
    activity = Activity(
        type=ActivityTypes.typing,
        channel_id=request_activity.channel_id,
        conversation=request_activity.conversation,
        recipient=request_activity.from_property,
        from_property=request_activity.recipient,
        attachment_layout='carousel',
        text='',
        service_url=request_activity.service_url)

    return activity


async def create_buttons(buttons_name, channel, back=True):
    buttons = []
    if channel == 'msteams':
        postback = ActionTypes.im_back
    else:
        postback = ActionTypes.post_back
    async for word in words(buttons_name):
        button = CardAction(type=postback,
                            title="{}".format(word),
                            value=word)
        buttons.append(button)
    # =====================================================
    if back:
        button_back = CardAction(type=postback,
                                title="Назад",
                                value="Назад")
        buttons.append(button_back)
    attachments = create_hero_card('', buttons,
                                   text="Виберіть необхідну категорію")
    attachments = MessageFactory.carousel([attachments], text=None)
    return attachments


async def create_finish_buttons(buttons_name: dict, channel):
    buttons = []
    if channel == 'msteams':
        postback = ActionTypes.im_back
    else:
        postback = ActionTypes.post_back
    button = CardAction(type=ActionTypes.open_url,
                        title="20хв",
                        value=buttons_name.get('20'))
    buttons.append(button)
    # =====================================================
    button_back = CardAction(type=postback,
                            title="Назад",
                            value="Назад")
    buttons.append(button_back)
    attachments = create_hero_card('', buttons,
                                   text="Забронювати зустріч на")
    attachments = MessageFactory.carousel([attachments], text=None)
    return attachments


def create_hero_card(title, buttons, images=None, subtitle=None, text=None) -> Attachment:
    card = HeroCard(title=title,
                    subtitle=subtitle,
                    text=text,
                    images=images,
                    buttons=buttons,
                    )
    return CardFactory.hero_card(card)


async def zero_stage_funct(zero_stage, context):
    response = await create_buttons(zero_stage, context.activity.channel_id, back=False)
    await context.send_activity(response)


async def first_stage_func(conversation_data, context, first_stage):
    conversation_data.numeric_stage = 1
    response = await create_buttons(first_stage.get(conversation_data.stage), context.activity.channel_id)
    await context.send_activity(response)


async def second_stage_func(conversation_data, context, url_dict):
    conversation_data.numeric_stage = 2
    url_dict_in_stage = url_dict.get(conversation_data.stage)
    if context.activity.text == "Хірургія" or conversation_data.third_stage == "Хірургія":
        res_urls = url_dict_in_stage.get("Хірургія")
        response = await create_buttons(list(res_urls.keys()), context.activity.channel_id)
    else:
        conversation_data.third_stage = ""
        res_urls = url_dict_in_stage.get(context.activity.text)
        response = await create_finish_buttons(res_urls, context.activity.channel_id)
    await context.send_activity(response)


async def third_stage_func(conversation_data, context, surgery_url):
    conversation_data.numeric_stage = 3
    conversation_data.third_stage = "Хірургія"
    res_urls = surgery_url.get(context.activity.text)
    response = await create_finish_buttons(res_urls, context.activity.channel_id)
    await context.send_activity(response)


async def dialog_view(context: TurnContext, conversation_data) -> web.Response:
    # Get response from nlsql API
    zero_stage = ("Дитячі Лікарі", "Дорослі лікарі", "Псих. допомога")

    childs_doc = ("Алергологія",
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
                  "Стоматологія")

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
    adults_doc = ("Акушерство і гінекологія",
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
                  "Інше")

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

    psychology_doc = ("Дитяча та підліткова психологія",
                      "Психіатр / Наркологія",
                      "Перша психологічна допомога",
                      "Психіатрія",
                      "Психологія / Психотерапія",
                      "Сексолог")

    psychology_url = ({"20": "https://calendly.com/d/cq4-gfs-f2t/20"},  # Дитяча та підліткова психологія
                      {"20": "https://calendly.com/d/cpc-p6q-6f3/20"},  # Психіатр / Наркологія
                      {"20": "https://calendly.com/d/cnk-dqc-wmt/20"},  # Перша психологічна допомога
                      {"20": "https://calendly.com/d/crw-sv8-26b/20"},  # Психіатрія
                      {"20": "https://calendly.com/d/cnk-htg-8vy/20"},  # Психологія / Психотерапія
                      {"20": "https://calendly.com/d/crx-tzn-35n/20"})  # Сексолог

    psychology_url = dict(zip(psychology_doc, psychology_url))
    url_dict = {"Дитячі Лікарі": childs_url, "Дорослі лікарі": adults_url, "Псих. допомога": psychology_url}
    first_stage = {"Дитячі Лікарі": childs_doc, "Дорослі лікарі": adults_doc, "Псих. допомога": psychology_doc}
    response = await create_typing_activity(context.activity)
    await context.send_activity(response)
    if context.activity.text in zero_stage:
        conversation_data.stage = context.activity.text
        await first_stage_func(conversation_data, context, first_stage)
    elif conversation_data.numeric_stage == 1 and context.activity.text in first_stage.get(conversation_data.stage):
        await second_stage_func(conversation_data, context, url_dict)
    elif conversation_data.numeric_stage == 2 and context.activity.text in surgery_doc:
        await third_stage_func(conversation_data, context, surgery_url)
    else:
        if context.activity.text.lower() == "назад":
            if conversation_data.numeric_stage == 3:
                conversation_data.numeric_stage = 2
                await second_stage_func(conversation_data, context, url_dict)
            elif conversation_data.numeric_stage == 2:
                conversation_data.numeric_stage = 1
                conversation_data.third_stage = ""
                await first_stage_func(conversation_data, context, first_stage)
            else:
                conversation_data.numeric_stage = 0
                conversation_data.stage = ""
                conversation_data.third_stage = ""
                await zero_stage_funct(zero_stage, context)
        else:
            conversation_data.numeric_stage = 0
            conversation_data.stage = ""
            await zero_stage_funct(zero_stage, context)

    return web.Response(status=200)


# for async cycle
async def words(word):
    for i in range(len(word)):
        yield word[i]
