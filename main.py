'''
Laboratorna 1
'''

import folium
import argparse
import pandas as pd
from haversine import haversine
from geopy.geocoders import Nominatim
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


def generate_map(year: int, latitude: float, longitude: float, path: str) -> 0:
    '''
    (int, float, float, str) -> 0
    Generates HTML-map
    '''
    geolocator = Nominatim(user_agent = "Map_App",)
    user_coords = (latitude, longitude)

    df = pd.read_csv(path, sep = ';')
    df = df[df.Year == year]

    locations = list(df.Location)[:25]

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

    havers_dist = {}
    for place in distances:
        lenght = haversine(user_coords, place)
        havers_dist[lenght] = [user_coords, place]

    least_dist = sorted(list(havers_dist.keys()))[:10]

    map = folium.Map()
    fg = folium.FeatureGroup(name = '10 nearest films')
    for elem in least_dist:
        fg.add_child(
            folium.Marker(location = [float(havers_dist[elem][1][0]), float(havers_dist[elem][1][1])],
                          icon = folium.Icon())
        )

    uni_coords = [
        [50.463231, 30.519054],
        [50.445211, 30.459539],
        [49.841684, 24.030131],
        [49.993499, 36.233956],
        [50.450459, 30.457221],
        [50.323748, 26.518328],
        [48.288187, 25.936838],
        [48.905042, 24.719944],
        [49.221831, 28.414686],
        [46.654441, 32.623493]
    ]
    fg_1 = folium.FeatureGroup(name = 'Top-10 ukrainian universities')
    for uni in uni_coords:
        fg_1.add_child(
            folium.Marker(
            location = uni,
            icon = folium.Icon(color = 'red')
            )
        )

    map.add_child(fg)
    map.add_child(fg_1)
    map.add_child(folium.LayerControl())
    map.save('Map_films_main.html')

    return 0


if __name__ == '__main__':
    print(generate_map(args.year, args.latitude, args.longtitude, args.path))