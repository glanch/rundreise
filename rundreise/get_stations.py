import pandas as pd

stations = pd.read_csv("db_stations.csv", sep=";")

def get_eva_number(station_name):
    series = stations[stations["NAME"] == station_name]["EVA_NR"]

    if len(series) > 0:
        return str(series.iloc[0])
    else:
        return None
