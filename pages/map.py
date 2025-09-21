import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
from streamlit_geolocation import streamlit_geolocation
import time
from pyproj import Geod
import requests
import json

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Map Tool")

# Complete CSS replacement for map.py - Replace the entire st.markdown CSS section with this:

st.title("Interactive Satellite Map with Area Calculation")

# Navigation (updated labels & improved wording)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🏠 Back to Home — Return to Dashboard", use_container_width=True, help="Go back to the main Hydro‑Assess page"):
        st.switch_page("index.py")
with col2:
    if st.button("⚙️ Open Calculator — Start Assessment", use_container_width=True, help="Open the intelligent recommendation engine to analyze this area"):
        st.switch_page("pages/calc.py")

# --- Google API Configuration ---
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")

if not GOOGLE_API_KEY:
    st.warning("Google API Key not configured. Add GOOGLE_API_KEY to your secrets.toml file for enhanced search.")
    st.info("Get your API key from: https://console.cloud.google.com/")

# --- Area Calculation Function ---
def calculate_geodesic_area(coordinates):
    """Calculate area using geodesic method"""
    if len(coordinates) < 3:
        return None
    
    if coordinates[0] != coordinates[-1]:
        coordinates = coordinates + [coordinates[0]]
    
    geod = Geod(ellps='WGS84')
    lons = [coord[0] for coord in coordinates]
    lats = [coord[1] for coord in coordinates]
    
    area_m2, perimeter_m = geod.polygon_area_perimeter(lons, lats)
    area_m2 = abs(area_m2)
    
    return {'area_m2': area_m2}

# --- Search Functions ---
def search_with_google_places(query, api_key):
    """Search using Google Places API"""
    try:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK' and data.get('results'):
                result = data['results'][0]
                location = result['geometry']['location']
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'name': result.get('name', ''),
                    'address': result.get('formatted_address', ''),
                    'place_id': result.get('place_id', '')
                }
    except Exception as e:
        st.error(f"Google Places search failed: {str(e)}")
    return None

def search_with_google_geocoding(query, api_key):
    """Search using Google Geocoding API"""
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': query,
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK' and data.get('results'):
                result = data['results'][0]
                location = result['geometry']['location']
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'address': result.get('formatted_address', ''),
                    'place_id': result.get('place_id', '')
                }
    except Exception as e:
        st.error(f"Google Geocoding failed: {str(e)}")
    return None

