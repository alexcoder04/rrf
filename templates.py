
error = "Sorry, an error occured while executing command `/{command}`. 🤯"

class shutdown:
    denied = "You are not allowed to use this command, you nasty bastard 😡"
    progress = "Shutting down... 😴"


class system:
    denied = "You are not allowed to use this command, you nasty bastard 😡"
    info = """User id: {user}
Running on: {host}
Running since: {started}

Log tail:
{log}"""


class start:
    greeting = """Hello there 👋!
I'm a bot that helps you find free rooms at the RWTH.

/free to find rooms that are free at the moment
/freeat to find rooms that are free at a certain time"""


class free:
    weekend = "It's weekend! Go touch some grass! 🌱"
    init = "⏳ I'm starting to check free rooms on {day} at {hour:02d}:{minute:02d}. Please be patient as this may take a while."
    no_found = """☑️ Checked {number} rooms in {duration:.3f} seconds.
Unfortunately, I was not able to find any rooms available at that time. 😞"""
    list_ = """☑️ Checked {number} rooms in {duration:.3f} seconds.
🎓 Here is what I can offer you:

"""

class freeat:
    missing_args = "⛔ Please pass the time you want to check as an argument. For example, `/freeat Tue 12:00`"
    invalid_args = "⛔ Your arguments are in an invalid format. The first one has to be a weekday(Mon/Tue/Wed/Thu/Fri/Sat/Sun) and the second one the time in 24-hour-format (e. g. 13:30)."
    passed_day = "⚠️ Please note that due to technical reasons I am using this week's timetable, not next week's."

