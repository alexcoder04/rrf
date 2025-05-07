#!/usr/bin/env python3

from rrfbot import RRFBot
import asyncio


if __name__ == "__main__":
    bot = RRFBot()
    asyncio.run(bot.run())

