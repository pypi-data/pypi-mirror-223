import folium
import re
from folium.plugins import HeatMap

class heatMapItemsFrequency:
    def __init__(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        self.lines = content.split('\n')
        
    def extract_lat_lon_radius(self, point_radius_str):
        match = re.search(r'Point\((.*?)\)', point_radius_str)
        if match is None:
            return None, None, None

        lat_lon_str = match.group(1)
        lon, lat = map(float, lat_lon_str.split())

        radius_str = point_radius_str.split(':')[-1] if ':' in point_radius_str else '0'
        radius = int(radius_str)
        
        return lat, lon, radius

    def create_heat_map(self):
        m = folium.Map(location=[35.682839, 139.759455], zoom_start=5)
        heat_data = []

        for line in self.lines:
            elements_list = line.split(',')
            for elements in reversed(elements_list):
                lat, lon, radius = self.extract_lat_lon_radius(elements)
                
                # Skip if pattern does not match
                if lat is None or lon is None or radius is None:
                    continue
                
                # Using radius as weight for the heatmap
                heat_data.append([lat, lon, radius])
        
        HeatMap(heat_data).add_to(m)
        return m

if __name__ == "__main__":
    heatmap_frequency = HeatMapItemsFrequency('frequentPatterns.txt')
    m = heatmap_frequency.create_heat_map()
    m