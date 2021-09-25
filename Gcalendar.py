import httplib2
import config
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

def main():
        credentials = ServiceAccountCredentials.from_json_keyfile_name(config.client_secret_calendar, 'https://www.googleapis.com/auth/calendar')
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service

def add_event(events):

    events_info = []
    service = main()
    for calendarId, event in events:
        event_result = service.events().insert(calendarId=calendarId, body=event).execute()
        events_info.append((event_result['id'], event_result['source']['title']))
    return events_info

def update_event(calendarId, eventid, start, end, talonid, client_name, phone, tlg_client_name, colorId):
    service = main()
    event_result = service.events().update(
            calendarId=calendarId,
            eventId=eventid,
            body={
                "summary": str(client_name),
                "description": 'Телефон клиента: ' + str(phone)+'\n'+'Telegram: ' + str(tlg_client_name),
                "start": {"dateTime": start, "timeZone": 'Europe/Moscow'},
                "end": {"dateTime": end, "timeZone": 'Europe/Moscow'},
                "colorId": colorId,
                "source": {
                    "url": 'https://t.me/llllllallllll_bot',
                    "title": str(talonid)
                }
            },
        ).execute()

def delete_event(calendarId, eventid):
    service = main()
    try:
        service.events().delete(
            calendarId=calendarId,
            eventId=eventid,
        ).execute()
    except:
        print("Failed to delete event")



# if __name__ == '__main__':
#     add_talon(18845, 600, 780)
