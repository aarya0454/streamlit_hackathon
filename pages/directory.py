import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import requests
from typing import List, Dict, Any, Optional

from db import list_vendors, CATEGORIES

st.set_page_config(page_title="Find a Pro | Hydro-Assess", layout="wide")

# --- Config ---
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
DEFAULT_CENTER = [20.5937, 78.9629]  # India centroid fallback
DEFAULT_ZOOM = 5
MAX_ZOOM = 20

# --- Helper functions ---

def get_place_suggestions(query: str, api_key: str, type_filter: str = "(cities)") -> List[str]:
    if not api_key or not query or len(query) < 2:
        return []
    try:
        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {
            "input": query,
            "key": api_key,
            "types": type_filter,  # '(cities)' is accepted by Places Autocomplete
        }
        r = requests.get(url, params=params, timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "OK":
                return [p.get("description", "") for p in data.get("predictions", [])]
    except Exception:
        pass
    return []


def geocode_address(address: str, api_key: str) -> Optional[Dict[str, float]]:
    if not address:
        return None
    # Try Google first
    if api_key:
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {"address": address, "key": api_key}
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data.get("status") == "OK" and data.get("results"):
                    loc = data["results"][0]["geometry"]["location"]
                    return {"lat": loc["lat"], "lng": loc["lng"]}
        except Exception:
            pass
    # Fallback to Nominatim
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": address, "format": "json", "limit": 1}
        headers = {"User-Agent": "HydroAssessDirectory/1.0"}
        r = requests.get(url, params=params, headers=headers, timeout=5)
        if r.status_code == 200 and r.json():
            item = r.json()[0]
            return {"lat": float(item["lat"]), "lng": float(item["lon"])}
    except Exception:
        pass
    return None


# --- UI ---
st.title("Find a Pro — Local Vendors & Installers")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("index.py")
with c2:
    if st.button("📣 List Your Business", use_container_width=True):
        st.switch_page("pages/list_your_business.py")
with c3:
    if st.button("🔐 Admin Dashboard", use_container_width=True):
        st.switch_page("pages/admin_directory.py")

st.markdown("---")

with st.container():
    st.subheader("Search Vendors")
    col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
    with col_a:
        city_input = st.text_input("City", placeholder="Type a city (e.g., Bengaluru)")
        if city_input and len(city_input) >= 3 and GOOGLE_API_KEY:
            suggestions = get_place_suggestions(city_input, GOOGLE_API_KEY, type_filter="(cities)")
            if suggestions:
                sel = st.selectbox("Suggestions", options=[""] + suggestions, key="city_suggestions")
                if sel:
                    city_input = sel
        elif not GOOGLE_API_KEY:
            st.caption("Tip: Add GOOGLE_API_KEY in secrets.toml to enable city suggestions")
    with col_b:
        pincode_input = st.text_input("Pincode", placeholder="Optional pincode")
        if pincode_input and len(pincode_input) >= 3 and GOOGLE_API_KEY:
            pin_suggestions = get_place_suggestions(pincode_input, GOOGLE_API_KEY, type_filter="geocode")
            # Filter predictions that look like postal codes
            pin_suggestions = [s for s in pin_suggestions if any(ch.isdigit() for ch in s)]
            if pin_suggestions:
                selp = st.selectbox("Pincode suggestions", options=[""] + pin_suggestions, key="pin_suggestions")
                if selp:
                    # Try to extract numeric pincode part
                    digits = ''.join([c for c in selp if c.isdigit()])
                    if digits:
                        pincode_input = digits
    with col_c:
        category = st.selectbox("Category", options=["All"] + CATEGORIES)
    with col_d:
        search_clicked = st.button("🔎 Search", use_container_width=True)

# Persist results across reruns
if "dir_results" not in st.session_state:
    st.session_state.dir_results = []
if "dir_center" not in st.session_state:
    st.session_state.dir_center = DEFAULT_CENTER
if "dir_zoom" not in st.session_state:
    st.session_state.dir_zoom = DEFAULT_ZOOM

if search_clicked:
    results = list_vendors(city_query=city_input or None,
                           pincode=(pincode_input or None),
                           category=category if category != "All" else None,
                           only_approved=True,
                           limit=500)
    st.session_state.dir_results = results
    # Center logic: use average vendor coords, else geocode city/pincode, else default
    coords = [(v.get("lat"), v.get("lng")) for v in results if v.get("lat") is not None and v.get("lng") is not None]
    if coords:
        avg_lat = sum([lat for lat, _ in coords]) / len(coords)
        avg_lng = sum([lng for _, lng in coords]) / len(coords)
        st.session_state.dir_center = [avg_lat, avg_lng]
        st.session_state.dir_zoom = 12
    else:
        query_addr = ", ".join([x for x in [city_input, pincode_input] if x])
        ge = geocode_address(query_addr, GOOGLE_API_KEY) if query_addr else None
        if ge:
            st.session_state.dir_center = [ge["lat"], ge["lng"]]
            st.session_state.dir_zoom = 12
        else:
            st.session_state.dir_center = DEFAULT_CENTER
            st.session_state.dir_zoom = DEFAULT_ZOOM

# --- Results ---
st.markdown("---")
results = st.session_state.dir_results

left, right = st.columns([1.3, 1])

with left:
    st.subheader("Map View")
    m = folium.Map(
        location=st.session_state.dir_center,
        zoom_start=st.session_state.dir_zoom,
        tiles=None,
        control_scale=True,
        max_zoom=MAX_ZOOM,
    )
    # Google Satellite + Hybrid like other pages
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google', name='Satellite', overlay=False, control=True, maxZoom=MAX_ZOOM
    ).add_to(m)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google', name='Hybrid', overlay=False, control=True, maxZoom=MAX_ZOOM
    ).add_to(m)
    folium.LayerControl().add_to(m)

    cluster = MarkerCluster().add_to(m)

    if results:
        for v in results:
            lat, lng = v.get("lat"), v.get("lng")
            if lat is None or lng is None:
                continue
            name = v.get("business_name") or "Vendor"
            rating = v.get("rating_avg") or 0
            cat = v.get("category") or ""
            popup_html = f"""
                <div style='min-width:200px'>
                    <div style='font-weight:700'>{name}</div>
                    <div>⭐ {rating:.1f} • {cat}</div>
                </div>
            """
            folium.Marker([lat, lng], popup=folium.Popup(popup_html, max_width=260), tooltip=name).add_to(cluster)

    st_folium(m, height=560, use_container_width=True)

with right:
    st.subheader("List View")
    if not results:
        st.info("No vendors found. Try another city/pincode or category. If you're a business, list your services!")
    else:
        for v in results:
            with st.container(border=True):
                top_col1, top_col2 = st.columns([3, 1])
                with top_col1:
                    st.markdown(f"**{v.get('business_name','Vendor')}**")
                    st.caption(f"{v.get('category','')} • ⭐ {float(v.get('rating_avg') or 0):.1f} ({int(v.get('rating_count') or 0)})")
                    addr_line = ", ".join([x for x in [v.get('city'), v.get('pincode')] if x])
                    st.write(addr_line)
                    phone = v.get('phone') or ""
                    if phone:
                        st.write(f"📞 {phone}")
                with top_col2:
                    if st.button("View Profile", key=f"view_{v['id']}"):
                        # Pass vendor id via session state and query params
                        st.session_state.selected_vendor_id = v['id']
                        try:
                            st.experimental_set_query_params(vendor_id=v['id'])
                        except Exception:
                            pass
                        st.switch_page("pages/vendor_profile.py")

st.markdown("---")
st.caption("Results show approved listings only. Reviews are moderated for quality.")
