import folium

# Generates an interactive HTML map of cache locations

def generate_cache_map(caches, default_location=(0, 0), zoom=2, map_path='cache_map.html'):
    """
    caches: list of tuples (id, name, lat, lng, description)
    default_location: tuple for initial map center
    zoom: initial zoom level
    map_path: output HTML file path
    """
    m = folium.Map(location=default_location, zoom_start=zoom)
    for cid, name, lat, lng, desc in caches:
        folium.Marker(
            [lat, lng], popup=f"{name}: {desc}", tooltip=name
        ).add_to(m)
    m.save(map_path)
    return map_path