import streamlit as st
import folium
from streamlit_folium import st_folium
from typing import List, Dict, Any, Optional

from db import get_vendor, list_reviews, add_review

st.set_page_config(page_title="Vendor Profile | Hydro-Assess", layout="wide")

# --- Helpers ---

def _stars(n: int) -> str:
    n = max(0, min(5, int(n)))
    return "★" * n + "☆" * (5 - n)


def _parse_gallery(gallery_raw: Optional[str]) -> List[str]:
    if not gallery_raw:
        return []
    gallery_raw = gallery_raw.strip()
    # JSON list or comma/newline separated
    if gallery_raw.startswith("[") and gallery_raw.endswith("]"):
        try:
            import json
            arr = json.loads(gallery_raw)
            return [str(x).strip() for x in arr if str(x).strip()]
        except Exception:
            pass
    # Fallback: split by comma/newline
    parts = [p.strip() for p in gallery_raw.replace("\r", "\n").split("\n")]
    items: List[str] = []
    for p in parts:
        items.extend([x.strip() for x in p.split(",") if x.strip()])
    return items


# --- Identify vendor ---
query_params = {}
try:
    query_params = st.experimental_get_query_params()
except Exception:
    pass

vendor_id = None
if query_params.get("vendor_id"):
    try:
        vendor_id = int(query_params["vendor_id"][0])
    except Exception:
        vendor_id = None
elif "selected_vendor_id" in st.session_state:
    vendor_id = st.session_state.get("selected_vendor_id")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    if st.button("← Back to Directory", use_container_width=True):
        st.switch_page("pages/directory.py")
with c2:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("index.py")

if not vendor_id:
    st.warning("No vendor selected. Please go back to the directory.")
    st.stop()

vendor = get_vendor(int(vendor_id))
if not vendor:
    st.error("Vendor not found.")
    st.stop()

# --- Header ---
logo_url = vendor.get("logo_url")
name = vendor.get("business_name") or "Vendor"
category = vendor.get("category") or ""
avg = float(vendor.get("rating_avg") or 0)
cnt = int(vendor.get("rating_count") or 0)

colA, colB = st.columns([1, 3])
with colA:
    if logo_url:
        st.image(logo_url, width=140)
with colB:
    st.title(name)
    st.write(f"{category} • ⭐ {avg:.1f} ({cnt})")

st.markdown("---")

# --- Layout ---
left, right = st.columns([1.2, 1])

with left:
    st.subheader("Location")
    lat, lng = vendor.get("lat"), vendor.get("lng")
    if lat is not None and lng is not None:
        m = folium.Map(location=[lat, lng], zoom_start=14, tiles=None, control_scale=True)
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google', name='Satellite', overlay=False, control=True
        ).add_to(m)
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr='Google', name='Hybrid', overlay=False, control=True
        ).add_to(m)
        folium.LayerControl().add_to(m)
        folium.Marker([lat, lng], tooltip=name).add_to(m)
        st_folium(m, height=360, use_container_width=True)
    else:
        st.info("No coordinates provided for this vendor.")

    st.subheader("About Us")
    desc = vendor.get("description") or "No description provided."
    st.write(desc)

    gallery = _parse_gallery(vendor.get("gallery_urls"))
    if gallery:
        st.subheader("Gallery")
        cols = st.columns(3)
        for i, url in enumerate(gallery):
            with cols[i % 3]:
                try:
                    st.image(url, use_column_width=True)
                except Exception:
                    st.caption(url)

with right:
    st.subheader("Contact")
    person = vendor.get("contact_person") or ""
    phone = vendor.get("phone") or ""
    email = vendor.get("email") or ""
    addr = vendor.get("address") or ""
    city = vendor.get("city") or ""
    pincode = vendor.get("pincode") or ""

    if person:
        st.write(f"👤 {person}")
    if phone:
        st.markdown(f"📞 <a href='tel:{phone}'>{phone}</a>", unsafe_allow_html=True)
    if email:
        st.markdown(f"✉️ <a href='mailto:{email}'>{email}</a>", unsafe_allow_html=True)
    st.write(addr)
    st.write(" ".join([str(city), str(pincode)]).strip())

    st.markdown("---")

    st.subheader("User Reviews")
    reviews = list_reviews(vendor_id=int(vendor_id), only_approved=True)
    if not reviews:
        st.info("No reviews yet. Be the first to review!")
    else:
        for r in reviews:
            with st.container(border=True):
                st.markdown(f"**{_stars(int(r.get('rating', 0)))}**  —  {r.get('user_name') or 'Anonymous'}")
                comment = r.get("comment") or ""
                if comment:
                    st.write(comment)

    st.markdown("---")

    st.subheader("Leave a Review")
    with st.form("review_form"):
        user_name = st.text_input("Your name (optional)")
        rating = st.slider("Rating", min_value=1, max_value=5, value=5)
        comment = st.text_area("Comments", placeholder="Share your experience")
        submitted = st.form_submit_button("Submit Review")
        if submitted:
            add_review(int(vendor_id), int(rating), comment, user_name if user_name.strip() else None)
            st.success("Thank you! Your review has been submitted and is pending approval.")
