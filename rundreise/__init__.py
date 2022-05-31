import json
from datetime import datetime, timedelta, timezone, time

from bahnhofs_abfahrten_client import Client
from bahnhofs_abfahrten_client.api.hafas import geo_station_v_1

from rundreise.public_transport_routes import find_routes_between, find_stations
from rundreise.get_stations import get_eva_number

import itertools


stations_stay = {
    "Aachen Hbf": 2,
    "Darmstadt Hbf": 2,
    "Karlsruhe Hbf": 2,
}

# Get every eva number
eva_numbers = {
    station: get_eva_number(station) for station in stations_stay.keys()
}

# Build permutation of cities
stations_permutation_pairs = [
    (perm[0][0], perm[1][0]) for perm in itertools.permutations(eva_numbers.items())
]

total_days = sum(stations_stay.values())
trip_start_date = datetime.now(timezone.utc).date()

connections = {}


# For every day, we gather every connection between every city
for day in range(0, total_days):
    # Initialize multi-dimensional map
    connections[day] = {}

    for station_1, station_2 in stations_permutation_pairs:
        delta = timedelta(days=day)
        start_date = trip_start_date + delta
        start_time = datetime.combine(start_date, time(8, 0, 0), timezone.utc)
        end_time = datetime.combine(start_date, time(17, 0, 0), timezone.utc)

        routes = find_routes_between(
            start=eva_numbers[station_1],
            destination=eva_numbers[station_2],
            start_time=start_time,
            end_time=end_time,
            only_regional=True,
        )

        connections[day][station_1, station_2] = routes

print(connections)