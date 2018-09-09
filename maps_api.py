from credentials import city_mappers_api_key

import requests
import db_manager

default_payload = { 'key': city_mappers_api_key }

def get_travel_time(meeting_id, current_location):
    meeting_location = db_manager.get_meeting_location(meeting_id)
    startcoord = str(current_location[1]) + ',' + str(current_location[0])
    endcoord = str(meeting_location[1]) + ',' + str(meeting_location[0])
    payload = default_payload.copy()
    payload.update({'startcoord': startcoord, 'endcoord': endcoord})
    result = requests.get('https://developer.citymapper.com/api/1/traveltime/', params=payload)
    return result.json()['travel_time_minutes']

