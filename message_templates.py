
START = """Hello there 👋!
I'm a bot that helps you find free rooms at the RWTH.

/free to find rooms that are free at the moment
/freeat to find rooms that are free at a certain time
/where to locate a building by its number"""

FREEAT_WEEKEND = "⚠️ Please note that due to technical reasons I am using this week's timetable, not next week's."
FREEAT_ERROR = """⛔ Please pass the time you want to check as an argument. 
For Example, `/freeat Tue 12:00`"""
FREEAT_INVALIDDAY = "⛔ The entered weekday '{day}' is invalid. Enter one of these: Mon/Tue/Wed/Thu/Fri/Sat/Sun."
FREEAT_START = """I'm starting to check free rooms on {day} at {hour:02d}:{minute:02d}.
Please be patient as this may take a while. ⏳"""
FREEAT_NO = """☑️ Checked {number} rooms in {dur:.2f} seconds.
Unfortunately, I was not able to find any rooms available at that time. 😞"""
FREEAT_RESP = """☑️ Checked {number} rooms in {dur:.2f} seconds.
🎓 Here is what I can offer you:

"""

FREE_WEEKEND = "It's weekend! I'm not even going to bother, go touch some grass! 🌱"
FREE_START = FREEAT_START
FREE_NO = FREEAT_NO
FREE_RESP = FREEAT_RESP

WHERE_ERROR = """⛔ Please pass the building number you want to find as an argument. 
For Example, `/where 1385`"""
WHERE_ANS = """🏫 You can find {building} over here:
https://maps.rwth-aachen.de/navigator/?type=roadmap&obj={building}"""


SHUTDOWN_DENIED = "You are not allowed to use this command, you nasty bastard 😡"
SHUTDOWN_SUCCESS = "Shutting down... 😴"

