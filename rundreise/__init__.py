from bahnhofs_abfahrten_client import Client
from bahnhofs_abfahrten_client.api.hafas import geo_station_v_1

client = Client(base_url="https://marudor.de/api")

# Find stations in Aachen
stations_result = geo_station_v_1.sync_detailed(client=client, lat=50.775555, lng=6.083611)
stations = json.loads(stations_result.content)

# Find all routes between now and now + 1h
start_time = datetime.now(timezone.utc)
end_time = start_time + timedelta(minutes=10)
routes = find_trips_between(start=stations[1]["id"], destination=stations[0]["id"], start_time=start_time, end_time=end_time, only_regional=True)
print(routes)