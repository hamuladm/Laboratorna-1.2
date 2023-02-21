'''
Laboratorna 1
'''

import folium
import geopy
import geocoder
import argparse
import pandas as pd
import numpy as np
from typing import List
import re
from haversine import haversine
from collections import Counter
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable


parser = argparse.ArgumentParser()

parser.add_argument(
    'year',
    help = 'Year',
    type = int
)

parser.add_argument(
    'latitude',
    help = 'Latitude',
    type = float
)

parser.add_argument(
    'longtitude',
    help = 'Longtitude',
    type = float
)

parser.add_argument(
    'path',
    help = 'Path to dataset'
)

args = parser.parse_args()


def generate_map(year: int, latitude: int, longitude, path: str) -> 0:
    '''
    (int, int, int, str) -> 0
    '''
    geolocator = Nominatim(user_agent = "Map_App",)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 1)
    user_coords = (latitude, longitude)

    df = pd.read_csv(path, sep = ';')
    df = df[df.Year == year]

    locations = list(df.Location)[:25]

    #return locations

    distances = []

    for location in locations:
        try:
            addr = geolocator.geocode(location)
            if not addr:
                continue
            loc = addr.latitude, addr.longitude
            distances.append(loc)
        except GeocoderUnavailable:
            continue

    # addr = geolocator.geocode(locations[0])
    # distances.append((addr.latitude, addr.longitude))

    #return distances
    havers_dist = {}

    for place in distances:
        lenght = haversine(user_coords, place)
        havers_dist[lenght] = [user_coords, place]

    # return havers_dist

    least_dist = sorted(list(havers_dist.keys()))[:10]

    # return least_dist


    map = folium.Map()

    fg = folium.FeatureGroup(
        name = 'Films'
    )

    for elem in least_dist:
        fg.add_child(
            folium.Marker(location = [float(havers_dist[elem][1][0]), float(havers_dist[elem][1][1])],
                          icon = folium.Icon())
        )

    map.add_child(fg)

    map.add_child(folium.LayerControl())
    map.save('Map_films.html')

    return 0

generate_map(2000, 49.83826, 24.02324, 'data_cut_test.csv')


if __name__ == '__main__':
    print(generate_map(args.year, args.latitude, args.longtitude, args.path))