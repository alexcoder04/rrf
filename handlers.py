
from checkrooms import checkrooms
from rb_api import Time
import log
import message_templates

from datetime import datetime
from time import sleep

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)


WEEKDAYS = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6
}

def build_response(rooms: list, checked: int, dur: float) -> str:
    roomslist = "\n".join([f"{r[0].html_disp()} free for {r[1]} more minutes." for r in rooms])
    return message_templates.FREEAT_RESP.format(number=checked, dur=dur) + roomslist


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.call("start", update.effective_user.id)
    await update.message.reply_text(message_templates.START)


async def freeat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.call("freeat", update.effective_user.id)

    if not context.args:
        await update.message.reply_text(message_templates.FREEAT_ERROR)
        return

    try:
        day = WEEKDAYS[context.args[0]]
    except KeyError:
        await update.message.reply_text(message_templates.FREEAT_INVALIDDAY.format(day=context.args[0]))
        return
    hour = int(context.args[1].split(":")[0])
    minute = int(context.args[1].split(":")[1])

    if datetime.now().weekday() > day:
        await update.message.reply_text(message_templates.FREEAT_WEEKEND)

    await update.message.reply_text(message_templates.FREEAT_START.format(
        day=context.args[0], hour=hour, minute=minute
        ))
    rooms, checked, dur = checkrooms(day, Time(hour, minute))
    if rooms is None or len(rooms) == 0:
        await update.message.reply_text(message_templates.FREEAT_NO.format(number=checked, dur=dur))
        return
    await update.message.reply_text(build_response(rooms, checked, dur), parse_mode="HTML")


async def free(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.call("free", update.effective_user.id)
    now = datetime.now()

    if now.weekday() in (5, 6):
        await update.message.reply_text(message_templates.FREE_WEEKEND)
        return

    await update.message.reply_text(message_templates.FREE_START.format(
            day=now.strftime("%a"),
            hour=now.hour,
            minute=now.minute
        ))
    rooms, checked, dur = checkrooms(now.weekday(), Time(now.hour, now.minute))
    if rooms is None or len(rooms) == 0:
        await update.message.reply_text(message_templates.FREE_NO.format(number=checked, dur=dur))
        return
    await update.message.reply_text(build_response(rooms, checked, dur), parse_mode="HTML")

async def where(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.call("where", update.effective_user.id)

    if not context.args:
        await update.message.reply_text(message_templates.WHERE_ERROR)
        return

    await update.message.reply_text(message_templates.WHERE_ANS.format(building=context.args[0]))

