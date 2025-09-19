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

st.markdown("""
<style>
    /* CSS Variables for consistent theming and better readability */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-card: #ffffff;
        --text-primary: #2c3e50;
        --text-secondary: #34495e;
        --text-muted: #6c757d;
        --border-color: #dee2e6;
        --success-color: #28a745;
        --warning-color: #007bff;
        --error-color: #dc3545;
        --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        --shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    
    /* Dark mode variables */
    [data-theme="dark"], .stApp[data-theme="dark"] {
        --bg-primary: #1a1a1a;
        --bg-secondary: #2d2d2d;
        --bg-card: #343a40;
        --text-primary: #ffffff;
        --text-secondary: #e9ecef;
        --text-muted: #adb5bd;
        --border-color: #495057;
        --success-color: #20c997;
        --warning-color: #17a2b8;
        --error-color: #fd7e14;
        --shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        --shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    
    /* Auto dark mode detection */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --bg-card: #343a40;
            --text-primary: #ffffff;
            --text-secondary: #e9ecef;
            --text-muted: #adb5bd;
            --border-color: #495057;
            --success-color: #20c997;
            --warning-color: #17a2b8;
            --error-color: #fd7e14;
            --shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            --shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.4);
        }
    }
    
    /* Main app styling */
    .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    .main .block-container {
        background-color: var(--bg-primary) !important;
        padding: 2rem 1rem;
        max-width: 1400px;
    }
    
    /* Typography improvements */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
        margin-bottom: 1rem !important;
    }
    
    .stApp h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    .stApp h3 {
        font-size: 1.5rem !important;
        color: var(--text-secondary) !important;
    }
    
    .stApp h4 {
        font-size: 1.25rem !important;
        color: var(--text-secondary) !important;
    }
    
    .stApp p, .stApp span, .stApp div, .stApp li {
        color: var(--text-primary) !important;
        line-height: 1.6 !important;
        font-size: 1rem !important;
    }
    
    .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    /* Improved section headers */
    .stApp h3 {
        background: linear-gradient(135deg, var(--warning-color), var(--success-color)) !important;
        background-clip: text !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
    }
    
    .stApp h4 {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid var(--border-color) !important;
    }
    
    /* Radio button improvements for location selection */
    .stRadio {
        background-color: var(--bg-card) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 16px 0 !important;
        box-shadow: var(--shadow) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .stRadio > div {
        background-color: transparent !important;
    }
    
    .stRadio label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
    }
    
    .stRadio div[role="radiogroup"] > label {
        background-color: var(--bg-secondary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin: 4px !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .stRadio div[role="radiogroup"] > label:hover {
        background-color: var(--bg-card) !important;
        border-color: var(--warning-color) !important;
        box-shadow: var(--shadow) !important;
    }
    
    /* Input fields with better contrast and sizing */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 14px 16px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--warning-color) !important;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1) !important;
        outline: none !important;
    }
    
    /* Labels for form fields */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stTextArea label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 8px !important;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background-color: var(--warning-color) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        min-height: 50px !important;
        cursor: pointer !important;
        box-shadow: var(--shadow) !important;
    }
    
    .stButton > button:hover {
        background-color: #0056b3 !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-hover) !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: var(--success-color) !important;
        font-size: 1.1rem !important;
        padding: 16px 32px !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #1e7e34 !important;
    }
    
    .stButton > button:disabled {
        background-color: var(--text-muted) !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* Metric cards for area display */
    [data-testid="stMetric"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.3s ease !important;
        min-height: 120px !important;
        text-align: center !important;
    }
    
    [data-testid="stMetric"]:hover {
        box-shadow: var(--shadow-hover) !important;
        transform: translateY(-2px) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 8px !important;
    }
    
    /* Sidebar improvements */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] p {
        color: var(--text-secondary) !important;
        line-height: 1.5 !important;
    }
    
    /* Alert boxes with better readability */
    .stInfo {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--warning-color) !important;
        border-left: 4px solid var(--warning-color) !important;
        color: var(--text-primary) !important;
        padding: 16px 20px !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: var(--shadow) !important;
        margin: 16px 0 !important;
    }
    
    .stSuccess {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--success-color) !important;
        border-left: 4px solid var(--success-color) !important;
        color: var(--text-primary) !important;
        padding: 16px 20px !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: var(--shadow) !important;
        margin: 16px 0 !important;
    }
    
    .stWarning {
        background-color: var(--bg-card) !important;
        border: 1px solid #ffc107 !important;
        border-left: 4px solid #ffc107 !important;
        color: var(--text-primary) !important;
        padding: 16px 20px !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: var(--shadow) !important;
        margin: 16px 0 !important;
    }
    
    .stError {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--error-color) !important;
        border-left: 4px solid var(--error-color) !important;
        color: var(--text-primary) !important;
        padding: 16px 20px !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: var(--shadow) !important;
        margin: 16px 0 !important;
    }
    
    /* Map container styling */
    iframe {
        border-radius: 12px !important;
        box-shadow: var(--shadow-hover) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Expander improvements */
    .streamlit-expanderHeader {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 16px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 20px !important;
    }
    
    /* Column spacing and layout */
    [data-testid="column"] {
        padding: 0 8px !important;
    }
    
    /* Selectbox improvements */
    .stSelectbox {
        margin: 12px 0 !important;
    }
    
    .stSelectbox > div > div {
        background-color: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox > div > div > div {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        padding: 12px 16px !important;
    }
    
    /* Progress indicators */
    .stSpinner {
        color: var(--warning-color) !important;
    }
    
    .stSpinner > div {
        border-color: var(--warning-color) transparent var(--warning-color) transparent !important;
    }
    
    /* Text input placeholder styling */
    .stTextInput input::placeholder {
        color: var(--text-muted) !important;
        font-style: italic !important;
    }
    
    /* Ensure proper contrast for all text elements */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: var(--text-primary) !important;
        line-height: 1.6 !important;
    }
    
    .stMarkdown strong {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }
    
    .stMarkdown em {
        color: var(--text-secondary) !important;
        font-style: italic !important;
    }
    
    /* List improvements */
    .stMarkdown ul, .stMarkdown ol {
        padding-left: 1.5rem !important;
        margin: 1rem 0 !important;
    }
    
    .stMarkdown ul li, .stMarkdown ol li {
        margin-bottom: 0.5rem !important;
        color: var(--text-primary) !important;
    }
    
    /* Code blocks if any */
    .stMarkdown code {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid var(--border-color) !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Ensure all interactive elements have proper focus states */
    button:focus-visible,
    input:focus-visible,
    select:focus-visible {
        outline: 2px solid var(--warning-color) !important;
        outline-offset: 2px !important;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth !important;
    }
    
    /* Ensure text remains readable during loading */
    .stApp * {
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        text-rendering: optimizeLegibility !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Interactive Satellite Map with Area Calculation")

# Navigation (updated labels & improved wording)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🏠 Back to Home — Return to Dashboard", use_container_width=True, help="Go back to the main Hydro‑Assess page"):
        st.switch_page("index")
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
            placeholder="e.g., Delhi, India or Times Square, New York"
        )
        
        # Show suggestions if available
        if search_query and len(search_query) > 2:
            if GOOGLE_API_KEY:
                suggestions = get_place_suggestions(search_query, GOOGLE_API_KEY)
                if suggestions:
                    selected_suggestion = st.selectbox(
                        "Suggestions:",
                        options=[""] + suggestions
                    )
                    if selected_suggestion:
                        search_query = selected_suggestion
        
        if st.button("Search", use_container_width=True) and search_query:
            with st.spinner("Searching..."):
                search_result = perform_search(search_query)
                
                if search_result:
                    if search_result['type'] == 'single':
                        # Direct result from Google
                        result = search_result['data']
                        latitude = result['lat']
                        longitude = result['lng']
                        selected_place = result
                        st.success(f"Found: {result.get('address', 'Location found')}")
                    else:
                        # Multiple results from Nominatim
                        st.session_state.map_search_results = search_result['data']
                        st.success(f"Found {len(search_result['data'])} results")
                else:
                    st.error("Location not found. Try different search terms.")
        
        # Show search results if available
        if st.session_state.map_search_results:
            st.markdown("##### Select from results:")
            for idx, res in enumerate(st.session_state.map_search_results):
                if st.button(
                    f"{res['display_name'][:100]}...",
                    key=f"search_result_{idx}",
                    use_container_width=True
                ):
                    latitude = res['lat']
                    longitude = res['lng']
                    selected_place = res
                    st.session_state.map_search_results = []  # Clear results
                    st.success("Location selected!")
                    st.rerun()
    
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