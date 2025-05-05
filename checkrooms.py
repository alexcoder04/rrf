
from rb_api import read_roomdb, get_room_data, Time
from time import monotonic


def checkrooms(day: int, time: Time):
    start = monotonic()

    room_ids = read_roomdb("./data/roomdb.csv")
    rooms = []
    for rid in room_ids:
        r = get_room_data(rid)

        if not r.loaded:
            print(f"room {rid} could not be loaded")
            continue

        free = r.minutes_left(day, time)
        if free is not None:
            rooms.append((r, free))

    return rooms, len(room_ids), monotonic() - start
