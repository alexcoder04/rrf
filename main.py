#!/usr/bin/env python3

from handlers import start, free, freeat, where
import log
import message_templates

import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)


should_shutdown = asyncio.Event()


# in this file because of the should_shutdown variable
async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.call("shutdown", update.effective_user.id)
    if update.effective_user.id != int(open("./data/root").read()):
        await update.message.reply_text(message_templates.SHUTDOWN_DENIED)
        return

    await update.message.reply_text(message_templates.SHUTDOWN_SUCCESS)
    should_shutdown.set()


async def main():
    application = ApplicationBuilder().token(open("./data/token").read().strip()).build()

    await application.initialize()
    await application.start()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("free", free))
    application.add_handler(CommandHandler("freeat", freeat))
    application.add_handler(CommandHandler("where", where))
    application.add_handler(CommandHandler("shutdown", shutdown))

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

