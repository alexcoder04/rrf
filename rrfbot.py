
# local imports {{{
from logger import Logger
from rb_api import Time, Room
import templates
# }}}

# library imports {{{
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from time import monotonic, sleep
import asyncio
import os
# }}}


class RRFBot:
    # settings {{{
    WEEKDAYS = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    WEEKDAYS_REV = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    CACHE_LIFETIME = 12 # hours
    REQUEST_DELAY = 1 # seconds
    # }}}

    # init, run, shutdown {{{
    def __init__(self, data_dir: str = "./data") -> None:
        self.data_dir = os.path.realpath(data_dir)
        self.started = datetime.now()
        self.log = Logger(os.path.join(self.data_dir, self.started.strftime("log-%Y%m%d%H%M%S")))
        self.app = ApplicationBuilder().token(self.read_file("token")).build()
        self.active = asyncio.Event()
        self.root = self.read_file("root")
        self.hostname = self.get_hostname()
        self.cache = {}

    async def run(self) -> None:
        await self.app.initialize()
        await self.app.start()

        self.app.add_handler(CommandHandler("start", self.c_start))
        self.app.add_handler(CommandHandler("free", self.c_free))
        self.app.add_handler(CommandHandler("freeat", self.c_freeat))
        self.app.add_handler(CommandHandler("shutdown", self.c_shutdown))
        self.app.add_handler(CommandHandler("system", self.c_system))

        await self.app.updater.start_polling(
            allowed_updates=Update.MESSAGE,
            drop_pending_updates=True
        )
        self.log.info("Application started successfully, waiting for commands...")

        await self.active.wait()
        await self.shutdown()

    async def shutdown(self) -> None:
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
    # }}}

    # handler: shutdown {{{
    async def c_shutdown(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.log.call("shutdown", update.effective_user.id)

        if not self.is_root(update.effective_user.id):
            await update.message.reply_text(templates.shutdown.denied)
            return

        await update.message.reply_text(templates.shutdown.progress)
        self.active.set()
    # }}}

    # handler: system {{{
    async def c_system(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            self.log.call("system", update.effective_user.id)
            if not self.is_root(update.effective_user.id):
                await update.message.reply_text(templates.system.denied)
                return

            await update.message.reply_text(templates.system.info.format(
                started=self.started.strftime("%Y-%m-%d_%H:%M:%S"),
                user=update.effective_user.id,
                host=self.hostname,
                log="".join(self.log.tail(10))
            ))
        except Exception as e:
            self.log.error(e)
            await update.message.reply_text(templates.error.format(command="system"))
    # }}}

    # handler: start {{{
    async def c_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.log.call("start", update.effective_user.id)
        await update.message.reply_text(templates.start.greeting)
    # }}}

    # handler: free {{{
    async def c_free(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            self.log.call("free", update.effective_user.id)
            now = datetime.now()

            if now.weekday() in (5, 6):
                await update.message.reply_text(templates.free.weekend)
                return

            await self.display_free(update, context, now.weekday(), Time(now.hour, now.minute))
        except Exception as e:
            self.log.error(e)
            await update.message.reply_text(templates.error.format(command="free"))
    # }}}

    # handler: freeat {{{
    async def c_freeat(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.log.call("freeat", update.effective_user.id)

        if not context.args or len(context.args) < 2:
            await update.message.reply_text(templates.freeat.missing_args)
            return

        try:
            day = self.WEEKDAYS[context.args[0]]
            hour = int(context.args[1].split(":")[0])
            minute = int(context.args[1].split(":")[1])
        except (KeyError, ValueError, IndexError):
            await update.message.reply_text(templates.freeat.invalid_args)
            return

        try:
            if datetime.now().weekday() > day:
                await update.message.reply_text(templates.freeat.passed_day)

            await self.display_free(update, context, day, Time(hour, minute))
        except Exception as e:
            self.log.error(e)
            await update.message.reply_text(templates.error.format(command="freeat"))
    # }}}

    # disp free general {{{
    async def display_free(self, update: Update, context: ContextTypes.DEFAULT_TYPE, day: int, time: Time) -> None:
        await update.message.reply_text(templates.free.init.format(day=self.WEEKDAYS_REV[day], hour=time.hour, minute=time.minute))

        check_start = monotonic()

        room_ids = self.read_db()
        rooms = []
        for rid in room_ids:
            room = await self.check_room(rid)

            if room is None or not room.loaded:
                continue

            if room.minutes_left(day, time) is not None:
                rooms.append((room, room.minutes_left(day, time)))
        
        duration = monotonic() - check_start

        if len(rooms) == 0:
            await update.message.reply_text(templates.free.no_found.format(number=len(room_ids), duration=duration))
            return

        roomslist_message = "\n".join([f"{r[0].html_disp()} free for {r[1]} more minutes." for r in sorted(rooms, key=lambda r: r[1])])
        await update.message.reply_text(templates.free.list_.format(number=len(room_ids), duration=duration) + roomslist_message, parse_mode="HTML")
    # }}}

    # check_room with cache {{{
    async def check_room(self, rid: int) -> Room:
        if rid in self.cache and datetime.now() - self.cache[rid].loadtime < timedelta(hours=self.CACHE_LIFETIME):
            return self.cache[rid]

        await asyncio.sleep(self.REQUEST_DELAY)

        room = Room(rid)
        if not room.loaded:
            return None

        self.cache[rid] = room
        return room
    # }}}

    # helper functions {{{
    def is_root(self, user: int) -> None:
        return self.root == str(user)

    def read_db(self) -> list:
        import csv
        room_ids = []
        with open(os.path.join(self.data_dir, "roomdb.csv"), mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                room_ids.append(int(row["rb_id"]))
        return room_ids

    def read_file(self, filename: str) -> str:
        with open(os.path.join(self.data_dir, filename), "r") as f:
            return f.read().strip()

    def get_hostname(self) -> str:
        with open("/etc/hostname", "r") as f:
            return f.read().strip()
    # }}}

