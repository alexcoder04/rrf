from .event import Event
from .mytime import Time
from bs4 import BeautifulSoup
from datetime import date, datetime
import requests


DAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


class Room:
    loaded = False
    URL_TEMPLATE = "https://online.rwth-aachen.de/RWTHonline/pl/ui/$ctx;design=ca2;header=max/wbKalender.wbRessource?pDatum={date}&pOrgNr=&pResNr={rb_id}"
    URL_MAP_TEMPLATE = "https://maps.rwth-aachen.de/navigator/?type=roadmap&obj={building}"

    def __init__(self, rb_id: int) -> None:
        if rb_id is None or rb_id == 0:
            return

        response = requests.get(self.URL_TEMPLATE.format(date=date.today().strftime('%d.%m.%Y'), rb_id=rb_id))
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        self.rb_id = rb_id
        self.name = soup.find(id="idTopPageHeader").find("tr").find("td").get_text(strip=True)
        self.days = []
        self.loadtime = datetime.now()

        divs = soup.find_all('div', class_='cocal-ev-content')

        day = -1
        for i, div in enumerate(divs):
            block = Event.from_html(div)
            if block is None:
                continue
            if block.time_start.hour == 0 and block.time_start.minute == 0:
                day += 1
                self.days.append([])
            self.days[day].append(block)

        self.loaded = True

    def minutes_left(self, day: int, time: Time) -> Time:
        if self.occupied(day, time):
            return None

        future_events = [event for event in self.days[day] if event.time_start > time]
        if not future_events:
            return Time(23, 59)

        next_event = min(future_events, key=lambda e: e.time_start)
        return next_event.time_start - time

    def occupied(self, day: int, time: Time) -> bool:
        for block in self.days[day]:
            if block.time_start <= time and block.time_end > time:
               return True
        return False

    def free(self, day: int, time: Time) -> bool:
        return not self.occupied(day, time)

    def rb_url(self) -> str:
        return self.URL_TEMPLATE.format(date=date.today().strftime('%d.%m.%Y'), rb_id=self.rb_id)

    def print_data(self) -> None:
        title = f"{self.name} ({self.rb_id})"
        print()
        print("-" * (len(title)+4))
        print("| " + title + " |")
        print("-" * (len(title)+4))

        for i, day in enumerate(self.days):
            print()
            print(DAYS[i])
            for block in day:
                print(block)

    def short_disp(self) -> str:
        return self.name

    def html_disp(self) -> str:
        return "<a href='{plan_url}'>{name}</a> (<a href='{map_url}'>{bid}</a>)".format(
                plan_url=self.URL_TEMPLATE.format(date=date.today().strftime('%d.%m.%Y'), rb_id=self.rb_id),
                name=self.name.split("(")[0].strip(),
                map_url=self.URL_MAP_TEMPLATE.format(building=self.name.split("(")[1].replace(")", "").split("|")[0]),
                bid=self.name.split("(")[1].replace(")", "")
                )

    def __repr__(self) -> str:
        return f"Room \"{self.name}\" ({self.rb_id})"

