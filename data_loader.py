import numpy as np
import pandas as pd


def load_data(airlines, routes, airp):
    ### LOAD ALL DATA ###

    airlines = pd.read_csv(airlines,
                           names=["airline ID", "Name", "alias", "IATA", "ICAO", "Callsign", "Country", "Active"])
    routes = pd.read_csv(routes,
                         names=["airline", "airline ID", "source airport", "source airport id", "destination airport",
                                "destination airport id", "codeshare", "stops", "equipment"])
    routes.replace('\\N', np.nan, inplace=True)
    routes = routes.dropna(axis=0, how='any')
    routes['airline ID'] = routes['airline ID'].astype(int)

    new_column_names = [
        'id', 'airport.name', 'city.name', 'country.name', 'IATA', 'ICAO',
        'lat', 'long', 'altitude', 'tz.offset', 'DST', 'tz.name',
        'airport.type', 'source.data']
    airports = pd.read_csv(airp, names=new_column_names)

    ### MERGE LOADED DATA TO ONE ###
    merged_df = pd.merge(routes, airlines, left_on='airline ID', right_on='airline ID', how='left')
    keep_col = ['airline', 'airline ID', 'Name', 'Country', 'source airport', 'source airport id',
                'destination airport', 'destination airport id', 'codeshare',
                'stops', 'equipment', 'Active']
    merged_df = merged_df[keep_col]
    merged_df = pd.merge(merged_df, airports, left_on='source airport', right_on='IATA', how='left')
    merged_df = pd.merge(merged_df, airports, left_on='destination airport', right_on='IATA', how='left')
    routes = ['Name', 'Country', 'airport.name_x', 'city.name_x', 'country.name_x',
              'lat_x', 'long_x', 'airport.name_y', 'city.name_y', 'country.name_y',
              'lat_y', 'long_y']
    routes = merged_df[routes]

    ### REMOVE NON-US DATA ###
    routes = routes[routes['country.name_x'].isin(['United States']) & routes['country.name_y'].isin(['United States'])]

    return routes