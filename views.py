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
    button = CardAction(type=ActionTypes.open_url,
                        title="40хв",
                        value=buttons_name.get('40'))
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
    res_urls = url_dict_in_stage.get(context.activity.text)
    response = await create_finish_buttons(res_urls, context.activity.channel_id)
    await context.send_activity(response)


async def dialog_view(context: TurnContext, conversation_data) -> web.Response:
    # Get response from nlsql API
    zero_stage = ("Для дітей", "Для дорослих", "Психологічна допомога")

    childs_doc = ("Алергологія", "Анестезіологія", "Гастроентерологія", "Гінекологія", "Імунологія",
                  "Неврологія", "Пульмонологія", "Інфекційні хвороби", "Сімейна медицина")

    childs_url = ({"20": "https://calendly.com/d/cq9-29s-v8j/20", "40": "https://calendly.com/d/cq9-3pn-zhs/40"},
                  {"20": "https://calendly.com/d/cq5-jx7-n2w/20", "40": "https://calendly.com/d/cnr-psn-zrg/40"},
                  {"20": "https://calendly.com/d/crw-y24-cqq/20", "40": "https://calendly.com/d/cq8-78q-55y/40"},
                  {"20": "https://calendly.com/d/cq9-zq3-x5b/20", "40": "https://calendly.com/d/crx-wr7-wb5/40"},
                  {"20": "https://calendly.com/d/crw-p9h-4qw/20", "40": "https://calendly.com/d/cnr-y3w-nwv/40"},
                  {"20": "https://calendly.com/d/cpc-rjv-ytp/20", "40": "https://calendly.com/d/crx-6k6-f2t/40"},
                  {"20": "https://calendly.com/d/cq9-29q-zyv/20", "40": "https://calendly.com/d/cn6-yht-bsw/40"},
                  {"20": "https://calendly.com/d/crx-569-kd6/20", "40": "https://calendly.com/d/cpd-jcv-xp5/40"},
                  {"20": "https://calendly.com/d/cq8-v2z-ttb/20", "40": "https://calendly.com/d/crw-2v9-ksp/40"},)
    childs_url = dict(zip(childs_doc, childs_url))
    adults_doc = ("Акушерство і гінекологія", "Гастроентерологія", "Дерматовенерологія", "Ендокринологія",
                  "Інфекційні хвороби", "Кардіологія", "Неврологія", "Неонатологія", "Нефрологія",
                  "Педіатрія", "Проктологія", "Пульмонологія", "Ревматологія", "Сімейна медицина",
                  "Судинна хірургія", "Терапія", "Урологія", "Хірургічна стоматологія",
                  "Хірургія", "Інше")

    adults_url = ({"20": "https://calendly.com/d/cnk-8hp-drx/20", "40": "https://calendly.com/d/crx-4r6-zwj/40"},
                  {"20": "https://calendly.com/d/cn7-43v-mdp/20", "40": "https://calendly.com/d/cnr-y22-g7k/40"},
                  {"20": "https://calendly.com/d/crq-8s4-fkf/20", "40": "https://calendly.com/d/crw-3jb-8wv/40"},
                  {"20": "https://calendly.com/d/crb-cg6-qw3/20", "40": "https://calendly.com/d/cq5-mdj-mg8/40"},
                  {"20": "https://calendly.com/d/cnr-y6d-f8s/20", "40": "https://calendly.com/d/cnr-2n6-65r/40"},
                  {"20": "https://calendly.com/d/crw-yzy-38f/20", "40": "https://calendly.com/d/crs-cjh-mn2/40"},
                  {"20": "https://calendly.com/d/cnq-xx8-k2f/20", "40": "https://calendly.com/d/cpc-g4x-562/40"},
                  {"20": "https://calendly.com/d/cq4-frw-5dc/20", "40": "https://calendly.com/d/cpd-vsf-7rh/40"},
                  {"20": "https://calendly.com/d/cpd-v78-t79/20", "40": "https://calendly.com/d/crs-f5g-7w6/40"},
                  {"20": "https://calendly.com/d/cnq-n2j-n38/20", "40": "https://calendly.com/d/cnm-mc4-stz/40"},
                  {"20": "https://calendly.com/d/cn7-27p-v5f/20", "40": "https://calendly.com/d/cn6-xz6-wgv/40"},
                  {"20": "https://calendly.com/d/cn6-9ns-wd2/20", "40": "https://calendly.com/d/cnr-y24-x4t/40"},
                  {"20": "https://calendly.com/d/cnj-5dn-mkz/20", "40": "https://calendly.com/d/cpc-d9v-mrz/40"},
                  {"20": "https://calendly.com/d/cq8-v2z-ttb/20", "40": "https://calendly.com/d/crw-2v9-ksp/40"},
                  {"20": "https://calendly.com/d/cq8-8dz-wmn/20", "40": "https://calendly.com/d/cn7-5n5-zdt/40"},
                  {"20": "https://calendly.com/d/crs-f5r-qtk/20", "40": "https://calendly.com/d/cq8-whs-p8f/40"},
                  {"20": "https://calendly.com/d/cn7-42v-8xm/20", "40": "https://calendly.com/d/crw-3hd-vrk/40"},
                  {"20": "https://calendly.com/d/crb-cmq-9cr/20", "40": "https://calendly.com/d/cnm-kwh-3dj/40"},
                  {"20": "https://calendly.com/d/cq5-jk9-m6f/20", "40": "https://calendly.com/d/cq5-tct-zwc/40"},
                  {"20": "https://calendly.com/d/cqx-v9y-pfw/20", "40": "https://calendly.com/d/cqx-v9y-pfw/20"},)
    adults_url = dict(zip(adults_doc, adults_url))

    psychology_doc = ("Дитяча Медична психологія", "Перша психологічна допомога")

    psychology_url = ({"20": "https://calendly.com/d/cnq-k6m-9vz/20", "40": "https://calendly.com/d/cnk-93v-428/40"},
                      {"20": "https://calendly.com/d/cnk-dqc-wmt/20", "40": "https://calendly.com/d/cpd-vm8-kpz/40"})
    psychology_url = dict(zip(psychology_doc, psychology_url))
    url_dict = {"Для Дітей": childs_url, "Для Дорослих": adults_url, "Психологічна допомога": psychology_url}
    first_stage = {"Для Дітей": childs_doc, "Для Дорослих": adults_doc, "Психологічна допомога": psychology_doc}
    response = await create_typing_activity(context.activity)
    await context.send_activity(response)
    if context.activity.text in zero_stage:
        conversation_data.stage = context.activity.text
        await first_stage_func(conversation_data, context, first_stage)
    elif conversation_data.numeric_stage == 1 and context.activity.text in first_stage.get(conversation_data.stage):
        await second_stage_func(conversation_data, context, url_dict)
    else:
        if context.activity.text.lower() == "назад":
            if conversation_data.numeric_stage == 2:
                conversation_data.numeric_stage = 1
                await first_stage_func(conversation_data, context, first_stage)
            else:
                conversation_data.numeric_stage = 0
                conversation_data.stage = ""
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
