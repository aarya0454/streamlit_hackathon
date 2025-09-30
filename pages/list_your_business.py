import streamlit as st
import requests
from typing import Optional, Dict

from db import CATEGORIES, submit_vendor_submission

st.set_page_config(page_title="List Your Business | Hydro-Assess", layout="wide")

GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")


def geocode_address(address: str, api_key: str) -> Optional[Dict[str, float]]:
    if not address:
        return None
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


st.title("List Your Business — Join the Directory")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    if st.button("← Back to Directory", use_container_width=True):
        st.switch_page("pages/directory.py")
with c2:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("index.py")

st.markdown("---")

st.info("Submit your details below. Your listing will appear after admin approval.")

with st.form("vendor_submit_form"):
    st.subheader("Business Details")
    business_name = st.text_input("Business Name", max_chars=120)
    logo_url = st.text_input("Logo URL (optional)")
    category = st.selectbox("Category", options=CATEGORIES)

    st.subheader("Contact")
    contact_person = st.text_input("Contact Person")
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    st.subheader("Location")
    address = st.text_area("Full Address")
    city = st.text_input("City")
    pincode = st.text_input("Pincode")

    col_lat, col_lng = st.columns(2)
    with col_lat:
        lat = st.number_input("Latitude (optional)", value=0.0, format="%.6f")
    with col_lng:
        lng = st.number_input("Longitude (optional)", value=0.0, format="%.6f")

    if st.form_submit_button("Detect Coordinates from Address"):
        addr_text = ", ".join([x for x in [address, city, pincode] if x])
        ge = geocode_address(addr_text, GOOGLE_API_KEY)
        if ge:
            st.session_state.vendor_lat = ge["lat"]
            st.session_state.vendor_lng = ge["lng"]
            st.success("Coordinates detected. They will be used on submit.")
        else:
            st.warning("Could not detect coordinates. You can enter them manually.")

    st.subheader("About & Gallery")
    description = st.text_area("About Us / Services")
    gallery_urls = st.text_area("Gallery image URLs (comma or newline separated)")

    submitted = st.form_submit_button("Submit for Approval")

    if submitted:
        if not business_name:
            st.error("Business Name is required.")
        else:
            lat_val = st.session_state.get("vendor_lat", None)
            lng_val = st.session_state.get("vendor_lng", None)
            if (lat and abs(lat) > 0.000001) and (lng and abs(lng) > 0.000001):
                lat_val, lng_val = float(lat), float(lng)
            data = {
                "business_name": business_name.strip(),
                "logo_url": logo_url.strip() or None,
                "category": category,
                "contact_person": contact_person.strip() or None,
                "phone": phone.strip() or None,
                "email": email.strip() or None,
                "address": address.strip() or None,
                "city": city.strip() or None,
                "pincode": pincode.strip() or None,
                "lat": lat_val,
                "lng": lng_val,
                "description": description.strip() or None,
                "gallery_urls": gallery_urls.strip() or None,
            }
            submit_vendor_submission(data)
            # Clear temp lat/lng
            st.session_state.pop("vendor_lat", None)
            st.session_state.pop("vendor_lng", None)
            st.success("Submitted! Your listing is pending admin approval.")
