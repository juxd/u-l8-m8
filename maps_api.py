from credentials import city_mappers_api_key

import requests
import db_manager

default_payload = { 'key': city_mappers_api_key }

def get_travel_time(meeting_id, current_location):
    meeting_location = db_manager.get_meeting_location(meeting_id)
    startcoord = current_location[0] + ',' + current_location[1]
    endcoord = meeting_location[0] + ',' + meeting_location[0]
    payload = default_payload.copy().update({'startcoord': startcoord, 'endcoord': endcoord})
    result = requests.get('https://developer.citymapper.com/api/1/traveltime/', params=payload)
    return result.json()['travel_time_minutes']

