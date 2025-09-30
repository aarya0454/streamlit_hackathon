import streamlit as st
from typing import Dict, Any, Optional, List

from db import (
    list_pending_vendors,
    approve_vendor,
    reject_vendor,
    list_pending_reviews,
    approve_review,
    reject_review,
    list_vendors,
    get_vendor,
    update_vendor,
    delete_vendor,
    CATEGORIES,
    add_vendor,
)

st.set_page_config(page_title="Directory Management | Hydro-Assess", layout="wide")

ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", None)

# --- Auth ---
if "admin_authed" not in st.session_state:
    st.session_state.admin_authed = False

if not st.session_state.admin_authed:
    st.title("Directory Management — Admin")
    if not ADMIN_PASSWORD:
        st.warning("Set ADMIN_PASSWORD in secrets.toml to secure this page. Using open access for now.")
        st.session_state.admin_authed = True
        st.rerun()
    pwd = st.text_input("Admin Password", type="password")
    if st.button("Login"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_authed = True
            st.success("Logged in")
            st.experimental_rerun()
        else:
            st.error("Invalid password")
    st.stop()

# --- Header ---
st.title("Directory Management")
sub1, sub2, sub3 = st.columns([1, 1, 1])
with sub1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("index.py")
with sub2:
    if st.button("🔎 Open Directory", use_container_width=True):
        st.switch_page("pages/directory.py")

st.markdown("---")

# --- Pending Approvals ---
st.subheader("Pending Vendor Submissions")
pending_vendors = list_pending_vendors()
if not pending_vendors:
    st.info("No pending vendor submissions.")
else:
    for v in pending_vendors:
        with st.expander(f"{v.get('business_name')} — {v.get('category')} | {v.get('city')}, {v.get('pincode')}"):
            cols = st.columns(3)
            with cols[0]:
                st.write(f"Contact: {v.get('contact_person') or ''}")
                st.write(f"Phone: {v.get('phone') or ''}")
                st.write(f"Email: {v.get('email') or ''}")
            with cols[1]:
                st.write(f"Address: {v.get('address') or ''}")
                st.write(f"Lat/Lng: {v.get('lat')}, {v.get('lng')}")
            with cols[2]:
                st.write(v.get("description") or "")

            c1, c2, csp, c3 = st.columns([1, 1, 3, 1])
            with c1:
                if st.button("Approve", key=f"approve_{v['id']}"):
                    approve_vendor(int(v["id"]))
                    st.success("Approved")
                    st.experimental_rerun()
            with c2:
                if st.button("Reject", key=f"reject_{v['id']}"):
                    reject_vendor(int(v["id"]))
                    st.warning("Rejected")
                    st.experimental_rerun()

st.markdown("---")

# --- Pending Reviews ---
st.subheader("Pending Reviews")
pending_reviews = list_pending_reviews()
if not pending_reviews:
    st.info("No pending reviews.")
else:
    for r in pending_reviews:
        with st.container(border=True):
            st.markdown(f"**{r.get('business_name', 'Vendor')}** — ⭐ {int(r.get('rating', 0))}")
            comment = r.get("comment") or ""
            if comment:
                st.write(comment)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Approve Review", key=f"appr_rev_{r['id']}"):
                    approve_review(int(r["id"]))
                    st.success("Review approved and rating recalculated")
                    st.experimental_rerun()
            with c2:
                if st.button("Delete Review", key=f"del_rev_{r['id']}"):
                    reject_review(int(r["id"]))
                    st.warning("Review deleted")
                    st.experimental_rerun()

st.markdown("---")

# --- Manage Vendors ---
st.subheader("Manage Vendors")
with st.expander("Search / Filter Vendors"):
    colf1, colf2, colf3, colf4 = st.columns([1, 1, 1, 1])
    with colf1:
        f_city = st.text_input("City contains")
    with colf2:
        f_pincode = st.text_input("Pincode")
    with colf3:
        f_category = st.selectbox("Category", options=["All"] + CATEGORIES)
    with colf4:
        show_all = st.checkbox("Include pending/rejected", value=True)

    if st.button("Apply Filters"):
        st.session_state.admin_vendor_filters = {
            "city": f_city,
            "pincode": f_pincode,
            "category": None if f_category == "All" else f_category,
            "only_approved": not show_all,
        }

filters = st.session_state.get("admin_vendor_filters", {
    "city": None,
    "pincode": None,
    "category": None,
    "only_approved": False,
})

vendors = list_vendors(
    city_query=filters.get("city"),
    pincode=filters.get("pincode"),
    category=filters.get("category"),
    only_approved=filters.get("only_approved", False),
    limit=500,
)

if not vendors:
    st.info("No vendors match the filters.")
else:
    for v in vendors:
        with st.expander(f"[{v.get('status')}] {v.get('business_name')} — {v.get('category')} | {v.get('city')}, {v.get('pincode')}"):
            c1, c2 = st.columns([3, 1])
            with c1:
                with st.form(f"edit_{v['id']}"):
                    name = st.text_input("Business Name", value=v.get("business_name") or "")
                    logo = st.text_input("Logo URL", value=v.get("logo_url") or "")
                    cat = st.selectbox("Category", options=CATEGORIES, index=max(0, CATEGORIES.index(v.get("category")) if v.get("category") in CATEGORIES else 0))
                    contact = st.text_input("Contact Person", value=v.get("contact_person") or "")
                    phone = st.text_input("Phone", value=v.get("phone") or "")
                    email = st.text_input("Email", value=v.get("email") or "")
                    addr = st.text_area("Address", value=v.get("address") or "")
                    city = st.text_input("City", value=v.get("city") or "")
                    pin = st.text_input("Pincode", value=v.get("pincode") or "")
                    lat = st.number_input("Latitude", value=float(v.get("lat") or 0.0), format="%.6f")
                    lng = st.number_input("Longitude", value=float(v.get("lng") or 0.0), format="%.6f")
                    desc = st.text_area("Description", value=v.get("description") or "")
                    gal = st.text_area("Gallery URLs", value=v.get("gallery_urls") or "")

                    save = st.form_submit_button("Save Changes")
                    if save:
                        update_vendor(
                            int(v["id"]),
                            {
                                "business_name": name,
                                "logo_url": logo or None,
                                "category": cat,
                                "contact_person": contact or None,
                                "phone": phone or None,
                                "email": email or None,
                                "address": addr or None,
                                "city": city or None,
                                "pincode": pin or None,
                                "lat": float(lat) if abs(lat) > 0.000001 else None,
                                "lng": float(lng) if abs(lng) > 0.000001 else None,
                                "description": desc or None,
                                "gallery_urls": gal or None,
                            },
                        )
                        st.success("Vendor updated")
                        st.experimental_rerun()
            with c2:
                st.metric("Avg Rating", f"{float(v.get('rating_avg') or 0):.1f}")
                st.metric("Reviews", int(v.get("rating_count") or 0))
                if v.get("status") != "approved":
                    if st.button("Approve", key=f"appr_v_{v['id']}"):
                        approve_vendor(int(v["id"]))
                        st.success("Approved")
                        st.experimental_rerun()
                if st.button("Delete", type="secondary", key=f"del_v_{v['id']}"):
                    delete_vendor(int(v["id"]))
                    st.warning("Vendor deleted")
                    st.experimental_rerun()

st.markdown("---")

# --- Add Vendor Manually ---
st.subheader("Add Vendor Manually")
with st.form("add_vendor_form"):
    name = st.text_input("Business Name")
    logo = st.text_input("Logo URL")
    cat = st.selectbox("Category", options=CATEGORIES)
    contact = st.text_input("Contact Person")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    addr = st.text_area("Address")
    city = st.text_input("City")
    pin = st.text_input("Pincode")
    lat = st.number_input("Latitude", value=0.0, format="%.6f")
    lng = st.number_input("Longitude", value=0.0, format="%.6f")
    desc = st.text_area("Description")
    gal = st.text_area("Gallery URLs (comma or newline separated)")

    add = st.form_submit_button("Add Vendor (Approved)")
    if add:
        data = {
            "business_name": name.strip(),
            "logo_url": logo.strip() or None,
            "category": cat,
            "contact_person": contact.strip() or None,
            "phone": phone.strip() or None,
            "email": email.strip() or None,
            "address": addr.strip() or None,
            "city": city.strip() or None,
            "pincode": pin.strip() or None,
            "lat": float(lat) if abs(lat) > 0.000001 else None,
            "lng": float(lng) if abs(lng) > 0.000001 else None,
            "description": desc.strip() or None,
            "gallery_urls": gal.strip() or None,
            "status": "approved",
        }
        add_vendor(data)
        st.success("Vendor added as approved")
        st.experimental_rerun()
