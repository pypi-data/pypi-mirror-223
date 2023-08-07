import sys
import os
import folium
import re

class heatMapItemsFrequencies:
    # Add the module directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    frequencyOfItems_directory = os.path.join(current_directory, '../statics')
    sys.path.append(frequencyOfItems_directory)
    
    # 1. Import frequencyOfItems.py
    from frequencyOfItems import frequencyOfItems
    
    # 2. Set values for inputFile, minSup, and sep
    inputFile = 'PM24HeavyPollutionRecordingSensors.csv'
    minSup = 10
    sep = '\t'
    
    # 3. Create an instance of the frequencyOfItems class
    itemsFrequency = frequencyOfItems(inputFile, minSup, sep)

    # 4. Call the getFrequency function to retrieve the return value
    itemsFreqDictionary = itemsFrequency.getFrequency()

    lines = itemsFreqDictionary.split('\n')

    m = folium.Map(location=[35.682839, 139.759455], zoom_start=5)  # Initial location is around Tokyo

    # Helper function to extract latitude, longitude, and radius from a point string
    def extract_lat_lon_radius(point_radius_str):
        match = re.search(r'Point\((.*?)\)', point_radius_str)
        if match is None:
            return None, None, None  # return None if the pattern does not match
        lat_lon_str = match.group(1)
        lon, lat = map(float, lat_lon_str.split())

        radius_str = point_radius_str.split(':')[-1] if ':' in point_radius_str else '0'
        radius = int(radius_str)

        return lat, lon, radius

    for line in lines:
        elements_list = line.split(',')

        for elements in reversed(elements_list):
            # Add each Point as a circle on the map
            lat, lon, radius = extract_lat_lon_radius(elements)

            # Skip if the pattern does not match
            if lat is None or lon is None or radius is None:
                continue

            color = ""
            if 0 <= radius < 25:
                color = "pink"
            elif 25 <= radius < 50:
                color = "blue"
            else:
                color = "yellow"
            folium.CircleMarker(location=[lat, lon], radius=5, fill=True, fill_color=color, color=color, fill_opacity=0.4).add_to(m)

    # Display the map
    m
