import googlemaps
import numpy as np

gmaps = googlemaps.Client(key='AIzaSyBHTg3CiB8uRMI_OUl9-qkfIEvLJLLRlhM')

# placeholder options
modes = ['driving', 'walking', 'transit', 'bicycling']
types = ['airport', 'bank', 'bar', 'cafe', 'gas_station', 'grocery_or_supermarket', 'gym',
         'hospital', 'laundry', 'park', 'police', 'school', 'train_station', 'transit_station']


# works w/ strings and lat-lon pairs as a list
def get_distances(work, locations):
    results = []
    print locations
    if len(locations) <= 1:
        locations = [locations]
    for i, loc in enumerate(locations):
        print loc
        if loc[0] is None:
            results.append(np.nan)
        else:
            dist = gmaps.distance_matrix(
                origins=work,
                destinations=loc,
                mode=None,
                units='imperial')
            duration = dist['rows'][0]['elements'][0]['duration']['text'].encode('utf-8')
            distance = dist['rows'][0]['elements'][0]['distance']['text'].encode('utf-8')
            if not bool(duration and distance):
                results.append(np.nan)
            else:
                results.append([duration, distance])
    return results


# works w/ lat-long only (not strings)
def get_places(category, locations):
    if category not in types:
        return None
    else:
        if len(locations) <= 1:
            locations = [locations]
        results = []
        for i, loc in enumerate(locations):
            if loc[0] is None:
                results.append(np.nan)
            else:
                places = []
                place = gmaps.places_nearby(
                    location = loc,
                    rank_by = 'distance',
                    type = category)
                for j in range(3):
                    places.append(place['results'][j]['name'].encode('utf-8'))
                    # for pulling lat-lon, omitted to reduce gmaps API calls
                    # place['results'][j]['geometry']['location']
                results.append(places)
    return results


def add_gmaps_cols(filtered_df, work, category):
    locations = zip(filtered_df['latitude'], filtered_df['longitude'])
    dist_col = get_distances(work, locations)
    places_col = get_places(category, locations)
    filtered_df['local'] = places_col
    filtered_df['commute'] = dist_col
    return filtered_df
