from bs4 import BeautifulSoup
from .mytime import Time


class Block:
    def __init__(self, time_start, time_end, title, info):
        self.time_start = time_start
        self.time_end = time_end
        self.title = title
        self.info = info

    def __str__(self):
        return f"Time block at {self.time_start}-{self.time_end} - {self.title}"


def parse_block(div):
    header = div.find(class_="cocal-ev-header")
    header_spans = list(header.children)

    # no time - no real event
    time = header_spans[2].get_text(strip=True)
    if time == "":
        return None

    times = [i.strip() for i in time.split("-")]
    time_start = times[0].split(":")
    time_start = Time(int(time_start[0]), int(time_start[1]))
    time_end = times[1].split(":")
    time_end = Time(int(time_end[0]), int(time_end[1]))

    title = header_spans[3].get_text(strip=True)

    body = div.find(class_="cocal-ev-body")
    info = list(body.children)[1].get_text(strip=True)

    return Block(time_start, time_end, title, info)

