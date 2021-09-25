from datetime import datetime
import time
import datetime

def Current_Now():
    timestamp = time.time()/86400 #(60 секунд, 60 мин, 24 часа = 86400)
    return timestamp

def Current_Now_Str():
    dt = datetime.date.today()
    return dt

def DateToStr(date,type):
    if type == 0:
        dt = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(date*86400),'%d.%m.%Y %H:%M')
    else:
        dt = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(date * 86400), '%d.%m.%Y')
    return dt

def DateToDateIsoformat(date):

    dt = datetime.datetime.utcfromtimestamp(date*86400).isoformat()
    return dt

def DateStrToFloat(date):
    dt = int(round((datetime.datetime.strptime(date,'%d.%m.%Y').timestamp())/86400))
    return dt

def TimeStrToInt(time_str):
   h, m = time_str.split(':')
   return int(h) * 60 + int(m)

def IntToTimeStr(mn):
    h = int(mn/60)
    m = (mn%60)
    if h < 10:
        h = '0' + str(h)
    if m < 10:
        m = '0'+str( m)
    time_str = str(h) +':'+ str(m)
    return time_str





