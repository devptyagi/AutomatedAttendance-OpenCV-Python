# this is for the referance the code has been added directly to login.py
from datetime import datetime

def Time:
    global strTime
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    return strTime
hour = int(datetime.datetime.now().hour)
if hour>=0 and hour<12:
    daytime = "Morning"
elif hour>=12 and hour<18:
    daytime = "Afternoon"
else:
    daytime = "Evening"

strTime = strTime + ' ' + daytime
