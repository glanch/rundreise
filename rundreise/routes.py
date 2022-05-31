from bahnhofs_abfahrten_client import Client
from bahnhofs_abfahrten_client.api.hafas import trip_search_v_3, geo_station_v_1

import json
import datetime
from datetime import datetime, timezone, timedelta
from dateutil import parser

def find_trips_between(start, destination, start_time, end_time, only_regional = True):
    client = Client(base_url="https://marudor.de/api")

    merged_routes = []
    
    end_reached = False
    context = None

    while not end_reached:
        options = trip_search_v_3.TripSearchOptionsV3(start=start, destination=destination, only_regional=only_regional)
        if context is None:
            options.time = start_time
        else:
            options.ctx_scr = context

        trips_result = trip_search_v_3.sync_detailed(client=client, json_body=options)
        trips = json.loads(trips_result.content)
        routes = trips["routes"]
        if len(routes) > 0:
            context = trips["context"]["later"]

            routes_hash = {route["checksum"]: route for route in routes}
            def departure(route):
                return parser.parse(route["departure"]["scheduledTime"])

            scheduled_departures = list(map(departure, routes))
            
            last_route = max(scheduled_departures)

            if last_route > end_time:
                end_reached = True

            merged_routes.extend(routes)
        else:
            end_reached = True

        
    return merged_routes
