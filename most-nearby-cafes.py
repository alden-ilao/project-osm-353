import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_TEMPLATE=(
    "Cafe with the most dense number of nearby cafes:\n"
    "Name: {cafe_name}\n"
    "Latitude: {lat}\n"
    "Longitude: {lon}\n"
    "# of Cafes 0.8km from location: {count}"
)

'''
CITATION:
count_cafes_walkable_from and deg2rad modified from: user1921 
https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
'''
def deg2rad(deg):
    '''
    returns series of rads
    '''
    return deg * (np.pi / 180)

def count_cafes_walkable_from(cafe, filtered_cafes, walkable=0.8):
    R = 6371; # Radius of the earth in km

    cafe_lat = cafe['lat']
    cafe_lon = cafe['lon']
    
    # start operating on numpy arrays
    dLat = deg2rad(cafe_lat - filtered_cafes['lat'])
    dLon = deg2rad(cafe_lon - filtered_cafes['lon'])
    
    a = (
        np.sin(dLat / 2) * np.sin(dLat / 2) + 
        np.cos(deg2rad(cafe_lat)) * np.cos(deg2rad(filtered_cafes['lat'])) * 
        np.sin(dLon/2) * np.sin(dLon/2)
        )
    
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c # in km
    return d[d <= walkable].count()

def filter_out_franchises(cafes_df):
    # filter-out franchised cafes
    cafe_counts_df = cafes_df.groupby(['name'])['name'].count()
    franchises_counts = cafe_counts_df[cafe_counts_df > 3]
    franchises = set(franchises_counts.index)

    return cafes_df[~cafes_df['name'].isin(franchises)]

def main():
    file_amenities = sys.argv[1]
    amenities = pd.read_json(file_amenities, lines=True)[['lat','lon','amenity','name']]

    cafes = amenities[amenities['amenity'] == 'cafe']

    # filter out franchises
    filtered_cafes = filter_out_franchises(cafes).reset_index()

    filtered_cafes['cafes nearby'] = filtered_cafes.apply(count_cafes_walkable_from, filtered_cafes=filtered_cafes, axis=1)

    idx = filtered_cafes['cafes nearby'].idxmax()
    most_dense = filtered_cafes.iloc[idx]

    plt.plot(filtered_cafes['lon'],filtered_cafes['lat'],'.b',alpha=0.5)
    plt.plot(most_dense['lon'],most_dense['lat'],'.r')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Non Franchised Cafe Locations')
    plt.legend(['cafes', 'Most nearby cafes'])
    plt.savefig('cafes.jpg')
        
    print(OUTPUT_TEMPLATE.format(
        cafe_name=most_dense['name'],
        lat=most_dense['lat'],
        lon=most_dense['lon'],
        count=most_dense['cafes nearby']
    ))


if __name__ == '__main__':
    main()
