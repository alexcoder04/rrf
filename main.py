#!/usr/bin/env python3

from handlers import start, free, freeat
import log
import message_templates

import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)


should_shutdown = asyncio.Event()
script_start_time = datetime.now()


# in this file because of the should_shutdown variable
async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.call("shutdown", update.effective_user.id)
    if update.effective_user.id != int(open("./data/root").read()):
        await update.message.reply_text(message_templates.SHUTDOWN_DENIED)
        return

    await update.message.reply_text(message_templates.SHUTDOWN_SUCCESS)
    should_shutdown.set()


# in this file because of the script_start_time variable
async def system(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.call("system", update.effective_user.id)
    if update.effective_user.id != int(open("./data/root").read()):
        await update.message.reply_text(message_templates.SYSTEM_DENIED)
        return

    await update.message.reply_text(message_templates.SYSTEM_INFO.format(
        start=script_start_time.strftime("%Y-%m-%d_%H:%M:%S"),
        user=update.effective_user.id,
        host=open("/etc/hostname").read().strip()
        ))


async def main():
    application = ApplicationBuilder().token(open("./data/token").read().strip()).build()

    await application.initialize()
    await application.start()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("free", free))
    application.add_handler(CommandHandler("freeat", freeat))
    application.add_handler(CommandHandler("shutdown", shutdown))
    application.add_handler(CommandHandler("system", system))

    await application.updater.start_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
            )
    log.info("Application started successfully, waiting for commands...")

    await should_shutdown.wait()

    await application.updater.stop()
    await application.stop()
    await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

