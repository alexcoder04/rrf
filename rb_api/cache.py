from datetime import datetime, timedelta
from time import sleep
from .room import Room


REQUEST_DELAY = 0.5
CACHE_LIFETIME = 12 # hours


cache = {}


def get_room_data(rb_id: int) -> Room:
    if rb_id in cache and datetime.now() - cache[rb_id].loadtime < timedelta(hours=CACHE_LIFETIME):
        return cache[rb_id]

    sleep(REQUEST_DELAY)

    room = Room(rb_id)
    if not room.loaded:
        return None

    cache[rb_id] = room
    return room

