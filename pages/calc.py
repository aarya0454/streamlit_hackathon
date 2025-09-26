import streamlit as st
import pandas as pd
from translator import T, main_page_language_selector
import numpy as np
import requests
import matplotlib.pyplot as plt
# Configure matplotlib to handle Unicode characters
import matplotlib
matplotlib.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False
from datetime import datetime
# Importing our new professional PDF generator
from pdf_generator import generate_professional_pdf
import io
import base64
from shapely.geometry import Point
import geopandas as gpd
import json
import math
import os
import time
from typing import Optional, Dict

# Initialize language in session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title=T('page_title_calc'),
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for calc.py with modern, cool interactive elements
st.markdown("""
<style>
    /* Import Google Font for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global typography enhancement */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Enhanced button styling with smooth transitions */
    .stButton > button {
        color: red;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(128, 128, 128, 0.2);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover:before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        transition: transform 0.1s;
    }
    
    /* Primary button special styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, color-mix(in srgb, var(--primary-color) 85%, black) 100%);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced input fields with animated focus states */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        transition: all 0.3s ease;
        border: 1.5px solid rgba(128, 128, 128, 0.2);
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
        transform: translateY(-1px);
    }
    
    /* Enhanced selectbox with smooth transitions */
    .stSelectbox > div > div {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-color);
    }
    
    /* Metric cards with subtle animations */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(128, 128, 128, 0.1);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        border-color: var(--primary-color);
    }
    
    /* Enhanced tabs using Streamlit's native theme variables */
    .stTabs [data-baseweb="tab-list"] {
        gap: 18px;
        padding: 12px 18px;
        border-radius: 24px;
        backdrop-filter: blur(15px);
        margin-bottom: 25px;
        transition: all 0.3s ease;
        /* Use Streamlit's secondary background with enhanced styling */
        background: linear-gradient(135deg, 
            color-mix(in srgb, var(--secondary-background-color) 95%, var(--background-color) 5%) 0%, 
            color-mix(in srgb, var(--secondary-background-color) 85%, var(--background-color) 15%) 100%);
        box-shadow: 0 4px 20px color-mix(in srgb, var(--text-color) 8%, transparent 92%), 
                    inset 0 1px 0 color-mix(in srgb, var(--background-color) 50%, transparent 50%);
        border: 1px solid color-mix(in srgb, var(--text-color) 15%, transparent 85%);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 18px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
        padding: 14px 24px !important;
        min-height: 52px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex: 1 !important;
        text-align: center !important;
        font-size: 14px !important;
        letter-spacing: 0.6px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    /* Individual tabs using Streamlit theme variables */
    .stTabs [data-baseweb="tab"] {
        /* Use Streamlit's background color with enhanced styling */
        background: linear-gradient(135deg, 
            color-mix(in srgb, var(--background-color) 90%, var(--secondary-background-color) 10%) 0%, 
            color-mix(in srgb, var(--background-color) 75%, var(--secondary-background-color) 25%) 100%);
        color: var(--text-color);
        border: 1px solid color-mix(in srgb, var(--text-color) 20%, transparent 80%);
        box-shadow: 0 2px 8px color-mix(in srgb, var(--text-color) 6%, transparent 94%), 
                    inset 0 1px 0 color-mix(in srgb, var(--background-color) 70%, transparent 30%);
    }
    
    .stTabs [data-baseweb="tab"]:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.6s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px) scale(1.02);
    }
    
    /* Enhanced Hover States - More Visible */
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, 
            rgba(59, 130, 246, 0.15) 0%, 
            rgba(37, 99, 235, 0.08) 100%) !important;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.15),
                    0 4px 15px rgba(0, 0, 0, 0.1) !important;
        border-color: rgba(59, 130, 246, 0.4) !important;
        color: var(--text-color) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover:before {
        left: 100%;
    }
    
    .stTabs [aria-selected="true"] {
        transform: translateY(-2px) scale(1.05);
        animation: slideIn 0.4s ease;
        font-weight: 700 !important;
        z-index: 10;
        position: relative;
    }
    
    /* Active Tab - Enhanced Professional Styling */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, 
            #3b82f6 0%, 
            #2563eb 50%,
            #1d4ed8 100%) !important;
        color: white !important;
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.3), 
                    0 6px 20px rgba(37, 99, 235, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(59, 130, 246, 0.8) !important;
        position: relative;
        overflow: hidden;
    }
    
    /* Add a subtle shine effect to active tab */
    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.15) 50%, 
            transparent 100%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        50% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Active Tab Hover */
    .stTabs [aria-selected="true"]:hover {
        transform: translateY(-4px) scale(1.06) !important;
        box-shadow: 0 16px 50px rgba(59, 130, 246, 0.4), 
                    0 8px 25px rgba(37, 99, 235, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(135deg, 
            #4f46e5 0%, 
            #3b82f6 50%,
            #2563eb 100%) !important;
    }
    
    /* Ensure tabs container takes full width */
    .stTabs {
        width: 100%;
    }
    
    .stTabs > div {
        width: 100%;
    }
    
    /* Responsive tab styling for smaller screens */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 10px 12px !important;
            font-size: 12px !important;
            min-height: 40px !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            padding: 6px 8px;
        }
    }
    
    /* Force override Streamlit's default tab styling with maximum specificity */
    .stTabs [data-baseweb="tab"] > div,
    .stTabs [data-baseweb="tab"] > div > div,
    .stTabs [data-baseweb="tab"] span,
    .stTabs [data-baseweb="tab"] p {
        color: inherit !important;
        font-weight: inherit !important;
    }
    
    /* ACTIVE TAB TEXT - THEME AWARE COLORS */
    
    /* Light Mode Active Tab Text - Dark text for better contrast */
    [data-theme="light"] .stTabs [data-baseweb="tab"][aria-selected="true"] > div,
    [data-theme="light"] .stTabs [data-baseweb="tab"][aria-selected="true"] > div > div,
    [data-theme="light"] .stTabs [data-baseweb="tab"][aria-selected="true"] > div > div > div,
    [data-theme="light"] .stTabs [data-baseweb="tab"][aria-selected="true"] span,
    [data-theme="light"] .stTabs [data-baseweb="tab"][aria-selected="true"] p,
    [data-theme="light"] .stTabs [data-baseweb="tab"][aria-selected="true"] *,
    [data-theme="light"] .stTabs [aria-selected="true"] > div,
    [data-theme="light"] .stTabs [aria-selected="true"] > div > div,
    [data-theme="light"] .stTabs [aria-selected="true"] > div > div > div,
    [data-theme="light"] .stTabs [aria-selected="true"] span,
    [data-theme="light"] .stTabs [aria-selected="true"] p,
    [data-theme="light"] .stTabs [aria-selected="true"] *,
    .stApp:not([data-theme="dark"]) .stTabs [data-baseweb="tab"][aria-selected="true"] > div,
    .stApp:not([data-theme="dark"]) .stTabs [data-baseweb="tab"][aria-selected="true"] > div > div,
    .stApp:not([data-theme="dark"]) .stTabs [data-baseweb="tab"][aria-selected="true"] > div > div > div,
    .stApp:not([data-theme="dark"]) .stTabs [data-baseweb="tab"][aria-selected="true"] span,
    .stApp:not([data-theme="dark"]) .stTabs [data-baseweb="tab"][aria-selected="true"] p,
    .stApp:not([data-theme="dark"]) .stTabs [data-baseweb="tab"][aria-selected="true"] *,
    .stApp:not([data-theme="dark"]) .stTabs [aria-selected="true"] > div,
    .stApp:not([data-theme="dark"]) .stTabs [aria-selected="true"] > div > div,
    .stApp:not([data-theme="dark"]) .stTabs [aria-selected="true"] > div > div > div,
    .stApp:not([data-theme="dark"]) .stTabs [aria-selected="true"] span,
    .stApp:not([data-theme="dark"]) .stTabs [aria-selected="true"] p,
    .stApp:not([data-theme="dark"]) .stTabs [aria-selected="true"] * {
        color: #1e293b !important;
        font-weight: 700 !important;
    }
    
    /* Dark Mode Active Tab Text - White text */
    [data-theme="dark"] .stTabs [data-baseweb="tab"][aria-selected="true"] > div,
    [data-theme="dark"] .stTabs [data-baseweb="tab"][aria-selected="true"] > div > div,
    [data-theme="dark"] .stTabs [data-baseweb="tab"][aria-selected="true"] > div > div > div,
    [data-theme="dark"] .stTabs [data-baseweb="tab"][aria-selected="true"] span,
    [data-theme="dark"] .stTabs [data-baseweb="tab"][aria-selected="true"] p,
    [data-theme="dark"] .stTabs [data-baseweb="tab"][aria-selected="true"] *,
    [data-theme="dark"] .stTabs [aria-selected="true"] > div,
    [data-theme="dark"] .stTabs [aria-selected="true"] > div > div,
    [data-theme="dark"] .stTabs [aria-selected="true"] > div > div > div,
    [data-theme="dark"] .stTabs [aria-selected="true"] span,
    [data-theme="dark"] .stTabs [aria-selected="true"] p,
    [data-theme="dark"] .stTabs [aria-selected="true"] * {
        color: white !important;
        font-weight: 700 !important;
    }
    
    /* Fallback for systems without theme detection - use white text for better visibility */
    .stTabs [data-baseweb="tab"][aria-selected="true"] > div,
    .stTabs [data-baseweb="tab"][aria-selected="true"] > div > div,
    .stTabs [data-baseweb="tab"][aria-selected="true"] > div > div > div,
    .stTabs [data-baseweb="tab"][aria-selected="true"] span,
    .stTabs [data-baseweb="tab"][aria-selected="true"] p,
    .stTabs [aria-selected="true"] > div,
    .stTabs [aria-selected="true"] > div > div,
    .stTabs [aria-selected="true"] > div > div > div,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] p {
        color: white !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Extra specificity for dark backgrounds - force white text */
    .stTabs [data-baseweb="tab"][aria-selected="true"] *,
    .stTabs [aria-selected="true"] * {
        color: white !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Enhanced expander with smooth animations */
    .streamlit-expanderHeader {
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(128, 128, 128, 0.1);
    }
    
    /* Info, warning, error boxes with subtle animations */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
        animation: fadeIn 0.5s ease;
        backdrop-filter: blur(10px);
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Enhanced slider with smooth thumb transitions */
    .stSlider > div > div > div > div {
        transition: all 0.3s ease;
    }
    
    .stSlider > div > div > div[role="slider"] {
        transition: all 0.2s ease;
    }
    
    .stSlider > div > div > div[role="slider"]:hover {
        transform: scale(1.2);
    }
    
    /* Sidebar enhancements */
    section[data-testid="stSidebar"] {
        backdrop-filter: blur(10px);
    }
    
    section[data-testid="stSidebar"] .element-container {
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div {
        border-radius: 10px;
        overflow: hidden;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), color-mix(in srgb, var(--primary-color) 70%, white));
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* Enhanced DataFrame styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Custom recommendation box styling */
    .recommendation-box {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
        border: 2px solid rgba(76, 175, 80, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        animation: glow 3s ease-in-out infinite;
        text-align: center;
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(76, 175, 80, 0.2); }
        50% { box-shadow: 0 0 30px rgba(76, 175, 80, 0.4); }
    }
    
    /* Custom reason box styling */
    .reason-box {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.05) 0%, rgba(33, 150, 243, 0.02) 100%);
        border-left: 4px solid rgba(33, 150, 243, 0.8);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
        animation: slideInRight 0.6s ease;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Design card styling */
    .design-card {
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .design-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Cost card styling */
    .cost-card {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(255, 193, 7, 0.05) 100%);
        border: 1px solid rgba(255, 193, 7, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border-color: var(--primary-color) transparent transparent transparent;
    }
    
    /* Enhanced file uploader */
    .uploadedFile {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        background: rgba(128, 128, 128, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Add language selector to main page
main_page_language_selector()

# Navigation buttons (similar to map.py)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button(T('nav_home'), use_container_width=True, help=T('nav_home_help')):
        st.switch_page("index.py")
with col2:
    if st.button(T('nav_map'), use_container_width=True, help=T('nav_map_help')):
        st.switch_page("pages/map.py")

st.markdown("---")

if 'groundwater_gdf' not in st.session_state:
    st.session_state['groundwater_gdf'] = None
if 'data_source' not in st.session_state:
    st.session_state['data_source'] = 'simulation'
# Don't set default coordinates - let onboarding handle this
if 'coordinates_from_map' not in st.session_state:
    st.session_state['coordinates_from_map'] = False

# --- CONSTANTS ---
RUNOFF_COEFFICIENTS = {
    "Concrete Roof": 0.90,
    "Tile Roof": 0.85,
    "Metal Sheet": 0.90,
    "Asphalt": 0.85,
    "Concrete Surface": 0.75,
    "Paved Area": 0.70
}

SOIL_INFILTRATION_RATES = {
    "Sandy": 25,  # mm/hour
    "Loamy": 13,
    "Clay": 5,
    "Rocky": 2
}

# --- DATA FETCHING FUNCTIONS ---

@st.cache_data(ttl=3600)
def get_annual_rainfall(lat, lon):
    """Fetch annual rainfall data from Open-Meteo API."""
    try:
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "daily": "precipitation_sum",
            "timezone": "auto"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            precipitation = [p if p is not None else 0 for p in data['daily']['precipitation_sum']]
            return sum(precipitation)
        return None
    except Exception as e:
        st.warning(f"Could not fetch rainfall data: {e}")
        return None

@st.cache_data(ttl=3600)
def get_soil_type(lat, lon):
    """Fetch soil type from multiple sources with enhanced error handling."""
    
    # Try multiple soil APIs in order of preference
    soil_apis = [
        ("ISRIC SoilGrids", get_soil_from_isric),
        ("Alternative API", get_soil_from_alternative),
        ("Geographic Fallback", get_soil_type_fallback)
    ]
    
    for api_name, api_func in soil_apis:
        try:
            result = api_func(lat, lon)
            if result and result != "Unknown":
                return result
        except Exception as e:
            continue
    
    # Final fallback
    return "Loamy"

def get_soil_from_isric(lat, lon):
    """Get soil data from ISRIC SoilGrids API - FIXED implementation."""
    try:
        # Correct ISRIC SoilGrids REST API endpoint for point queries
        base_url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
        
        # Request clay and sand properties at 0-5cm depth
        # Use list for 'property' so requests encodes property=clay&property=sand
        params = {
            "lon": lon,
            "lat": lat,
            "property": ["clay", "sand"],  # Multiple properties in one call
            "depth": "0-5cm",
            "value": "mean"
        }
        
        headers = {
            'User-Agent': 'HydroAssess-RainwaterHarvesting/1.0',
            'Accept': 'application/json'
        }
        
        # Helper to parse a response into clay/sand percentages
        def _parse_layers(data_json):
            properties = data_json.get('properties', {})
            layers = properties.get('layers', [])
            clay_pct = None
            sand_pct = None
            for layer in layers:
                name = (layer.get('name') or '').lower()
                depths = layer.get('depths') or []
                if not depths:
                    continue
                values = (depths[0].get('values') or {})
                mean_val = values.get('mean')
                if mean_val is None:
                    continue
                # API unit is g/kg; convert to %
                pct = float(mean_val) / 10.0
                if 'clay' in name:
                    clay_pct = pct
                if 'sand' in name:
                    sand_pct = pct
            return clay_pct, sand_pct

        response = requests.get(base_url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse the response structure
            try:
                clay_content, sand_content = _parse_layers(data)
                
                # If combined query didn't return, try separate calls (some servers ignore multiple props)
                if clay_content is None or sand_content is None:
                    for prop in ["clay", "sand"]:
                        resp2 = requests.get(
                            base_url,
                            params={"lon": lon, "lat": lat, "property": prop, "depth": "0-5cm", "value": "mean"},
                            headers=headers,
                            timeout=10
                        )
                        if resp2.status_code == 200:
                            c2, s2 = _parse_layers(resp2.json())
                            if c2 is not None:
                                clay_content = c2
                            if s2 is not None:
                                sand_content = s2
                
                # Still nothing? Try the next available shallow depth as a fallback
                if clay_content is None or sand_content is None:
                    resp3 = requests.get(
                        base_url,
                        params={"lon": lon, "lat": lat, "property": "clay,sand", "depth": "5-15cm", "value": "mean"},
                        headers=headers,
                        timeout=10
                    )
                    if resp3.status_code == 200:
                        c3, s3 = _parse_layers(resp3.json())
                        if clay_content is None:
                            clay_content = c3
                        if sand_content is None:
                            sand_content = s3
                
                # Classify soil based on USDA texture triangle
                if clay_content is not None and sand_content is not None:
                    # Calculate silt content
                    silt_content = 100 - clay_content - sand_content
                    
                    # USDA soil classification logic (simplified)
                    if sand_content > 85 and clay_content < 10:
                        return 'Sandy'
                    elif clay_content >= 40:
                        return 'Clay'
                    elif clay_content >= 35 and sand_content < 45:
                        return 'Clay'
                    elif sand_content >= 70 and clay_content < 30:
                        return 'Sandy'
                    elif clay_content < 20 and silt_content < 50:
                        return 'Sandy'
                    elif clay_content < 27 and 50 <= silt_content < 80:
                        return 'Loamy'
                    elif silt_content >= 80:
                        return 'Loamy'
                    else:
                        return 'Loamy'  # Default to loamy for mixed soils
                
                return None
                
            except (KeyError, IndexError, TypeError, ValueError):
                return None
        
        elif response.status_code == 404:
            # No data available for this location
            return None
        elif response.status_code == 429:
            # Rate limited
            return None
        else:
            return None
            
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return None

def get_soil_from_alternative(lat, lon):
    """Try alternative soil classification based on elevation and climate."""
    try:
        # This is a simplified approach based on geographic patterns
        # You could integrate with other APIs here
        
        # For now, use the geographic fallback
        return get_soil_type_fallback(lat, lon)
        
    except Exception:
        return None

def get_soil_type_fallback(lat, lon):
    """Enhanced fallback soil type determination based on geographic patterns."""
    try:
        # Enhanced geographic-based soil type estimation
        
        # For India (detailed regional mapping)
        if 8.0 <= lat <= 37.0 and 68.0 <= lon <= 97.0:
            # Rajasthan desert regions - sandy
            if 24.0 <= lat <= 30.0 and 68.0 <= lon <= 78.0:
                return "Sandy"
            # Gangetic plains - alluvial/loamy
            elif 24.0 <= lat <= 31.0 and 75.0 <= lon <= 88.0:
                return "Loamy"
            # Deccan plateau - black cotton soil (clay)
            elif 15.0 <= lat <= 24.0 and 74.0 <= lon <= 80.0:
                return "Clay"
            # Western Ghats - rocky/lateritic
            elif 8.0 <= lat <= 20.0 and 72.0 <= lon <= 77.0:
                return "Rocky"
            # Eastern coastal plains - sandy/loamy
            elif 10.0 <= lat <= 20.0 and 79.0 <= lon <= 87.0:
                return "Sandy"
            # Western coastal plains - lateritic/clay
            elif 8.0 <= lat <= 23.0 and 68.0 <= lon <= 76.0:
                return "Clay"
            # Himalayan foothills - rocky/loamy
            elif lat >= 28.0:
                return "Rocky"
            # Southern peninsula - mixed
            elif lat <= 15.0:
                # Use longitude to differentiate
                if lon <= 77.0:
                    return "Rocky"  # Western side
                else:
                    return "Clay"   # Eastern side
            else:
                return "Loamy"
        
        # For other global regions
        elif lat > 40.0:  # Northern temperate regions
            return "Clay"
        elif lat < 10.0:  # Tropical regions
            if lon < 0:  # Western hemisphere tropics
                return "Sandy"
            else:  # Eastern hemisphere tropics
                return "Loamy"
        elif 10.0 <= lat <= 40.0:  # Subtropical regions
            # Arid regions (rough approximation)
            if 20.0 <= lat <= 35.0 and ((0 <= lon <= 60) or (-120 <= lon <= -90)):
                return "Sandy"
            else:
                return "Loamy"
        else:
            return "Loamy"
            
    except Exception:
        return "Loamy"

@st.cache_data(ttl=3600)
def get_monthly_rainfall(lat: float, lon: float) -> Optional[Dict[str, float]]:
    """Fetch monthly rainfall totals (mm) for the last full year (2023)."""
    try:
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "daily": "precipitation_sum",
            "timezone": "auto"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame({
                'date': pd.to_datetime(data['daily']['time']),
                'precipitation': [p or 0 for p in data['daily']['precipitation_sum']]
            })
            df['month'] = df['date'].dt.month
            monthly = df.groupby('month')['precipitation'].sum().round(1)
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            return {m: float(monthly.get(i + 1, 0.0)) for i, m in enumerate(months)}
        return None
    except Exception as e:
        st.warning(f"Could not fetch monthly rainfall data: {e}")
        return None

def get_groundwater_data(lat, lon):
    """Generate simulated groundwater data."""
    # Create realistic variation based on coordinates
    depth_base = 10 + ((lat + lon) % 15)
    seasonal_variation = 2 * np.sin((lat * lon) % 6.28)
    post_monsoon_depth = max(3, depth_base + seasonal_variation)
    
    # Determine aquifer type based on location
    if lat > 25:  # Northern India
        aquifer_type = "Alluvial Plains"
    elif lat < 20:  # Southern India
        aquifer_type = "Hard Rock (Crystalline)"
    else:
        aquifer_type = "Mixed Aquifer System"
    
    return {
        'post_monsoon_depth_m': post_monsoon_depth,
        'pre_monsoon_depth_m': post_monsoon_depth + 2,
        'principal_aquifer_type': aquifer_type,
        'aquifer_yield': 'Moderate' if post_monsoon_depth < 15 else 'Low'
    }

def query_groundwater_from_gdf(lat, lon, gdf):
    """Query groundwater data from uploaded GeoDataFrame."""
    try:
        user_point = Point(lon, lat)
        distances = gdf.geometry.distance(user_point)
        nearest_idx = distances.idxmin()
        nearest_data = gdf.loc[nearest_idx]
        return {
            'post_monsoon_depth_m': float(nearest_data.get('post_monsoon_depth_m', 12)),
            'pre_monsoon_depth_m': float(nearest_data.get('pre_monsoon_depth_m', 14)),
            'principal_aquifer_type': str(nearest_data.get('principal_aquifer_type', 'Unknown')),
            'aquifer_yield': str(nearest_data.get('aquifer_yield', 'Moderate'))
        }
    except Exception as e:
        st.warning(f"Error querying uploaded data: {e}")
        return get_groundwater_data(lat, lon)

# --- CORE RECOMMENDATION ENGINE ---

def generate_recommendation(params):
    """
    Core recommendation engine that analyzes all parameters and generates
    a specific RWH strategy recommendation.
    """
    # 1. Calculate Annual Potential (in liters)
    annual_potential = params['area'] * (params['annual_rainfall'] / 1000) * params['runoff_coefficient'] * 1000
    
    # 2. Apply Decision Rules in Order
    recommendation_type = ""
    reason = ""
    
    # Rule 1: Low Rainfall Check
    if params['annual_rainfall'] < 500:
        recommendation_type = "Storage Only"
        reason = "Annual rainfall is too low for effective groundwater recharge."
    
    # Rule 2: High Groundwater Level Check
    elif params['post_monsoon_depth_m'] < 8.0:
        recommendation_type = "Storage Only"
        reason = "Groundwater level is too high (<8m), making recharge unsafe and ineffective."
    
    # Rule 3: Urban Density Check - FIXED to allow hybrid systems
    elif params['city_type'] == "Tier 1 (Metro - High Density)":
        # Check if there's enough potential for both storage and recharge
        household_demand = params['household_size'] * 135 * 20  # 20-day buffer
        if annual_potential > household_demand * 2:  # If potential is more than 2x household demand
            recommendation_type = "Hybrid System"
            reason = "High-density urban area with sufficient rainfall potential for both storage and groundwater recharge to mitigate flooding."
        else:
            recommendation_type = "Storage Only"
            reason = "High-density urban area with limited rainfall potential - prioritizing direct water storage for household use."
    
    # Rule 4: Default - Hybrid System
    else:
        recommendation_type = "Hybrid System"
        reason = "Optimal balance of direct use and groundwater recharge."
    
    # 3. Calculate System Volumes Based on Recommendation
    if recommendation_type == "Storage Only":
        volume_to_store = annual_potential
        volume_to_recharge = 0
    elif recommendation_type == "Recharge Only":
        volume_to_store = 0
        volume_to_recharge = annual_potential
    else:  # Hybrid System
        # Calculate household demand for 20-day buffer
        demand_liters = params['household_size'] * 135 * 20  # 135 LPCD standard
        volume_to_store = min(demand_liters, annual_potential * 0.6)  # Increased from 0.5 to 0.6
        volume_to_recharge = annual_potential - volume_to_store
    
    return {
        'recommendation_type': recommendation_type,
        'reason': reason,
        'annual_potential': annual_potential,
        'volume_to_store': volume_to_store,
        'volume_to_recharge': volume_to_recharge,
        'household_demand_20_days': params['household_size'] * 135 * 20,
        'efficiency_rating': calculate_efficiency_rating(annual_potential, params)
    }

def calculate_efficiency_rating(potential, params):
    """Calculate system efficiency rating."""
    annual_household_demand = params['household_size'] * 135 * 365
    potential_coverage = (potential / annual_household_demand) * 100
    
    if potential_coverage >= 80:
        return "Excellent"
    elif potential_coverage >= 60:
        return "Good"
    elif potential_coverage >= 40:
        return "Fair"
    else:
        return "Limited"

# --- DESIGN AND COST CALCULATIONS ---

def calculate_design_and_cost(recommendation_result, params):
    """Calculate system design specifications and costs."""
    design = {}
    cost_breakdown = {}
    
    # Storage System Design
    if recommendation_result['volume_to_store'] > 0:
        tank_volume_liters = recommendation_result['volume_to_store']
        tank_volume_m3 = tank_volume_liters / 1000
        
        # Calculate optimal cylindrical tank dimensions (height ≈ diameter for efficiency)
        radius = (tank_volume_m3 / (math.pi * 1.2))**(1/3)  # Assume height = 1.2 * diameter
        diameter = radius * 2
        height = tank_volume_m3 / (math.pi * radius**2)
        
        design['storage_tank'] = {
            'volume_liters': tank_volume_liters,
            'volume_m3': tank_volume_m3,
            'dimensions': f"{diameter:.1f}m Diameter × {height:.1f}m Height",
            'type': 'Cylindrical HDPE/Concrete Tank'
        }
        
        # Storage costs (₹4 per liter for HDPE, ₹6 per liter for concrete if >5000L)
        if tank_volume_liters > 5000:
            cost_breakdown['storage_tank'] = tank_volume_liters * 6  # Concrete tank
        else:
            cost_breakdown['storage_tank'] = tank_volume_liters * 4  # HDPE tank
    
    # Recharge System Design
    if recommendation_result['volume_to_recharge'] > 0:
        recharge_volume_m3 = recommendation_result['volume_to_recharge'] / 1000
        
        # Design recharge pit (assume 2m diameter, calculate required depth)
        pit_diameter = 2.0
        pit_area = math.pi * (pit_diameter / 2)**2
        pit_depth = min(recharge_volume_m3 / pit_area, 4.0)  # Max 4m depth
        
        # If single pit is too deep, suggest multiple pits
        if recharge_volume_m3 / pit_area > 4.0:
            num_pits = math.ceil(recharge_volume_m3 / (pit_area * 4.0))
            pit_depth = 4.0
            design['recharge_system'] = {
                'volume_m3': recharge_volume_m3,
                'configuration': f"{num_pits} Recharge Pits",
                'dimensions': f"Each: {pit_diameter}m Diameter × {pit_depth}m Depth",
                'total_area': f"{num_pits * pit_area:.1f} m²"
            }
        else:
            design['recharge_system'] = {
                'volume_m3': recharge_volume_m3,
                'configuration': "Single Recharge Pit",
                'dimensions': f"{pit_diameter}m Diameter × {pit_depth:.1f}m Depth",
                'total_area': f"{pit_area:.1f} m²"
            }
        
        # Recharge costs (₹2500 per cubic meter)
        cost_breakdown['recharge_system'] = recharge_volume_m3 * 2500
    
    # Fixed Components
    cost_breakdown['first_flush_diverter'] = 3500
    cost_breakdown['filtration_system'] = 4500
    cost_breakdown['guttering_and_pipes'] = params['area'] * 15  # ₹15 per m² of catchment
    cost_breakdown['installation_labor'] = sum(cost_breakdown.values()) * 0.15  # 15% of material cost
    
    total_cost = sum(cost_breakdown.values())
    
    # Enhanced Financial Analysis - considers both storage and recharge benefits
    stored_water_m3_annual = recommendation_result['volume_to_store'] / 1000
    recharged_water_m3_annual = recommendation_result['volume_to_recharge'] / 1000
    
    # Direct savings from stored water
    direct_water_savings = stored_water_m3_annual * params['water_cost_per_m3']
    
    # Indirect benefits from groundwater recharge (estimated monetary value)
    # Benefits: reduced flooding, groundwater table improvement, reduced municipal water stress
    recharge_benefits = 0
    if recharged_water_m3_annual > 0:
        # Conservative estimate: ₹5 per m³ of recharged water in indirect benefits
        # (flood mitigation, groundwater improvement, environmental benefits)
        recharge_benefits = recharged_water_m3_annual * 5
    
    # Total annual savings/benefits
    total_annual_savings = direct_water_savings + recharge_benefits
    
    # Financial metrics
    payback_period = total_cost / total_annual_savings if total_annual_savings > 0 else float('inf')
    
    # Calculate 10-year ROI
    if payback_period != float('inf') and payback_period > 0:
        # ROI = (Total 10-year savings - Initial investment) / Initial investment * 100
        total_10_year_savings = total_annual_savings * 10
        maintenance_10_year = (total_cost * 0.02) * 10  # 2% annual maintenance for 10 years
        net_10_year_benefit = total_10_year_savings - maintenance_10_year - total_cost
        roi_10_year = (net_10_year_benefit / total_cost) * 100
    else:
        roi_10_year = -100  # Negative ROI if no payback
    
    return {
        'design': design,
        'cost_breakdown': cost_breakdown,
        'total_cost': total_cost,
        'annual_savings': total_annual_savings,  # Now includes both direct and indirect benefits
        'direct_water_savings': direct_water_savings,
        'recharge_benefits': recharge_benefits,
        'payback_period_years': payback_period,
        'roi_10_year': roi_10_year,  # Added missing ROI calculation
        'flood_mitigation_benefit': recommendation_result['volume_to_recharge'] > 0,
        'groundwater_recharge_m3_annual': recharged_water_m3_annual,
        'maintenance_cost_annual': total_cost * 0.02  # 2% of system cost annually
    }

# --- PDF REPORT GENERATION ---

def safe_pdf_text(text):
    """Convert text to ASCII-safe format for PDF generation"""
    # If the current language is not English, use transliteration or fallback
    if st.session_state.get('language', 'en') != 'en':
        # For now, return the English version or a simplified version
        # This is a workaround for PDF Unicode issues
        try:
            # Try to encode as latin-1 (PDF standard)
            text.encode('latin-1')
            return text
        except:
            # Return a placeholder or English version
            return text.encode('ascii', 'ignore').decode('ascii')
    return text

# Old FPDF class removed - now using ReportLab-based generator in pdf_generator.py
# which provides better Unicode support for Hindi, Tamil, and other languages

# The following HydroAssessPDF class has been commented out and replaced by ReportLab
"""



# """
# def generate_pdf_report_old(params, recommendation, design_financial, site_data, charts: Optional[Dict[str, plt.Figure]] = None):
#     # This function has been replaced by generate_professional_pdf in pdf_generator.py
#     # which provides better Unicode support and professional layout
#     pdf = HydroAssessPDF()
#     pdf.add_page()
    
#     # Add all text-based sections (your existing code for this is fine)
#     pdf.add_recommendation_section(recommendation)
#     pdf.add_design_section(design_financial)
#     pdf.add_cost_analysis(design_financial)
    
#     # Site data section
#     pdf.chapter_title(T('results_site_characteristics').upper())
#     pdf.set_font('Helvetica', 'B', 11)
#     pdf.cell(0, 8, T('results_location_data'), 0, 1, 'L')
#     pdf.ln(3)
#     site_info_left = [
#         (T('results_coordinates').replace(':', ''), f"{params['latitude']:.4f}°N, {params['longitude']:.4f}°E"),
#         (T('results_catchment_area_label').replace(':', ''), f"{params['area']:,.0f} m²"),
#         (T('results_surface_type_label').replace(':', ''), params['surface_type']),
#         (T('results_runoff_coefficient_label').replace(':', ''), f"{params['runoff_coefficient']:.2f}"),
#         (T('results_city_classification_label').replace(':', ''), params['city_type']),
#     ]
#     site_info_right = [
#         (T('results_annual_rainfall_label').replace(':', ''), f"{params['annual_rainfall']:.0f} mm"),
#         (T('results_soil_classification').replace(':', ''), site_data['soil_type']),
#         (T('results_groundwater_post').replace(':', ''), f"{site_data['post_monsoon_depth_m']:.1f} m bgl"),
#         (T('results_aquifer_type').replace(':', ''), site_data['principal_aquifer_type']),
#         (T('results_household_size_label').replace(':', ''), f"{params['household_size']} persons")
#     ]
#     y_start = pdf.get_y()
#     pdf.set_font('Helvetica', '', 9)
#     for i, (label, value) in enumerate(site_info_left):
#         pdf.set_xy(10, y_start + i * 7)
#         pdf.set_font('Helvetica', 'B', 9)
#         pdf.cell(45, 6, label + ":", 0, 0, 'L')
#         pdf.set_font('Helvetica', '', 9)
#         pdf.cell(45, 6, str(value), 0, 1, 'L')
#     for i, (label, value) in enumerate(site_info_right):
#         pdf.set_xy(105, y_start + i * 7)
#         pdf.set_font('Helvetica', 'B', 9)
#         pdf.cell(45, 6, label + ":", 0, 0, 'L')
#         pdf.set_font('Helvetica', '', 9)
#         pdf.cell(45, 6, str(value), 0, 1, 'L')
#     pdf.set_y(y_start + max(len(site_info_left), len(site_info_right)) * 7)
#     pdf.ln(10)
    
#     # Add implementation guidelines & other sections
#     pdf.add_page()
#     pdf.chapter_title("IMPLEMENTATION & MAINTENANCE")
#     # (Your existing code for these sections would go here)
#     pdf.set_font('Helvetica', '', 10)
#     pdf.multi_cell(0, 5, "Placeholder for implementation guidelines and maintenance schedules...")
#     pdf.ln(10)

#     # --- FIX: HANDLE CHARTS IN MEMORY TO AVOID FILE I/O ---
#     if charts:
#         pdf.add_page()
#         pdf.chapter_title("HYDROLOGICAL & FINANCIAL ANALYTICS")

#         # Process rainfall chart in memory
#         if charts.get('rainfall_chart') is not None:
#             with io.BytesIO() as buf:
#                 charts['rainfall_chart'].savefig(buf, format='PNG', dpi=120, bbox_inches='tight')
#                 buf.seek(0)
#                 # Pass the buffer directly using the 'name' parameter
#                 pdf.image(name=buf, x=10, w=190)
#             pdf.ln(5)

#         # Process cost chart in memory
#         if charts.get('cost_chart') is not None:
#             with io.BytesIO() as buf:
#                 charts['cost_chart'].savefig(buf, format='PNG', dpi=120, bbox_inches='tight')
#                 buf.seek(0)
#                 pdf.image(name=buf, x=10, w=95)
        
#         # Process savings chart in memory
#         if charts.get('savings_chart') is not None:
#             with io.BytesIO() as buf:
#                 charts['savings_chart'].savefig(buf, format='PNG', dpi=120, bbox_inches='tight')
#                 buf.seek(0)
#                 pdf.image(name=buf, x=110, w=95)

#     # --- FIX: SIMPLIFY AND ROBUSTLY OUTPUT PDF BYTES ---
#     # Assuming `fpdf2` is in requirements.txt, this is the correct way.
#     try:
#     # Explicitly convert the bytearray to bytes
#         return bytes(pdf.output())
#     except Exception as e:
#         st.error(f"Failed during the final PDF output stage: {e}")
#         return b"" # Return empty bytes to prevent downstream errors
# """
# # End of old FPDF code - now using ReportLab in pdf_generator.py


# --- STREAMLIT UI ---

def show_onboarding():
    """Show onboarding flow for new users or users coming from map"""
    
    if st.session_state.get('came_from_map', False):
        st.markdown("### 🎉 Welcome from the Map!")
        st.info("Great! We have your location and area details. Let's complete your setup with a few more details.")
        
        # Show current location info
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📍 Location", f"{st.session_state.latitude:.4f}°N, {st.session_state.longitude:.4f}°E")
        with col2:
            st.metric("📐 Area", f"{st.session_state.area:,.0f} m²")
        
        st.markdown("---")
        st.markdown("### 🏠 Complete Your Setup")
        
        # Only ask for missing information
        col1, col2 = st.columns(2)
        with col1:
            household_size = st.number_input(f"👪 {T('calc_household_size')}", min_value=1, max_value=15, value=4, step=1)
        with col2:
            water_cost_per_m3 = st.number_input(f"💧 {T('calc_water_cost')}", min_value=10.0, value=25.0, step=1.0)
        
        city_type = st.selectbox(f"🏙️ {T('calc_city_classification')}", 
                               [T('calc_city_tier2'), T('calc_city_tier1')])
        
        if st.button("✅ Complete Setup", type="primary", use_container_width=True):
            # Save the additional information
            st.session_state['household_size'] = household_size
            st.session_state['water_cost_per_m3'] = water_cost_per_m3
            st.session_state['city_type'] = city_type
            st.session_state['calc_onboarding_complete'] = True
            st.session_state['came_from_map'] = False
            st.success("🎉 Setup complete! Redirecting to assessment...")
            time.sleep(1)
            st.rerun()
    
    else:
        # Fresh user - ask for everything
        st.markdown("### 🌟 Welcome to Hydro-Assess!")
        st.markdown("Let's set up your rainwater harvesting assessment in a few simple steps.")
        
        # Step 1: Location
        st.markdown("#### 📍 Step 1: Location Setup")
        location_method = st.radio("How would you like to set your location?", 
                                 ["🛰️ Use GPS", "🗺️ Use Interactive Map", "📝 Enter Manually"],
                                 horizontal=True)
        
        latitude, longitude = None, None
        
        if location_method == "🛰️ Use GPS":
            try:
                from streamlit_geolocation import streamlit_geolocation
                
                # Initialize GPS state for onboarding
                if 'onboard_gps_attempt' not in st.session_state:
                    st.session_state.onboard_gps_attempt = 0
                
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
                    st.session_state.coordinates_from_map = False
                    if source == 'ip':
                        st.info("📍 Using approximate location (IP-based)")
                    else:
                        st.success("✅ GPS acquired and applied")
                else:
                    if st.button("📍 Get Location", use_container_width=True):
                        st.session_state.onboard_gps_attempt += 1
                        st.rerun()
                            
            except ImportError:
                st.error("GPS functionality requires 'streamlit-geolocation' package.")
                st.code("pip install streamlit-geolocation")
                
        elif location_method == "🗺️ Use Interactive Map":
            st.info("💡 **Tip:** Use our interactive map to select your location and measure area precisely!")
            if st.button("🗺️ Open Interactive Map", type="primary"):
                st.switch_page("pages/map.py")
                
        else:  # Manual entry
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", value=28.9845, format="%.6f")
            with col2:
                longitude = st.number_input("Longitude", value=77.7064, format="%.6f")
            st.session_state.coordinates_from_map = False  # Mark as manual coordinates
        
        # Step 2: Area and Surface Type
        st.markdown("#### 📐 Step 2: Area & Surface Details")
        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input(T('calc_catchment_area'), min_value=1.0, value=150.0, step=10.0)
        with col2:
            surface_type = st.selectbox(T('calc_surface_type'), list(RUNOFF_COEFFICIENTS.keys()))
        
        # Step 3: Household Details
        st.markdown("#### 🏠 Step 3: Household Information")
        col1, col2 = st.columns(2)
        with col1:
            household_size = st.number_input(f"👪 {T('calc_household_size')}", min_value=1, max_value=15, value=4, step=1)
        with col2:
            city_type = st.selectbox(f"🏙️ {T('calc_city_classification')}", 
                                   [T('calc_city_tier2'), T('calc_city_tier1')])
        
        water_cost_per_m3 = st.number_input(f"💧 {T('calc_water_cost')}", min_value=10.0, value=25.0, step=1.0)
        
        # Complete setup button
        st.markdown("---")
        can_proceed = latitude is not None and longitude is not None and area > 0
        
        if not can_proceed:
            st.warning("⚠️ Please set your location to continue.")
        
        if st.button("🚀 Start Assessment", type="primary", disabled=not can_proceed, use_container_width=True):
            # Save all information to session state
            st.session_state['latitude'] = latitude
            st.session_state['longitude'] = longitude
            st.session_state['area'] = area
            st.session_state['surface_type'] = surface_type
            st.session_state['household_size'] = household_size
            st.session_state['city_type'] = city_type
            st.session_state['water_cost_per_m3'] = water_cost_per_m3
            st.session_state['calc_onboarding_complete'] = True
            st.session_state['came_from_map'] = False
            
            st.success("🎉 Setup complete! Loading your personalized assessment...")
            time.sleep(1)
            st.rerun()

def show_location_update_prompt():
    """Show prompt when user updates location from map after completing onboarding"""
    st.markdown("### 🗺️ Location Updated!")
    st.info("We detected you've selected a new location from the map. Would you like to update your assessment?")
    
    # Show the new location details
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📍 New Location", f"{st.session_state.latitude:.4f}°N, {st.session_state.longitude:.4f}°E")
    with col2:
        st.metric("📐 New Area", f"{st.session_state.area:,.0f} m²")
    
    # Show current settings for reference
    with st.expander("🔍 Current Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Household Size:** {st.session_state.get('household_size', 4)} persons")
            st.write(f"**Surface Type:** {st.session_state.get('surface_type', 'Concrete Roof')}")
        with col2:
            st.write(f"**City Type:** {st.session_state.get('city_type', 'Tier 2 & 3 (Lower Density)')}")
            st.write(f"**Water Cost:** ₹{st.session_state.get('water_cost_per_m3', 25.0)} per m³")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("✅ Use New Location", type="primary", use_container_width=True):
            # Keep the new coordinates and continue with existing settings
            st.success("🎉 Location updated! Refreshing assessment...")
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("🔄 Update All Settings", use_container_width=True):
            # Reset onboarding to allow full reconfiguration
            st.session_state['calc_onboarding_complete'] = False
            st.session_state['came_from_map'] = True
            st.info("🔧 Redirecting to setup...")
            time.sleep(1)
            st.rerun()
    
    with col3:
        if st.button("❌ Keep Old Location", use_container_width=True):
            # Restore previous coordinates
            if st.session_state['last_map_coordinates']:
                prev_coords = st.session_state['last_map_coordinates']
                st.session_state.latitude = prev_coords[0]
                st.session_state.longitude = prev_coords[1] 
                st.session_state.area = prev_coords[2]
            st.info("🔄 Restored previous location...")
            time.sleep(1)
            st.rerun()

def main():
    st.title(f"💧 {T('app_name')} | {T('calc_title_suffix')}")
    
    # Initialize session state for onboarding
    if 'calc_onboarding_complete' not in st.session_state:
        st.session_state['calc_onboarding_complete'] = False
    if 'came_from_map' not in st.session_state:
        st.session_state['came_from_map'] = False
    if 'last_map_coordinates' not in st.session_state:
        st.session_state['last_map_coordinates'] = None
    
    # Check if user came from map with new data
    current_map_coords = None
    has_map_coordinates = (hasattr(st.session_state, 'latitude') and 
                          hasattr(st.session_state, 'longitude') and 
                          hasattr(st.session_state, 'area') and 
                          st.session_state.get('coordinates_from_map', False))
    
    if has_map_coordinates:
        current_map_coords = (st.session_state.latitude, st.session_state.longitude, st.session_state.area)
    
    # Only process coordinate changes if they came from map selection
    if (current_map_coords and 
        st.session_state.get('coordinates_from_map', False) and 
        current_map_coords != st.session_state.get('last_map_coordinates')):
        
        st.session_state['came_from_map'] = True
        st.session_state['last_map_coordinates'] = current_map_coords
        
        # If user already completed onboarding but has new map data, show update prompt
        if st.session_state['calc_onboarding_complete']:
            show_location_update_prompt()
            return
    
    # Check if user came from map (has location data but onboarding not complete)
    if (has_map_coordinates and not st.session_state['calc_onboarding_complete']):
        st.session_state['came_from_map'] = True
    
    # Show onboarding if not completed
    if not st.session_state['calc_onboarding_complete']:
        show_onboarding()
        return
    
    # Main dashboard after onboarding
    st.markdown(f"### {T('calc_dashboard_title')}")
    
    # Sidebar: Master Controls (simplified after onboarding)
    st.sidebar.header(f"📍 {T('calc_site_parameters')}")
    latitude = st.sidebar.number_input(T('calc_latitude'), value=st.session_state.get('latitude', 28.9845), format="%.6f")
    longitude = st.sidebar.number_input(T('calc_longitude'), value=st.session_state.get('longitude', 77.7064), format="%.6f")
    # Ensure area value is not less than min_value to avoid Streamlit error
    current_area = st.session_state.get('area', 150.0)
    area_value = max(1.0, current_area)  # Ensure minimum value
    area = st.sidebar.number_input(T('calc_catchment_area'), min_value=1.0, value=area_value, step=1.0)
    
    surface_type = st.sidebar.selectbox(T('calc_surface_type'), list(RUNOFF_COEFFICIENTS.keys()), 
                                       index=list(RUNOFF_COEFFICIENTS.keys()).index(st.session_state.get('surface_type', 'Concrete Roof')))
    runoff_coefficient = RUNOFF_COEFFICIENTS[surface_type]
    
    st.sidebar.markdown("---")
    st.sidebar.header(f"👪 {T('calc_household_city')}")
    household_size = st.sidebar.slider(T('calc_household_size'), 1, 15, st.session_state.get('household_size', 4))
    city_type = st.sidebar.selectbox(T('calc_city_classification'), 
                                   [T('calc_city_tier2'), T('calc_city_tier1')],
                                   index=0 if st.session_state.get('city_type', T('calc_city_tier2')) == T('calc_city_tier2') else 1)
    water_cost_per_m3 = st.sidebar.number_input(T('calc_water_cost'), min_value=10.0, 
                                               value=st.session_state.get('water_cost_per_m3', 25.0), step=1.0)
    
    # Reset onboarding button
    if st.sidebar.button(T('calc_reset_setup'), help=T('calc_reset_help')):
        st.session_state['calc_onboarding_complete'] = False
        st.session_state['came_from_map'] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.header(T('calc_data_enhancements'))
    
    # Chart theme selector
    chart_theme = st.sidebar.selectbox(
        T('calc_chart_theme'),
        ["Auto (Match Streamlit)", "Light Mode", "Dark Mode"],
        index=0,
        help=T('calc_chart_theme_help')
    )
    st.session_state.chart_theme = chart_theme
    
    # Show current theme info
    st.sidebar.caption(f"Current selection: {chart_theme}")
    if chart_theme == "Auto (Match Streamlit)":
        st.sidebar.caption("💡 Try selecting 'Dark Mode' or 'Light Mode' manually if auto-detection isn't working")
    try:
        from streamlit_geolocation import streamlit_geolocation  # type: ignore
        loc = streamlit_geolocation()
        
        # Show warning if coordinates came from map
        if st.session_state.get('coordinates_from_map', False):
            st.sidebar.info("📍 Using coordinates from map selection")
            st.sidebar.caption("GPS override disabled to preserve map selection")
            if st.sidebar.button("🔄 Switch to GPS", help="Allow GPS to override map coordinates"):
                st.session_state.coordinates_from_map = False
                st.rerun()
            use_gps = False
        else:
            use_gps = st.sidebar.checkbox(T('calc_use_gps'), value=False, key="use_gps_checkbox")
        
        if use_gps and loc and loc.get('latitude') is not None and loc.get('longitude') is not None:
            # Only update if not using map coordinates
            if not st.session_state.get('coordinates_from_map', False):
                latitude = float(loc['latitude'])
                longitude = float(loc['longitude'])
                st.sidebar.success(f"GPS set: {latitude:.6f}, {longitude:.6f}")
    except Exception:
        st.sidebar.caption("Install 'streamlit-geolocation' to enable GPS.")
    
    uploaded_file = st.sidebar.file_uploader(T('calc_upload_geojson'), type=['geojson'])
    if uploaded_file:
        try:
            gdf = gpd.read_file(uploaded_file)
            required_cols = ['post_monsoon_depth_m', 'principal_aquifer_type']
            if all(col in gdf.columns for col in required_cols):
                st.session_state.groundwater_gdf = gdf
                st.session_state.data_source = 'uploaded'
                st.sidebar.success(f"Loaded {len(gdf)} groundwater points")
            else:
                st.sidebar.error(f"Missing required columns: {required_cols}")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
    else:
        st.session_state.data_source = 'simulation'
    
    # Persist basics
    st.session_state.latitude = latitude
    st.session_state.longitude = longitude
    st.session_state.area = area
    st.session_state.surface_type = surface_type
    st.session_state.runoff_coefficient = runoff_coefficient
    st.session_state.household_size = household_size
    st.session_state.city_type = city_type
    st.session_state.water_cost_per_m3 = water_cost_per_m3
    
    # Instant recalculation pipeline
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'area': area,
        'surface_type': surface_type,
        'runoff_coefficient': runoff_coefficient,
        'household_size': household_size,
        'city_type': city_type,
        'water_cost_per_m3': water_cost_per_m3
    }
    
    # Ensure both APIs use the same coordinates
    current_lat, current_lon = latitude, longitude
    
    # Debug: Show which coordinates are being used for API calls
    if st.session_state.get('coordinates_from_map', False):
        st.sidebar.success(f"🗺️ Using map coordinates: {current_lat:.4f}°N, {current_lon:.4f}°E")
    else:
        st.sidebar.info(f"📍 Using coordinates: {current_lat:.4f}°N, {current_lon:.4f}°E")
    
    # Show API status
    with st.sidebar.expander(T('calc_api_status'), expanded=False):
        st.write(f"**{T('calc_data_sources')}**")
        st.write("• Rainfall: Open-Meteo API")
        st.write("• Soil: ISRIC SoilGrids API")
        st.write("• Coordinates: " + ("Map Selection" if st.session_state.get('coordinates_from_map', False) else "GPS/Manual"))
    
    # Get rainfall data with status tracking
    params['annual_rainfall'] = get_annual_rainfall(current_lat, current_lon)
    if params['annual_rainfall'] is None:
        st.error("Could not fetch rainfall data. Please check your internet connection and try again.")
        st.stop()
    
    soil_type = get_soil_type(current_lat, current_lon)
    
    # Display soil type result with proper API status tracking
    with st.sidebar.expander(T('calc_detected_soil'), expanded=False):
        st.write(f"**{T('calc_soil_type')}** {soil_type}")
        st.write(f"**{T('calc_infiltration_rate')}** {SOIL_INFILTRATION_RATES.get(soil_type, 13)} mm/hour")
        
        # Show the actual source of the soil data
        with st.spinner("Checking soil data source..."):
            api_result = get_soil_from_isric(current_lat, current_lon)
            
            if api_result and api_result != "Unknown":
                if api_result == soil_type:
                    st.success("✅ Retrieved from ISRIC SoilGrids API")
                else:
                    st.success(f"✅ ISRIC API returned: {api_result}")
                    st.info(f"📊 Currently using: {soil_type}")
            else:
                # Check if it matches geographic analysis
                geo_result = get_soil_type_fallback(current_lat, current_lon)
                if soil_type == geo_result:
                    st.info("📍 Determined using geographic analysis")
                    st.caption("⚠️ ISRIC API data not available for this location")
                else:
                    st.warning("🔄 Using fallback estimate")
                    st.caption("API and geographic analysis both unavailable")
        
        # Add a button to force refresh soil data
        if st.button("🔄 Refresh Soil Data", key="refresh_soil"):
            st.cache_data.clear()
            st.rerun()
    
    monthly_rainfall = get_monthly_rainfall(current_lat, current_lon) or {m: 0.0 for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}
    
    if st.session_state.data_source == 'uploaded' and st.session_state.groundwater_gdf is not None:
        groundwater_data = query_groundwater_from_gdf(current_lat, current_lon, st.session_state.groundwater_gdf)
        data_source_msg = "Using uploaded groundwater data"
    else:
        groundwater_data = get_groundwater_data(current_lat, current_lon)
        data_source_msg = "Using simulated groundwater data"
    params.update(groundwater_data)
    
    recommendation = generate_recommendation(params)
    design_financial = calculate_design_and_cost(recommendation, params)

    # Calculate and store household coverage percentage for PDF generation
    household_coverage_pct = (recommendation['annual_potential'] / (params['household_size'] * 135 * 365)) * 100
    recommendation['household_coverage_percent'] = min(household_coverage_pct, 100)  # Cap at 100%
    
    # Simplified theme detection for charts
    def get_streamlit_theme_colors():
        """Get colors based on Streamlit's active theme configuration"""
        import streamlit as st
        
        # Check manual theme selection first
        chart_theme = st.session_state.get('chart_theme', 'Auto (Match Streamlit)')
        
        if chart_theme == 'Dark Mode':
            return get_dark_theme_colors()
        elif chart_theme == 'Light Mode':
            return get_light_theme_colors()
        else:  # Auto mode - use a more reliable detection method
            try:
                # Try to access Streamlit's theme configuration
                from streamlit import config
                
                # Get background color to determine theme
                bg_color = config.get_option('theme.backgroundColor')
                primary_color = config.get_option('theme.primaryColor')
                text_color = config.get_option('theme.textColor')
                secondary_bg = config.get_option('theme.secondaryBackgroundColor')
                
                # Debug: Show what colors we're getting
                st.sidebar.write(f"Debug - BG: {bg_color}, Primary: {primary_color}")
                
                # Check if it's dark theme based on background color
                if bg_color and (bg_color.upper() == '#1A1F2E' or bg_color.upper() == '#0E1117'):
                    # Dark theme detected - use config_dark.toml colors
                    return {
                        'bg_color': bg_color,
                        'text_color': text_color or '#E8EAED',
                        'grid_color': secondary_bg or '#242B3D',
                        'primary_bar': primary_color or '#00D4FF',
                        'secondary_bar': '#F59E0B',
                        'edge_color': secondary_bg or '#242B3D'
                    }
                else:
                    # Light theme detected - use config.toml colors
                    return {
                        'bg_color': bg_color or '#FAFBFC',
                        'text_color': text_color or '#1E2329',
                        'grid_color': secondary_bg or '#F0F2F5',
                        'primary_bar': primary_color or '#0066CC',
                        'secondary_bar': '#FFA500',
                        'edge_color': text_color or '#1E2329'
                    }
                    
            except Exception as e:
                # If config reading fails, default to light theme
                st.sidebar.write(f"Config error: {e}")
                return get_light_theme_colors()
    
    def get_dark_theme_colors():
        """Colors matching config_dark.toml"""
        return {
            'bg_color': '#1A1F2E',  # backgroundColor from config_dark.toml
            'text_color': '#E8EAED',  # textColor from config_dark.toml
            'grid_color': '#242B3D',  # secondaryBackgroundColor from config_dark.toml
            'primary_bar': '#00D4FF',  # primaryColor from config_dark.toml
            'secondary_bar': '#F59E0B',  # Complementary amber color
            'edge_color': '#242B3D'
        }
    
    def get_light_theme_colors():
        """Colors matching config.toml"""
        return {
            'bg_color': '#FAFBFC',  # backgroundColor from config.toml
            'text_color': '#1E2329',  # textColor from config.toml
            'grid_color': '#F0F2F5',  # secondaryBackgroundColor from config.toml
            'primary_bar': '#0066CC',  # primaryColor from config.toml
            'secondary_bar': '#FFA500',  # Complementary orange color
            'edge_color': '#1E2329'
        }
    
    theme_colors = get_streamlit_theme_colors()
    
    # Build figures for analytics and PDF with theme-aware styling
    # Rainfall chart
    fig_rain, ax_rain = plt.subplots(figsize=(10, 6))
    fig_rain.patch.set_facecolor(theme_colors['bg_color'])
    ax_rain.set_facecolor(theme_colors['bg_color'])
    
    months = list(monthly_rainfall.keys())
    values = list(monthly_rainfall.values())
    colors = [theme_colors['primary_bar'] if v >= (np.mean(values) if len(values) else 0) else theme_colors['secondary_bar'] for v in values]
    bars = ax_rain.bar(months, values, color=colors, edgecolor=theme_colors['edge_color'], linewidth=1, alpha=0.8)
    
    ax_rain.set_xlabel('Month', fontsize=12, fontweight='bold', color=theme_colors['text_color'])
    ax_rain.set_ylabel('Rainfall (mm)', fontsize=12, fontweight='bold', color=theme_colors['text_color'])
    ax_rain.set_title('Monthly Rainfall Distribution (2023)', fontsize=14, fontweight='bold', color=theme_colors['text_color'])
    ax_rain.grid(axis='y', alpha=0.3, linestyle='--', color=theme_colors['grid_color'])
    ax_rain.tick_params(colors=theme_colors['text_color'])
    ax_rain.spines['bottom'].set_color(theme_colors['text_color'])
    ax_rain.spines['left'].set_color(theme_colors['text_color'])
    ax_rain.spines['top'].set_visible(False)
    ax_rain.spines['right'].set_visible(False)
    
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax_rain.text(bar.get_x() + bar.get_width()/2., height, f'{value:.0f}', 
                    ha='center', va='bottom', fontsize=9, color=theme_colors['text_color'], fontweight='bold')
    plt.tight_layout()
    
    # Cost breakdown chart - Enhanced styling with theme support
    costs = design_financial['cost_breakdown']
    filtered_costs = {k: v for k, v in costs.items() if v > 0}
    fig_cost, ax_cost = plt.subplots(figsize=(10, 8))
    fig_cost.patch.set_facecolor(theme_colors['bg_color'])
    ax_cost.set_facecolor(theme_colors['bg_color'])
    
    if filtered_costs:
        # Dynamic theme-aware professional color palette
        is_dark_theme = theme_colors['bg_color'].lower() in ['#1a1f2e', '#0e1117', '#262730']
        
        if is_dark_theme:  # Dark mode colors - brighter and more vibrant
            custom_colors = [
                theme_colors['primary_bar'],  # Primary theme color
                '#ffb74d',  # Light Orange
                '#81c784',  # Light Green
                '#f06292',  # Light Pink
                '#ba68c8',  # Light Purple
                '#4db6ac',  # Light Teal
                '#ffcc02',  # Light Yellow
                '#ff8a65',  # Light Deep Orange
            ]
        else:  # Light mode colors - deeper and more professional
            custom_colors = [
                theme_colors['primary_bar'],  # Primary theme color
                theme_colors['secondary_bar'],  # Secondary theme color
                '#2E8B57',  # Sea Green
                '#4682B4',  # Steel Blue
                '#FF6347',  # Tomato
                '#9370DB',  # Medium Purple
                '#20B2AA',  # Light Sea Green
                '#DC143C',  # Crimson
            ]
        
        labels = [k.replace('_', ' ').title() for k in filtered_costs.keys()]
        values = list(filtered_costs.values())
        
        # Use custom colors, cycling through if needed
        colors = [custom_colors[i % len(custom_colors)] for i in range(len(values))]
        
        # Create enhanced pie chart
        wedges, texts, autotexts = ax_cost.pie(
            values, 
            labels=labels, 
            autopct=lambda pct: f'{pct:.1f}%' if pct <= 5 else f'{pct:.1f}%\n(₹{pct/100 * sum(values)/1000:.0f}K)',
            colors=colors, 
            startangle=90,
            explode=[0.05 if v == max(values) else 0 for v in values],  # Explode the largest slice
            shadow=True,
            wedgeprops=dict(width=0.8, edgecolor=theme_colors['edge_color'], linewidth=2)
        )
        
        ax_cost.set_title('System Cost Distribution', fontsize=16, fontweight='bold', 
                         pad=20, color=theme_colors['text_color'])
        
        # Improve text styling with theme colors
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
            text.set_color(theme_colors['text_color'])
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        # Add a legend with cost values
        legend_labels = [f'{label}: ₹{value/1000:.0f}K ({value/sum(values)*100:.1f}%)' 
                       for label, value in zip(labels, values)]
        legend = ax_cost.legend(wedges, legend_labels, title="Components", loc="center left", 
                               bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
        legend.get_title().set_color(theme_colors['text_color'])
        for text in legend.get_texts():
            text.set_color(theme_colors['text_color'])
        
        ax_cost.axis('equal')
        plt.tight_layout()
    
    # Savings projection chart - Enhanced styling with theme support
    fig_save, ax_save = plt.subplots(figsize=(10, 6))
    fig_save.patch.set_facecolor(theme_colors['bg_color'])
    ax_save.set_facecolor(theme_colors['bg_color'])
    
    years = list(range(1, 11))
    annual_savings_arr = [design_financial['annual_savings']] * 10
    annual_maintenance_arr = [design_financial['maintenance_cost_annual']] * 10
    net_annual = [s - m for s, m in zip(annual_savings_arr, annual_maintenance_arr)]
    cumulative_savings = np.cumsum(net_annual)
    
    # Dynamic theme-aware colors for savings chart
    is_dark_theme = theme_colors['bg_color'].lower() in ['#1a1f2e', '#0e1117', '#262730']
    
    if is_dark_theme:
        savings_color = theme_colors['primary_bar']  # Use theme primary color
        investment_color = '#ff8a65'  # Light orange for dark mode
    else:
        savings_color = theme_colors['primary_bar']  # Use theme primary color
        investment_color = '#DC143C'  # Dark red for light mode
    
    bars = ax_save.bar(years, cumulative_savings, alpha=0.8, color=savings_color, 
                      label='Cumulative Net Savings', edgecolor=theme_colors['edge_color'], linewidth=1)
    
    # Add investment line with better styling
    ax_save.axhline(y=design_financial['total_cost'], color=investment_color, linestyle='--', 
                   linewidth=2.5, label='Initial Investment', alpha=0.9)
    
    # Find and mark payback period if within 10 years
    investment = design_financial['total_cost']
    payback_year = next((i+1 for i, val in enumerate(cumulative_savings) if val >= investment), None)
    if payback_year and payback_year <= 10:
        # Use the same color as investment line for consistency
        marker_color = investment_color
        ax_save.plot(payback_year, investment, 'o', color=marker_color, markersize=8, 
                    markeredgecolor='white', markeredgewidth=2)
        ax_save.annotate(f'Payback: Year {payback_year}', 
                        xy=(payback_year, investment),
                        xytext=(payback_year + 0.5, investment * 0.8),
                        arrowprops=dict(arrowstyle='->', color=theme_colors['text_color']),
                        fontsize=10, fontweight='bold', color=theme_colors['text_color'])
    
    # Enhanced styling with theme colors
    ax_save.set_xlabel('Years', fontsize=12, fontweight='bold', color=theme_colors['text_color'])
    ax_save.set_ylabel('Amount (₹)', fontsize=12, fontweight='bold', color=theme_colors['text_color'])
    ax_save.set_title('10-Year Financial Projection', fontsize=14, fontweight='bold', 
                     pad=20, color=theme_colors['text_color'])
    
    # Style legend and grid with theme colors
    ax_save.tick_params(colors=theme_colors['text_color'])
    ax_save.spines['bottom'].set_color(theme_colors['text_color'])
    ax_save.spines['left'].set_color(theme_colors['text_color'])
    
    legend = ax_save.legend(fontsize=10, framealpha=0.9)
    legend.get_frame().set_facecolor(theme_colors['bg_color'])
    legend.get_frame().set_edgecolor(theme_colors['text_color'])
    for text in legend.get_texts():
        text.set_color(theme_colors['text_color'])
    
    ax_save.grid(True, alpha=0.3, linestyle='--', color=theme_colors['grid_color'])
    
    # Remove top and right spines for cleaner look
    for spine in ['top', 'right']:
        ax_save.spines[spine].set_visible(False)
    
    ax_save.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
    plt.tight_layout()
    
    # Persist computed artifacts for PDF
    st.session_state.assessment_params = params
    st.session_state.recommendation_result = recommendation
    st.session_state.design_financial = design_financial
    st.session_state.soil_type = soil_type
    st.session_state.data_source_message = data_source_msg
    st.session_state.monthly_rainfall = monthly_rainfall
    st.session_state.fig_rain = fig_rain
    st.session_state.fig_cost = fig_cost
    st.session_state.fig_save = fig_save
    
    # Header recommendation and KPIs
    # Translate recommendation type
    rec_type = recommendation['recommendation_type']
    if rec_type == 'Storage Only':
        rec_type_translated = T('results_storage_only')
    elif rec_type == 'Recharge Only':
        rec_type_translated = T('results_recharge_only')
    elif rec_type == 'Hybrid System':
        rec_type_translated = T('results_hybrid_system')
    else:
        rec_type_translated = rec_type
    
    # Translate efficiency rating
    efficiency = recommendation['efficiency_rating']
    if efficiency == 'Excellent':
        efficiency_translated = T('results_efficiency_excellent')
    elif efficiency == 'Good':
        efficiency_translated = T('results_efficiency_good')
    elif efficiency == 'Moderate':
        efficiency_translated = T('results_efficiency_moderate')
    else:
        efficiency_translated = efficiency
    
    st.markdown(f"""
    <div class="recommendation-box">
        <h2>{T('results_recommended_strategy')} <strong>{rec_type_translated}</strong></h2>
        <p style="font-size: 18px; margin-top: 10px;">{T('results_system_efficiency')} <strong>{efficiency_translated}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="reason-box">
        <strong>{T('results_strategic_rationale')}</strong> {recommendation['reason']}
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader(T('results_key_metrics'))
    
    # Debug: Ensure recommendation data exists
    if not recommendation:
        st.error(T('results_no_recommendation_data'))
        return
    
    # Create metrics with enhanced styling and error handling
    k1, k2, k3, k4 = st.columns(4)
    
    # Extract values with defaults
    annual_potential = recommendation.get('annual_potential', 0)
    volume_to_store = recommendation.get('volume_to_store', 0)
    volume_to_recharge = recommendation.get('volume_to_recharge', 0)
    
    with k1:
        st.metric(
            label=T('results_annual_harvest'), 
            value=f"{annual_potential:,.0f} L",
            help=T('results_help_harvest')
        )
    
    with k2:
        st.metric(
            label=T('results_storage_allocation'), 
            value=f"{volume_to_store:,.0f} L",
            help=T('results_help_storage')
        )
    
    with k3:
        st.metric(
            label=T('results_recharge_allocation'), 
            value=f"{volume_to_recharge:,.0f} L",
            help=T('results_help_recharge')
        )
    
    with k4:
        try:
            annual_demand = params['household_size'] * 135 * 365
            coverage_pct = (annual_potential / annual_demand) * 100 if annual_demand > 0 else 0
            coverage_display = f"{min(coverage_pct, 100):.1f}%"
            st.metric(
                label=T('results_household_coverage'), 
                value=coverage_display,
                help=T('results_help_coverage')
            )
        except (KeyError, ZeroDivisionError, TypeError) as e:
            st.metric(
                label=T('results_household_coverage'), 
                value="N/A",
                help=T('results_help_coverage')
            )
    
    st.markdown("---")
    
    # Output Tabs
    t1, t2, t3, t4, t5 = st.tabs([T('results_recommended_design'), T('results_financials'), T('results_site_data'), T('results_rainfall'), T('results_summary')])
    
    with t1:
        show_system_design_tab(design_financial)
    
    with t2:
        show_financial_analysis_tab(design_financial, recommendation)
    
    with t3:
        show_site_data_tab(params, soil_type)
        st.info(st.session_state.get('data_source_message', 'Using simulated data'))
    
    with t4:
        st.header(T('results_hydro_analysis'))
        st.pyplot(fig_rain)
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader(T('results_rainfall_statistics'))
            rainfall_df = pd.DataFrame({
                'Metric': [T('results_total_annual'), T('results_monthly_average'), T('results_max_month'), T('results_min_month')],
                'Value': [
                    f"{sum(monthly_rainfall.values()):.0f} mm",
                    f"{sum(monthly_rainfall.values())/12:.0f} mm",
                    f"{max(monthly_rainfall.values()):.0f} mm ({max(monthly_rainfall, key=monthly_rainfall.get)})",
                    f"{min(monthly_rainfall.values()):.0f} mm ({min(monthly_rainfall, key=monthly_rainfall.get)})"
                ]
            })
            st.dataframe(rainfall_df, hide_index=True, use_container_width=True)
        with col_b:
            st.subheader(T('results_harvesting_metrics'))
            harvest_df = pd.DataFrame({
                'Parameter': [T('results_runoff_coeff_param'), T('results_collection_efficiency')],
                'Value': [f"{params['runoff_coefficient']:.2f}", f"{params['runoff_coefficient']*100:.0f}%"]
            })
            st.dataframe(harvest_df, hide_index=True, use_container_width=True)
    
    with t5:
        show_summary_report_tab(params, recommendation, design_financial, soil_type)

def show_site_selection():
    st.header(T('calc_site_parameters'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(T('calc_site_parameters'))
        latitude = st.number_input(T('calc_latitude'), value=st.session_state.latitude, format="%.6f", help=T('calc_latitude'))
        longitude = st.number_input(T('calc_longitude'), value=st.session_state.longitude, format="%.6f", help=T('calc_longitude'))
        
        st.subheader(T('calc_data_enhancements'))
        # Ensure area value is valid to avoid Streamlit error
        area_value = max(1.0, st.session_state.get('area', 150.0))
        area = st.number_input(T('calc_catchment_area'), min_value=1.0, value=area_value, step=10.0, help=T('calc_catchment_area'))
    
    with col2:
        st.subheader(T('calc_data_enhancements'))
        surface_type = st.selectbox(T('calc_surface_type'), list(RUNOFF_COEFFICIENTS.keys()))
        runoff_coefficient = RUNOFF_COEFFICIENTS[surface_type]
        st.info(f"**Runoff Coefficient:** {runoff_coefficient}")
        
        st.subheader(T('calc_household_city'))
        household_size = st.slider(T('calc_household_size'), 1, 15, 4)
        city_type = st.selectbox(T('calc_city_classification'), [T('calc_city_tier2'), T('calc_city_tier1')])
        water_cost_per_m3 = st.number_input(T('calc_water_cost'), min_value=10.0, value=25.0, step=1.0)
        
    # Optional: Use device GPS (if streamlit_geolocation available)
    with st.expander("📍 Use Device GPS (Optional)"):
        try:
            from streamlit_geolocation import streamlit_geolocation  # type: ignore
            loc = streamlit_geolocation()
            if loc and loc.get('latitude') is not None and loc.get('longitude') is not None:
                st.success(f"Detected Location: {loc['latitude']:.6f}, {loc['longitude']:.6f}")
                if st.button("Use Detected GPS Location", use_container_width=True):
                    latitude = float(loc['latitude'])
                    longitude = float(loc['longitude'])
        except Exception:
            st.info("GPS helper not available. You can install 'streamlit-geolocation' to enable this.")
    
    # Advanced data upload
    with st.expander("🔬 Advanced: Upload Local Groundwater Data"):
        uploaded_file = st.file_uploader("Upload GeoJSON file with groundwater data", type=['geojson'])
        if uploaded_file:
            try:
                gdf = gpd.read_file(uploaded_file)
                required_cols = ['post_monsoon_depth_m', 'principal_aquifer_type']
                if all(col in gdf.columns for col in required_cols):
                    st.session_state.groundwater_gdf = gdf
                    st.session_state.data_source = 'uploaded'
                    st.success(f"✅ Successfully loaded {len(gdf)} groundwater data points")
                else:
                    st.error(f"❌ Missing required columns: {required_cols}")
            except Exception as e:
                st.error(f"❌ Error loading file: {e}")
    
    if st.button("🎯 Confirm Site Configuration", type="primary"):
        st.session_state.latitude = latitude
        st.session_state.longitude = longitude
        st.session_state.area = area
        st.session_state.surface_type = surface_type
        st.session_state.runoff_coefficient = runoff_coefficient
        st.session_state.household_size = household_size
        st.session_state.city_type = city_type
        st.session_state.water_cost_per_m3 = water_cost_per_m3
        st.success("✅ Site configuration saved successfully!")

def show_assessment_engine():
    st.header("⚡ Intelligent Assessment Engine")
    
    # Check if configuration is complete
    required_keys = ['latitude', 'longitude', 'area', 'surface_type', 'runoff_coefficient', 'household_size', 'city_type', 'water_cost_per_m3']
    if not all(key in st.session_state for key in required_keys):
        st.warning("⚠️ Please complete the site configuration in the 'Site Selection' tab first.")
        return
    
    # Display current configuration
    st.subheader("📋 Current Configuration")
    config_col1, config_col2 = st.columns(2)
    
    with config_col1:
        st.info(f"**Location:** {st.session_state.latitude:.4f}°N, {st.session_state.longitude:.4f}°E")
        st.info(f"**Catchment Area:** {st.session_state.area:,.0f} m²")
        st.info(f"**Surface Type:** {st.session_state.surface_type}")
        st.info(f"**Runoff Coefficient:** {st.session_state.runoff_coefficient}")
    
    with config_col2:
        st.info(f"**Household Size:** {st.session_state.household_size} persons")
        st.info(f"**City Type:** {st.session_state.city_type}")
        st.info(f"**Water Cost:** ₹{st.session_state.water_cost_per_m3}/m³")
        data_source_text = "Local Data" if st.session_state.data_source == 'uploaded' else "Simulated Data"
        st.info(f"**Groundwater Data:** {data_source_text}")
    
    st.markdown("---")
    
    # Run Assessment Button
    if st.button("🔍 Run Intelligent Assessment", type="primary", help="Analyze your site and generate recommendations"):
        run_complete_assessment()

def run_complete_assessment():
    """Execute the complete assessment workflow."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Compile parameters
    status_text.text("Compiling site parameters...")
    progress_bar.progress(20)
    
    params = {
        'latitude': st.session_state.latitude,
        'longitude': st.session_state.longitude,
        'area': st.session_state.area,
        'surface_type': st.session_state.surface_type,
        'runoff_coefficient': st.session_state.runoff_coefficient,
        'household_size': st.session_state.household_size,
        'city_type': st.session_state.city_type,
        'water_cost_per_m3': st.session_state.water_cost_per_m3
    }
    
    # Step 2: Fetch external data
    status_text.text("Fetching rainfall and soil data...")
    progress_bar.progress(40)
    
    # Ensure both APIs use the same coordinates
    current_lat, current_lon = params['latitude'], params['longitude']
    
    params['annual_rainfall'] = get_annual_rainfall(current_lat, current_lon)
    if params['annual_rainfall'] is None:
        st.error("Could not fetch rainfall data. Please check your internet connection and try again.")
        return
    
    soil_type = get_soil_type(current_lat, current_lon)
    
    # Monthly rainfall for charts
    monthly_rainfall = get_monthly_rainfall(current_lat, current_lon)
    if monthly_rainfall is None:
        monthly_rainfall = {m: 0.0 for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}
    
    # Step 3: Get groundwater data
    status_text.text("Analyzing groundwater conditions...")
    progress_bar.progress(60)
    
    if st.session_state.data_source == 'uploaded' and st.session_state.groundwater_gdf is not None:
        groundwater_data = query_groundwater_from_gdf(
            current_lat, current_lon, st.session_state.groundwater_gdf
        )
        data_source_msg = "Using uploaded groundwater data"
    else:
        groundwater_data = get_groundwater_data(current_lat, current_lon)
        data_source_msg = "Using simulated groundwater data"
    
    params.update(groundwater_data)
    
    # Step 4: Run recommendation engine
    status_text.text("Generating intelligent recommendations...")
    progress_bar.progress(80)
    
    recommendation_result = generate_recommendation(params)
    
    # Step 5: Calculate design and costs
    status_text.text("Calculating system design and costs...")
    progress_bar.progress(90)
    
    design_financial = calculate_design_and_cost(recommendation_result, params)
    
    # Build charts to embed in PDF
    fig_rain, ax_rain = plt.subplots(figsize=(10, 6))
    months = list(monthly_rainfall.keys())
    values = list(monthly_rainfall.values())
    colors = ['#1f77b4' if v >= (np.mean(values) if values else 0) else '#ff7f0e' for v in values]
    bars = ax_rain.bar(months, values, color=colors, edgecolor='black', linewidth=1)
    ax_rain.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax_rain.set_ylabel('Rainfall (mm)', fontsize=12, fontweight='bold')
    ax_rain.set_title('Monthly Rainfall Distribution (2023)', fontsize=14, fontweight='bold')
    ax_rain.grid(axis='y', alpha=0.3, linestyle='--')
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax_rain.text(bar.get_x() + bar.get_width()/2., height, f'{value:.0f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()

    # Cost breakdown chart - Enhanced for PDF
    costs = design_financial['cost_breakdown']
    filtered_costs = {k: v for k, v in costs.items() if v > 0}
    fig_cost, ax_cost = plt.subplots(figsize=(10, 8))
    if filtered_costs:
        # Use the same professional color palette as the web interface
        custom_colors = [
            '#2E8B57',  # Sea Green
            '#FFD700',  # Gold
            '#4682B4',  # Steel Blue
            '#FF6347',  # Tomato
            '#9370DB',  # Medium Purple
            '#20B2AA',  # Light Sea Green
            '#FFA500',  # Orange
            '#DC143C',  # Crimson
        ]
        
        labels = [k.replace('_', ' ').title() for k in filtered_costs.keys()]
        values = list(filtered_costs.values())
        
        # Use custom colors, cycling through if needed
        colors = [custom_colors[i % len(custom_colors)] for i in range(len(values))]
        
        # Create enhanced pie chart for PDF
        wedges, texts, autotexts = ax_cost.pie(
            values, 
            labels=labels, 
            autopct=lambda pct: f'{pct:.1f}%\n(₹{pct/100 * sum(values)/1000:.0f}K)' if pct > 5 else f'{pct:.1f}%',
            colors=colors, 
            startangle=90,
            explode=[0.05 if v == max(values) else 0 for v in values],  # Explode the largest slice
            shadow=True,
            wedgeprops=dict(width=0.8, edgecolor='white', linewidth=2)
        )
        
        ax_cost.set_title('System Cost Distribution', fontsize=16, fontweight='bold', pad=20)
        
        # Improve text styling
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        # Add a legend with cost values for PDF
        legend_labels = [f'{label}: ₹{value/1000:.0f}K ({value/sum(values)*100:.1f}%)' 
                       for label, value in zip(labels, values)]
        ax_cost.legend(wedges, legend_labels, title="Components", loc="center left", 
                     bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
        
        ax_cost.axis('equal')
        plt.tight_layout()

    # Savings projection chart - Enhanced for PDF
    fig_save, ax_save = plt.subplots(figsize=(10, 6))
    years = list(range(1, 11))
    annual_savings_arr = [design_financial['annual_savings']] * 10
    annual_maintenance_arr = [design_financial['maintenance_cost_annual']] * 10
    net_annual = [s - m for s, m in zip(annual_savings_arr, annual_maintenance_arr)]
    cumulative_savings = np.cumsum(net_annual)
    
    # Enhanced styling for PDF
    bars = ax_save.bar(years, cumulative_savings, alpha=0.8, color='#2E8B57', 
                      label='Cumulative Net Savings', edgecolor='white', linewidth=1)
    
    # Add investment line with better styling
    ax_save.axhline(y=design_financial['total_cost'], color='#DC143C', linestyle='--', 
                   linewidth=2.5, label='Initial Investment', alpha=0.9)
    
    # Find and mark payback period if within 10 years
    investment = design_financial['total_cost']
    payback_year = next((i+1 for i, val in enumerate(cumulative_savings) if val >= investment), None)
    if payback_year and payback_year <= 10:
        ax_save.plot(payback_year, investment, 'ro', markersize=8, 
                    markeredgecolor='white', markeredgewidth=2)
        ax_save.annotate(f'Payback: Year {payback_year}', 
                        xy=(payback_year, investment),
                        xytext=(payback_year + 0.5, investment * 0.8),
                        arrowprops=dict(arrowstyle='->', color='black'),
                        fontsize=10, fontweight='bold')
    
    # Enhanced styling
    ax_save.set_xlabel('Years', fontsize=12, fontweight='bold')
    ax_save.set_ylabel('Amount (₹)', fontsize=12, fontweight='bold')
    ax_save.set_title('10-Year Financial Projection', fontsize=14, fontweight='bold', pad=20)
    
    # Style legend and grid
    ax_save.legend(fontsize=10, framealpha=0.9)
    ax_save.grid(True, alpha=0.3, linestyle='--')
    
    # Remove top and right spines for cleaner look
    for spine in ['top', 'right']:
        ax_save.spines[spine].set_visible(False)
    
    ax_save.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
    plt.tight_layout()
    
    # Store results in session state
    st.session_state.assessment_params = params
    st.session_state.recommendation_result = recommendation_result
    st.session_state.design_financial = design_financial
    st.session_state.soil_type = soil_type
    st.session_state.data_source_message = data_source_msg
    st.session_state.monthly_rainfall = monthly_rainfall
    st.session_state.fig_rain = fig_rain
    st.session_state.fig_cost = fig_cost
    st.session_state.fig_save = fig_save
    
    status_text.text("Assessment completed!")
    progress_bar.progress(100)
    
    # Show results immediately
    st.success("Assessment completed successfully! View detailed results in the 'Results & Report' tab.")
    st.balloons()

def show_results_and_report():
    st.header(T('results_comprehensive_report'))
    
    # Check if assessment has been run
    if 'recommendation_result' not in st.session_state:
        st.warning(T('results_run_assessment_first'))
        return
    
    # Get results from session state
    params = st.session_state.assessment_params
    recommendation = st.session_state.recommendation_result
    design_financial = st.session_state.design_financial
    soil_type = st.session_state.soil_type
    
    # Display main recommendation prominently
    st.markdown(f"""
    <div class="recommendation-box">
        <h2>{T('results_recommended_strategy')} <strong>{recommendation['recommendation_type']}</strong></h2>
        <p style="font-size: 18px; margin-top: 10px;">{T('results_system_efficiency')} <strong>{recommendation['efficiency_rating']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="reason-box">
        <strong>{T('results_strategic_rationale')}</strong> {recommendation['reason']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key performance metrics
    st.subheader(T('results_key_metrics'))
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            T('results_annual_harvest'),
            f"{recommendation['annual_potential']:,.0f} L",
            help=T('results_help_harvest')
        )
    
    with col2:
        st.metric(
            T('results_storage_allocation'),
            f"{recommendation['volume_to_store']:,.0f} L",
            help=T('results_help_storage')
        )
    
    with col3:
        st.metric(
            T('results_recharge_allocation'), 
            f"{recommendation['volume_to_recharge']:,.0f} L",
            help=T('results_help_recharge')
        )
    
    with col4:
        coverage_pct = (recommendation['annual_potential'] / (params['household_size'] * 135 * 365)) * 100
        st.metric(
            T('results_household_coverage'),
            f"{min(coverage_pct, 100):.1f}%",
            help=T('results_help_coverage')
        )
    
    # Detailed results in tabs
    result_tab1, result_tab2, result_tab3, result_tab4, result_tab5 = st.tabs([T('results_recommended_design').replace('🏗️ ', ''), T('results_financials').replace('💰 ', ''), T('results_site_data').replace('🌍 ', ''), T('results_rainfall').replace('🌧️ ', ''), T('results_summary').replace('📋 ', '')])
    
    with result_tab1:
        show_system_design_tab(design_financial)
    
    with result_tab2:
        show_financial_analysis_tab(design_financial, recommendation)
    
    with result_tab3:
        show_site_data_tab(params, soil_type)
    
    with result_tab4:
        # Rainfall analytics
        st.header(T('results_hydro_analysis'))
        monthly = st.session_state.get('monthly_rainfall', None)
        if monthly:
            fig = st.session_state.get('fig_rain')
            if fig:
                st.pyplot(fig)
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.subheader(T('results_rainfall_statistics'))
                rainfall_df = pd.DataFrame({
                    'Metric': [T('results_total_annual'), T('results_monthly_average'), T('results_max_month'), T('results_min_month')],
                    'Value': [
                        f"{sum(monthly.values()):.0f} mm",
                        f"{sum(monthly.values())/12:.0f} mm",
                        f"{max(monthly.values()):.0f} mm ({max(monthly, key=monthly.get)})",
                        f"{min(monthly.values()):.0f} mm ({min(monthly, key=monthly.get)})"                    ]
                })
                st.dataframe(rainfall_df, hide_index=True, use_container_width=True)
            with col_b:
                st.subheader(T('results_harvesting_metrics'))
                harvest_df = pd.DataFrame({
                    'Parameter': [T('results_runoff_coeff_param'), T('results_collection_efficiency')],
                    'Value': [f"{params['runoff_coefficient']:.2f}", f"{params['runoff_coefficient']*100:.0f}%"]
                })
                st.dataframe(harvest_df, hide_index=True, use_container_width=True)
        else:
            st.info(T('results_monthly_data_unavailable'))
    
    with result_tab5:
        show_summary_report_tab(params, recommendation, design_financial, soil_type)

def show_system_design_tab(design_financial):
    st.header(T('results_recommended_design').replace('🏗️ ', ''))
    
    if not design_financial['design']:
        st.info(T('results_no_system_components'))
        return
    
    # Storage system
    if 'storage_tank' in design_financial['design']:
        tank = design_financial['design']['storage_tank']
        st.markdown(f"""
        <div class="design-card">
            <h4>{T('results_storage_specs')}</h4>
            <ul>
                <li><strong>{T('results_tank_type')}</strong> {tank['type']}</li>
                <li><strong>{T('results_capacity')}</strong> {tank['volume_liters']:,.0f} liters ({tank['volume_m3']:.1f} m³)</li>
                <li><strong>{T('results_dimensions')}</strong> {tank['dimensions']}</li>
                <li><strong>{T('results_installation')}</strong> {T('results_installation_underground')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Recharge system
    if 'recharge_system' in design_financial['design']:
        recharge = design_financial['design']['recharge_system']
        st.markdown(f"""
        <div class="design-card">
            <h4>{T('results_recharge_specs')}</h4>
            <ul>
                <li><strong>{T('results_configuration')}</strong> {recharge['configuration']}</li>
                <li><strong>{T('results_total_capacity')}</strong> {recharge['volume_m3']:.1f} m³</li>
                <li><strong>{T('results_dimensions')}</strong> {recharge['dimensions']}</li>
                <li><strong>{T('results_footprint')}</strong> {recharge['total_area']}</li>
                <li><strong>{T('results_depth')}</strong> {T('results_filter_media')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional components
    st.subheader(T('results_supporting_infra'))
    
    # Create a styled list for better visibility
    components_html = f"""
    <div style="background: var(--bg-secondary); border-radius: 12px; padding: 20px; margin: 15px 0; border: 1px solid var(--border-color);">
        <ul style="margin: 0; padding-left: 20px; color: var(--text-primary);">
            <li style="margin-bottom: 8px; color: var(--text-primary); font-weight: 500;">{T('results_first_flush_diverter')}</li>
            <li style="margin-bottom: 8px; color: var(--text-primary); font-weight: 500;">{T('results_multi_stage_filtration')}</li>
            <li style="margin-bottom: 8px; color: var(--text-primary); font-weight: 500;">{T('results_gutter_system')}</li>
            <li style="margin-bottom: 8px; color: var(--text-primary); font-weight: 500;">{T('results_distribution_piping')}</li>
            <li style="margin-bottom: 8px; color: var(--text-primary); font-weight: 500;">{T('results_overflow_management')}</li>
        </ul>
    </div>
    """
    st.markdown(components_html, unsafe_allow_html=True)

def show_financial_analysis_tab(design_financial, recommendation):
    st.header(T('results_financial_header'))
    
    # Cost breakdown
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(T('results_cost_breakdown'))
        
        # Create cost breakdown chart
        costs = design_financial['cost_breakdown']
        # Filter out zero costs for better visualization
        filtered_costs = {k: v for k, v in costs.items() if v > 0}
        
        if filtered_costs:
            # Enhanced pie chart with professional styling and dark mode support
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Detect if we're in dark mode (simple heuristic based on Streamlit's theme)
            # Set dark mode compatible styling
            is_dark_mode = True  # We'll assume dark mode for better compatibility
            
            if is_dark_mode:
                fig.patch.set_facecolor('#0e1117')  # Streamlit dark background
                ax.set_facecolor('#0e1117')
                text_color = '#ffffff'
                title_color = '#ffffff'
            else:
                fig.patch.set_facecolor('white')
                ax.set_facecolor('white')
                text_color = '#2c3e50'
                title_color = '#2c3e50'
            
            # Custom color palette - professional and visually appealing
            custom_colors = [
                '#2E8B57',  # Sea Green
                '#FFD700',  # Gold
                '#4682B4',  # Steel Blue
                '#FF6347',  # Tomato
                '#9370DB',  # Medium Purple
                '#20B2AA',  # Light Sea Green
                '#FFA500',  # Orange
                '#DC143C',  # Crimson
            ]
            
            labels = [k.replace('_', ' ').title() for k in filtered_costs.keys()]
            values = list(filtered_costs.values())
            
            # Use custom colors, cycling through if needed
            colors = [custom_colors[i % len(custom_colors)] for i in range(len(values))]
            
            # Create pie chart with enhanced styling
            wedges, texts, autotexts = ax.pie(
                values, 
                labels=labels, 
                autopct=lambda pct: f'{pct:.1f}%\n(₹{pct/100 * sum(values)/1000:.0f}K)' if pct > 5 else f'{pct:.1f}%',
                colors=colors, 
                startangle=90,
                explode=[0.05 if v == max(values) else 0 for v in values],  # Explode the largest slice
                shadow=True,
                wedgeprops=dict(width=0.8, edgecolor='white', linewidth=2)
            )
            
            # Enhanced title with better styling
            ax.set_title(T('results_cost_distribution'), fontsize=16, fontweight='bold', 
                        pad=20, color=title_color)
            
            # Improve text styling for dark mode compatibility
            for text in texts:
                text.set_fontsize(11)
                text.set_fontweight('bold')
                text.set_color(text_color)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Add a legend with cost values
            legend_labels = [f'{label}: ₹{value/1000:.0f}K ({value/sum(values)*100:.1f}%)' 
                           for label, value in zip(labels, values)]
            legend = ax.legend(wedges, legend_labels, title="Components", loc="center left", 
                             bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
            
            # Style legend for dark mode
            legend.get_title().set_color(text_color)
            for text in legend.get_texts():
                text.set_color(text_color)
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')
            
            # Adjust layout to prevent legend cutoff
            plt.tight_layout()
            
            st.pyplot(fig)
        
        # Cost summary table
        st.markdown(f"""
        <div class="cost-card">
            <h4>{T('results_investment_summary')}</h4>
            <table style="width:100%">
                <tr><td><strong>{T('results_total_cost')}</strong></td><td><strong>₹ {design_financial['total_cost']:,.0f}</strong></td></tr>
                <tr><td>{T('results_annual_maintenance')}</td><td>₹ {design_financial['maintenance_cost_annual']:,.0f}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader(T('results_financial_benefits'))
        
        # Create bar chart for cost breakdown
        if filtered_costs:
            # Create bar chart
            fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
            
            # Set dark mode compatible styling
            is_dark_mode = True  # Assume dark mode for better compatibility
            
            if is_dark_mode:
                fig_bar.patch.set_facecolor('#0e1117')  # Streamlit dark background
                ax_bar.set_facecolor('#0e1117')
                text_color = '#ffffff'
                grid_color = '#404040'
            else:
                fig_bar.patch.set_facecolor('white')
                ax_bar.set_facecolor('white')
                text_color = '#2c3e50'
                grid_color = '#cccccc'
            
            # Prepare data for bar chart
            components = [k.replace('_', ' ').title() for k in filtered_costs.keys()]
            cost_values = list(filtered_costs.values())
            
            # Create horizontal bar chart for better readability
            bars = ax_bar.barh(components, cost_values, color=colors, alpha=0.8, 
                              edgecolor='white', linewidth=1)
            
            # Style the chart
            ax_bar.set_xlabel('Cost (₹)', fontsize=12, fontweight='bold', color=text_color)
            ax_bar.set_ylabel('Components', fontsize=12, fontweight='bold', color=text_color)
            ax_bar.set_title('Cost Breakdown by Component', fontsize=14, fontweight='bold', 
                           color=text_color, pad=20)
            
            # Add value labels on bars
            for bar, value in zip(bars, cost_values):
                width = bar.get_width()
                ax_bar.text(width + max(cost_values) * 0.02, bar.get_y() + bar.get_height()/2,
                           f'₹{value/1000:.0f}K', ha='left', va='center', 
                           fontweight='bold', fontsize=10, color=text_color)
            
            # Style grid and ticks
            ax_bar.grid(True, alpha=0.3, color=grid_color, linestyle='--', axis='x')
            ax_bar.tick_params(colors=text_color)
            
            # Remove top and right spines
            for spine in ['top', 'right']:
                ax_bar.spines[spine].set_visible(False)
            
            # Style remaining spines
            for spine in ['bottom', 'left']:
                ax_bar.spines[spine].set_color(text_color)
            
            # Format x-axis labels
            ax_bar.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
            
            # Adjust layout
            plt.tight_layout()
            
            st.pyplot(fig_bar)
        
        if design_financial['annual_savings'] > 0:
            # Create savings projection chart
            years = list(range(1, 11))
            annual_savings = [design_financial['annual_savings']] * 10
            annual_maintenance = [design_financial['maintenance_cost_annual']] * 10
            net_annual_savings = [s - m for s, m in zip(annual_savings, annual_maintenance)]
            cumulative_savings = np.cumsum(net_annual_savings)
            
            # Create financial projection chart with dark mode support
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Set dark mode compatible styling
            is_dark_mode = True  # Assume dark mode for better compatibility
            
            if is_dark_mode:
                fig.patch.set_facecolor('#0e1117')  # Streamlit dark background
                ax.set_facecolor('#0e1117')
                text_color = '#ffffff'
                grid_color = '#404040'
            else:
                fig.patch.set_facecolor('white')
                ax.set_facecolor('white')
                text_color = '#2c3e50'
                grid_color = '#cccccc'
            
            # Plot with enhanced styling
            bars = ax.bar(years, cumulative_savings, alpha=0.8, color='#2E8B57', 
                         label='Cumulative Net Savings', edgecolor='white', linewidth=1)
            
            # Add investment line
            ax.axhline(y=design_financial['total_cost'], color='#DC143C', linestyle='--', 
                      linewidth=2.5, label='Initial Investment', alpha=0.9)
            
            # Style axes and labels
            ax.set_xlabel('Years', fontsize=12, fontweight='bold', color=text_color)
            ax.set_ylabel('Amount (₹)', fontsize=12, fontweight='bold', color=text_color)
            ax.set_title(T('results_financial_projection'), fontsize=14, fontweight='bold', 
                        color=text_color, pad=20)
            
            # Style legend
            legend = ax.legend(fontsize=10, framealpha=0.9)
            legend.get_frame().set_facecolor('#2d2d2d' if is_dark_mode else 'white')
            for text in legend.get_texts():
                text.set_color(text_color)
            
            # Style grid and ticks
            ax.grid(True, alpha=0.3, color=grid_color, linestyle='--')
            ax.tick_params(colors=text_color)
            
            # Remove top and right spines
            for spine in ['top', 'right']:
                ax.spines[spine].set_visible(False)
            
            # Style remaining spines
            for spine in ['bottom', 'left']:
                ax.spines[spine].set_color(text_color)
            
            # Format y-axis labels
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
            
            st.pyplot(fig)
            
            # Financial metrics
            payback_years = design_financial['payback_period_years']
            payback_text = f"{payback_years:.1f} years" if payback_years != float('inf') else "N/A"
            
            st.success(f"{T('results_annual_savings')} ₹ {design_financial['annual_savings']:,.0f}")
            st.success(f"{T('results_payback_period')} {payback_text}")
            
            # ROI calculation
            if payback_years != float('inf'):
                roi_10_year = ((cumulative_savings[-1] - design_financial['total_cost']) / design_financial['total_cost']) * 100
                st.success(f"{T('results_roi_10year')} {roi_10_year:.1f}%")
        else:
            st.info(T('results_environmental_benefits_focus'))
    
    # Environmental benefits
    st.subheader(T('results_environmental_impact'))
    col1, col2, col3 = st.columns(3)
    
    with col1:
        annual_harvest_m3 = recommendation['annual_potential'] / 1000
        st.metric(T('results_water_independence'), f"{annual_harvest_m3:,.0f} m³/year", 
                 help=T('results_annual_freshwater_demand'))
    
    with col2:
        if design_financial['groundwater_recharge_m3_annual'] > 0:
            st.metric(T('results_groundwater_recharge'), f"{design_financial['groundwater_recharge_m3_annual']:,.0f} m³/year",
                     help=T('results_annual_groundwater_replenishment'))
        else:
            st.metric(T('results_runoff_reduction'), f"{annual_harvest_m3:,.0f} m³/year",
                     help=T('results_reduced_stormwater_runoff'))
    
    with col3:
        co2_reduction = annual_harvest_m3 * 0.5  # Approximate CO2 savings
        st.metric(T('results_co2_reduction'), f"{co2_reduction:.0f} kg/year",
                 help=T('results_carbon_footprint_reduction'))

def show_site_data_tab(params, soil_type):
    st.header(T('results_site_characteristics'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(T('results_location_data'))
        location_data = {
            T('results_coordinates'): f"{params['latitude']:.6f}°N, {params['longitude']:.6f}°E",
            T('results_catchment_area_label'): f"{params['area']:,.0f} m²",
            T('results_surface_type_label'): params['surface_type'],
            T('results_runoff_coefficient_label'): f"{params['runoff_coefficient']:.2f}",
            T('results_city_classification_label'): params['city_type'],
            T('results_household_size_label'): f"{params['household_size']} persons"
        }
        
        for key, value in location_data.items():
            st.write(f"**{key}:** {value}")
    
    with col2:
        st.subheader(T('results_hydro_data'))
        hydro_data = {
            T('results_annual_rainfall_label'): f"{params['annual_rainfall']:.0f} mm",
            T('results_soil_classification'): soil_type,
            T('results_groundwater_post'): f"{params['post_monsoon_depth_m']:.1f} m bgl",
            T('results_groundwater_pre'): f"{params['pre_monsoon_depth_m']:.1f} m bgl",
            T('results_aquifer_type'): params['principal_aquifer_type'],
            T('results_aquifer_yield'): params.get('aquifer_yield', 'Moderate')
        }
        
        for key, value in hydro_data.items():
            st.write(f"**{key}:** {value}")
    
    # Data source information
    st.info(st.session_state.get('data_source_message', 'Using simulated data'))
    
    # Site suitability assessment
    st.subheader(T('results_site_suitability'))
    
    suitability_factors = []
    
    # Rainfall assessment
    if params['annual_rainfall'] > 800:
        suitability_factors.append(T('results_rainfall_excellent'))
    elif params['annual_rainfall'] > 500:
        suitability_factors.append(T('results_rainfall_good'))
    else:
        suitability_factors.append(T('results_rainfall_low'))
    
    # Groundwater assessment
    if params['post_monsoon_depth_m'] > 15:
        suitability_factors.append(T('results_groundwater_deep'))
    elif params['post_monsoon_depth_m'] > 8:
        suitability_factors.append(T('results_groundwater_moderate'))
    else:
        suitability_factors.append(T('results_groundwater_shallow'))
    
    # Area assessment
    if params['area'] > 200:
        suitability_factors.append(T('results_area_large'))
    elif params['area'] > 100:
        suitability_factors.append(T('results_area_good'))
    else:
        suitability_factors.append(T('results_area_compact'))
    
    for factor in suitability_factors:
        st.markdown(f"• {factor}")

def show_summary_report_tab(params, recommendation, design_financial, soil_type):
    st.header(T('results_executive_summary'))
    
    # Generate PDF report with enhanced data validation
    site_data = {
        'soil_type': soil_type if soil_type and soil_type.strip() else 'Sandy',
        'post_monsoon_depth_m': params.get('post_monsoon_depth_m', 12.0),
        'principal_aquifer_type': params.get('principal_aquifer_type', 'Alluvial Plains') if params.get('principal_aquifer_type') and params.get('principal_aquifer_type').strip() else 'Alluvial Plains',
        'aquifer_yield': params.get('aquifer_yield', 'Moderate') if params.get('aquifer_yield') and params.get('aquifer_yield').strip() else 'Moderate'
    }
    
    try:
        charts = {
            'rainfall_chart': st.session_state.get('fig_rain'),
            'cost_chart': st.session_state.get('fig_cost'),
            'savings_chart': st.session_state.get('fig_save')
        }
        
        # Generate PDF with better error handling
        with st.spinner('Generating comprehensive PDF report...'):
            # Add missing site data fields
            site_data['pre_monsoon_depth_m'] = params.get('pre_monsoon_depth_m', params['post_monsoon_depth_m'] + 2.0)
            pdf_buffer = generate_professional_pdf(params, recommendation, design_financial, site_data, charts)
            pdf_bytes = pdf_buffer.getvalue()
            
        # Validate PDF bytes
        if not pdf_bytes or len(pdf_bytes) == 0:
            raise ValueError("Generated PDF is empty")
            
        if not isinstance(pdf_bytes, bytes):
            raise TypeError(f"PDF generation returned {type(pdf_bytes)} instead of bytes")
        
        st.success("Your comprehensive assessment report is ready!")
        
        # Download button
        st.download_button(
            label=T('results_download_pdf'),
            data=pdf_bytes,
            file_name=f"Hydro_Assess_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
        # Report preview
        st.subheader(T('results_report_preview'))
        
        preview_col1, preview_col2 = st.columns(2)
        
        with preview_col1:
            st.markdown(f"**{T('results_report_contents')}**")
            contents = [
                T('results_executive_summary_recommendation'),
                T('results_system_design_specifications'), 
                T('results_financial_analysis_cost_breakdown'),
                T('results_site_characteristics_geohydrology'),
                T('results_implementation_guidelines'),
                T('results_maintenance_recommendations')
            ]
            
            for i, content in enumerate(contents, 1):
                st.write(f"{i}. {content}")
        
        with preview_col2:
            st.markdown(f"### {T('results_key_deliverables')}")
            
            # Create styled deliverables list
            deliverables_html = f"""
            <div style="background: var(--bg-secondary); border-radius: 12px; padding: 20px; margin: 15px 0; border: 1px solid var(--border-color);">
                <ul style="margin: 0; padding-left: 20px; color: var(--text-primary); line-height: 1.8;">
                    <li style="margin-bottom: 10px; color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">• {T('results_strategy')}: {recommendation['recommendation_type']}</li>
                    <li style="margin-bottom: 10px; color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">• {T('results_investment')}: ₹ {design_financial['total_cost']:,.0f}</li>
                    <li style="margin-bottom: 10px; color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">• {T('results_annual_benefit')}: ₹ {design_financial['annual_savings']:,.0f}</li>
                    <li style="margin-bottom: 10px; color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">• {T('results_harvest_potential')}: {recommendation['annual_potential']:,.0f} L/year</li>
                    <li style="margin-bottom: 10px; color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">• {T('results_efficiency_rating_label')}: {recommendation['efficiency_rating']}</li>
                    <li style="margin-bottom: 10px; color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">• {T('results_technical_specifications_drawings')}</li>
                </ul>
            </div>
            """
            st.markdown(deliverables_html, unsafe_allow_html=True)
        
        # Implementation next steps
        st.subheader(T('results_recommended_next_steps'))
        next_steps = [
            f"1. **{T('results_finalize_design')}**",
            f"2. **{T('results_obtain_permits')}**",
            f"3. **{T('results_source_materials')}**",
            f"4. **{T('results_schedule_installation')}**",
            f"5. **{T('results_setup_maintenance')}**"
        ]
        
        for step in next_steps:
            st.write(step)
            
    except Exception as e:
        st.error(T('results_pdf_generation_error') + f": {str(e)}")
        
        # Provide more specific error information
        error_type = type(e).__name__
        if "bytearray" in str(e).lower():
            st.info(f"💡 **{T('results_pdf_issue')}**: {T('results_pdf_compatibility')}")
            
            # Try alternative PDF generation without charts
            try:
                st.warning(T('results_generating_simplified'))
                pdf_bytes_simple = generate_pdf_report(params, recommendation, design_financial, site_data, None)
                
                if pdf_bytes_simple and isinstance(pdf_bytes_simple, bytes):
                    st.success(T('results_simplified_success'))
                    st.download_button(
                        label=T('results_download_simplified'),
                        data=pdf_bytes_simple,
                        file_name=f"Hydro_Assess_Simple_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        type="secondary"
                    )
                else:
                    st.error(T('results_unable_generate'))
            except Exception as e2:
                st.error(T('results_alternative_failed') + f": {str(e2)}")
        
        # Show debugging information
        with st.expander(f"🔧 {T('results_technical_details')}"):
            st.code(f"Error Type: {error_type}\nError Message: {str(e)}")
            st.info(T('results_error_persist'))

# --- MAIN APPLICATION ---
if __name__ == "__main__":
    main()