def search_with_nominatim(query):
    """Fallback search using OpenStreetMap Nominatim"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'limit': 5,
            'addressdetails': 1
        }
        headers = {'User-Agent': 'MapApp/1.0'}
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                results = []
                for item in data[:3]:
                    results.append({
                        'lat': float(item['lat']),
                        'lng': float(item['lon']),
                        'display_name': item.get('display_name', ''),
                        'type': item.get('type', ''),
                        'importance': item.get('importance', 0)
                    })
                return results
    except Exception as e:
        st.error(f"Nominatim search failed: {str(e)}")
    return None

def get_place_suggestions(query, api_key):
    """Get autocomplete suggestions using Google Places Autocomplete"""
    try:
        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {
            'input': query,
            'key': api_key,
            'types': 'geocode|establishment'
        }
        
        response = requests.get(url, params=params, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                return [pred['description'] for pred in data.get('predictions', [])]
    except:
        pass
    return []

def perform_search(query):
    """Unified search function that tries all methods"""
    result = None
    
    # Try Google APIs first if available
    if GOOGLE_API_KEY:
        result = search_with_google_places(query, GOOGLE_API_KEY)
        if not result:
            result = search_with_google_geocoding(query, GOOGLE_API_KEY)
    
    # If Google search found something, return it
    if result:
        return {'type': 'single', 'data': result}
    
    # Fallback to Nominatim
    nominatim_results = search_with_nominatim(query)
    if nominatim_results:
        return {'type': 'multiple', 'data': nominatim_results}
    
    return None

# --- Session State ---
DEFAULT_LOCATION = [12.9716, 77.5946]
DEFAULT_ZOOM = 12
MAX_ZOOM = 28

if 'map_initial_center' not in st.session_state:
    st.session_state.map_initial_center = DEFAULT_LOCATION
if 'map_initial_zoom' not in st.session_state:
    st.session_state.map_initial_zoom = DEFAULT_ZOOM
if 'map_force_refresh' not in st.session_state:
    st.session_state.map_force_refresh = 0
if 'map_location_set' not in st.session_state:
    st.session_state.map_location_set = False
if 'map_search_results' not in st.session_state:
    st.session_state.map_search_results = []
if 'map_selected_place' not in st.session_state:
    st.session_state.map_selected_place = None

# --- Location Selection UI (Similar to calc.py onboarding) ---
def show_location_selection():
    """Show location selection interface similar to calc.py onboarding"""
    st.markdown("### Choose Your Location Method")
    st.markdown("Select how you'd like to set your location on the map:")
    
    location_method = st.radio(
        "Location Selection Method:",
        ["Use GPS", "Search Address/Place", "Enter Coordinates", "Quick Locations"],
        horizontal=True
    )
    
    latitude, longitude = None, None
    selected_place = None
    
    if location_method == "Use GPS":
        st.markdown("#### GPS Location")
        try:
            def _try_geolocation():
                loc = streamlit_geolocation()
                lat_val = None
                lng_val = None
                if loc and isinstance(loc, dict):
                    if 'latitude' in loc and 'longitude' in loc:
                        lat_val, lng_val = loc.get('latitude'), loc.get('longitude')
                    elif 'coords' in loc and isinstance(loc['coords'], dict):
                        c = loc['coords']
                        lat_val, lng_val = c.get('latitude'), c.get('longitude')
                    elif 'lat' in loc and 'lon' in loc:
                        lat_val, lng_val = loc.get('lat'), loc.get('lon')
                if (lat_val in [None, 'NULL']) or (lng_val in [None, 'NULL']):
                    lat_val = None
                    lng_val = None
                if lat_val is not None and lng_val is not None:
                    return float(lat_val), float(lng_val), 'gps'
                # Fallback via IP (approximate)
                try:
                    ip_resp = requests.get("https://ipapi.co/json/", timeout=5)
                    if ip_resp.status_code == 200:
                        j = ip_resp.json()
                        if j.get('latitude') and j.get('longitude'):
                            return float(j['latitude']), float(j['longitude']), 'ip'
                except Exception:
                    pass
                return None, None, None
            
            lat, lng, source = _try_geolocation()
            if lat is not None and lng is not None:
                latitude = lat
                longitude = lng
                if source == 'ip':
                    st.info("Using approximate location (IP-based)")
                else:
                    st.success("GPS location acquired successfully")
            else:
                if st.button("Get GPS Location", use_container_width=True):
                    st.rerun()
                st.info("Click the button above to get your GPS location")
                    
        except ImportError:
            st.error("GPS functionality requires 'streamlit-geolocation' package.")
            st.code("pip install streamlit-geolocation")
    
    elif location_method == "Search Address/Place":
        st.markdown("#### Address/Place Search")
        search_query = st.text_input(
            "Enter address, place name, or landmark:",
            placeholder="e.g., IIT Delhi Campus, New Delhi"
        )

        # Autocomplete suggestions (your existing code for this is fine)
        if search_query and len(search_query) > 2 and GOOGLE_API_KEY:
            suggestions = get_place_suggestions(search_query, GOOGLE_API_KEY)
            if suggestions:
                selected_suggestion = st.selectbox(
                    "Suggestions:",
                    options=[""] + suggestions,
                    key="place_suggestion_box"
                )
                if selected_suggestion:
                    search_query = selected_suggestion

        # --- CORRECTED SEARCH LOGIC ---
        # This section now handles all results consistently.
        if st.button("Search", use_container_width=True) and search_query:
            with st.spinner("Searching..."):
                search_result = perform_search(search_query)

                # Unified logic: Always store results in a list in session_state
                if search_result:
                    if search_result['type'] == 'single':
                        # If one result, put it in a list
                        st.session_state.map_search_results = [search_result['data']]
                    else:  # 'multiple'
                        # If multiple results, use the list directly
                        st.session_state.map_search_results = search_result['data']
                else:
                    st.error("Location not found. Try different search terms.")
                    st.session_state.map_search_results = []

        # --- CORRECTED RESULT DISPLAY & SELECTION ---
        # This section uses st.radio for a stable selection experience.
        if st.session_state.map_search_results:
            # Create a dictionary of {display_name: full_result_object}
            # This makes it easy to look up the full data from the user's selection.
            options = {
                (res.get('address') or res.get('display_name')): res
                for res in st.session_state.map_search_results
            }

            # Let the user select a result using a radio button
            selected_display_name = st.radio(
                "Select from results:",
                options.keys()
            )

            # Prepare the selected data for the 'Apply' button
            if selected_display_name:
                selected_result_data = options[selected_display_name]
                latitude = selected_result_data['lat']
                # Handle both 'lng' (from Google) and 'lon' (from Nominatim)
                longitude = selected_result_data.get('lng') or selected_result_data.get('lon')
                selected_place = selected_result_data
    elif location_method == "Enter Coordinates":
        st.markdown("#### Manual Coordinates")
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", value=12.9716, format="%.6f")
        with col2:
            longitude = st.number_input("Longitude", value=77.5946, format="%.6f")
        
        if st.button("Set Location", use_container_width=True):
            if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                st.success("Coordinates set successfully!")
            else:
                st.error("Invalid coordinates. Please check your values.")
                latitude, longitude = None, None
    
    else:  # Quick Locations
        st.markdown("#### Quick Location Shortcuts")
        quick_locations = {
            "Delhi, India": [28.6139, 77.2090],
            "Mumbai, India": [19.0760, 72.8777],
            "Bangalore, India": [12.9716, 77.5946],
            "Kolkata, India": [22.5726, 88.3639],
            "Chennai, India": [13.0827, 80.2707],
            "New York, USA": [40.7128, -74.0060],
            "London, UK": [51.5074, -0.1278],
            "Tokyo, Japan": [35.6762, 139.6503]
        }
        
        selected_city = st.selectbox("Choose a city:", [""] + list(quick_locations.keys()))
        
        if selected_city and st.button("Use This Location", use_container_width=True):
            latitude, longitude = quick_locations[selected_city]
            selected_place = {'name': selected_city, 'address': selected_city}
            st.success(f"Selected: {selected_city}")
    
    # Apply location button
    st.markdown("---")
    can_proceed = latitude is not None and longitude is not None
    
    if not can_proceed:
        st.warning("Please set a location using one of the methods above.")
    
    if st.button("Apply Location to Map", type="primary", disabled=not can_proceed, use_container_width=True):
        st.session_state.map_initial_center = [latitude, longitude]
        st.session_state.map_initial_zoom = 16
        st.session_state.map_location_set = True
        st.session_state.map_selected_place = selected_place
        st.session_state.map_search_results = []  # Clear any search results
        st.success("Location applied! Loading map...")
        time.sleep(0.5)
        st.rerun()

# --- Main Application Logic ---
if not st.session_state.map_location_set:
    show_location_selection()
    st.stop()

# --- Map Display ---
st.markdown("---")

# Controls
col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
with col1:
    if st.button("🔄 Reset Map View", use_container_width=True, help="Reset the map to the initial center and zoom"):
        st.session_state.map_force_refresh += 1
        st.rerun()
with col2:
    if st.button("📍 Change Location", use_container_width=True, help="Choose a different location or re-run the location selection"):
        st.session_state.map_location_set = False
        st.session_state.map_selected_place = None
        st.session_state.map_search_results = []
        st.rerun()
with col3:
    if st.button("🔎 New Search", use_container_width=True, help="Start a fresh address/place search"):
        st.session_state.map_location_set = False
        st.rerun()
with col4:
    if st.session_state.map_selected_place:
        place_info = (st.session_state.map_selected_place.get('address') or 
                     st.session_state.map_selected_place.get('display_name') or
                     st.session_state.map_selected_place.get('name', ''))
        if place_info:
            st.info(f"Location: {place_info[:120]}")  # show slightly more text
    else:
        st.info("Draw polygons or rectangles on the map to calculate area")

# Create map
m = folium.Map(
    location=st.session_state.map_initial_center,
    zoom_start=st.session_state.map_initial_zoom,
    max_zoom=MAX_ZOOM,
    tiles=None,
    control_scale=True
)

# Add satellite layer
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google',
    name='Satellite',
    overlay=False,
    control=True,
    maxZoom=MAX_ZOOM
).add_to(m)

# Add hybrid layer
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google',
    name='Hybrid',
    overlay=False,
    control=True,
    maxZoom=MAX_ZOOM
).add_to(m)


# Add layer control
folium.LayerControl().add_to(m)

# Drawing tools
Draw(
    export=True,
    draw_options={
        'polyline': False,
        'polygon': True,
        'rectangle': True,
        'circle': False,
        'marker': False,
        'circlemarker': False,
        'edit': {'edit': True, 'remove': True}
    }
).add_to(m)

# Location marker with popup
popup_text = "Selected Location"
if st.session_state.map_selected_place:
    if 'name' in st.session_state.map_selected_place:
        popup_text = st.session_state.map_selected_place['name']
    elif 'address' in st.session_state.map_selected_place:
        popup_text = st.session_state.map_selected_place['address']
    elif 'display_name' in st.session_state.map_selected_place:
        popup_text = st.session_state.map_selected_place['display_name']

folium.Marker(
    st.session_state.map_initial_center,
    popup=popup_text,
    tooltip=popup_text,
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Render map
map_data = st_folium(
    m,
    key=f"map_{st.session_state.map_force_refresh}",
    width=1200,
    height=600,
    returned_objects=["last_active_drawing"],
    use_container_width=True
)

# Area calculation
if map_data and map_data.get("last_active_drawing"):
    geojson = map_data["last_active_drawing"]
    if "geometry" in geojson:
        geometry = geojson["geometry"]
        if geometry.get('type') in ['Polygon', 'Rectangle']:
            coords = geometry['coordinates'][0]
            area = calculate_geodesic_area(coords)
            if area:
                # Calculate centroid of the selected polygon
                lats = [coord[1] for coord in coords[:-1]]  # Exclude last point (duplicate of first)
                lons = [coord[0] for coord in coords[:-1]]
                centroid_lat = sum(lats) / len(lats)
                centroid_lon = sum(lons) / len(lons)
                
                # Store data in session state for calc.py
                st.session_state.latitude = centroid_lat
                st.session_state.longitude = centroid_lon
                st.session_state.area = area['area_m2']
                st.session_state.coordinates_from_map = True  # Flag to indicate map selection
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Area (m²)", f"{area['area_m2']:,.2f}")
                with col2:
                    st.metric("Area (sq ft)", f"{area['area_m2'] * 10.764:,.2f}")
                with col3:
                    st.metric("Area (acres)", f"{area['area_m2'] / 4047:,.4f}")
                with col4:
                    if st.button("🔍 Generate Detailed Analysis & Recommendations", use_container_width=True, help="Create a full assessment using this selected area"):
                        st.switch_page("pages/calc.py")

# Sidebar with info
with st.sidebar:
    st.header("Current Location")
    st.write(f"**Lat:** {st.session_state.map_initial_center[0]:.6f}")
    st.write(f"**Lng:** {st.session_state.map_initial_center[1]:.6f}")
    
    if st.session_state.map_selected_place:
        st.markdown("---")
        st.header("Selected Place")
        place = st.session_state.map_selected_place
        if 'name' in place:
            st.write(f"**Name:** {place['name']}")
        if 'address' in place:
            st.write(f"**Address:** {place['address']}")
        elif 'display_name' in place:
            st.write(f"**Address:** {place['display_name']}")
    
    st.markdown("---")
    if st.button("↺ Reset to Default Location & View", use_container_width=True, help="Restore original demo location and zoom"):
        st.session_state.map_initial_center = DEFAULT_LOCATION
        st.session_state.map_initial_zoom = DEFAULT_ZOOM
        st.session_state.map_force_refresh += 1
        st.session_state.map_selected_place = None
        st.session_state.map_search_results = []
        st.rerun()
    
    st.markdown("---")
    st.header("Instructions")
    st.write("1. Location is set and marked")
    st.write("2. Use drawing tools to select area")
    st.write("3. Draw polygon or rectangle")
    st.write("4. View calculated area")
    st.write("5. Switch between map layers")
    st.write("6. Click 'Generate Analysis' to proceed")
    
    st.markdown("---")
    st.header("Map Layers")
    st.write("• **Satellite:** High-resolution aerial imagery")
    st.write("• **Hybrid:** Satellite with road labels")
    st.write("• **Street Map:** Traditional road map")