# Custom CSS for Hydro-Assess Application
# This file contains the CSS styling to be injected into your Streamlit app
# Add this code snippet to your main application file or any page where you want the styling

import streamlit as st

# Custom CSS for enhanced UI polish
custom_css = """
<style>
    /* ===== GLOBAL STYLES ===== */
    
    /* Smooth transitions for all interactive elements */
    * {
        transition: all 0.2s ease-in-out;
    }
    
    /* Improved font rendering */
    body {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* ===== BUTTON STYLES ===== */
    
    /* Primary buttons with rounded corners and subtle shadows */
    .stButton > button {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 102, 204, 0.1);
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        letter-spacing: 0.02em;
    }
    
    /* Button hover effects */
    .stButton > button:hover {
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.15);
        transform: translateY(-1px);
        border-color: rgba(0, 102, 204, 0.3);
    }
    
    /* Button active state */
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* ===== INPUT FIELD STYLES ===== */
    
    /* Text inputs, text areas, and select boxes */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        border-radius: 6px;
        border: 1.5px solid #E0E4E8;
        padding: 0.5rem 0.75rem;
    }
    
    /* Input focus states */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus-within {
        border-color: #0066CC;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
        outline: none;
    }
    
    /* ===== SLIDER STYLES ===== */
    
    /* Slider track */
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, #0066CC 0%, #0066CC var(--slider-value), #E0E4E8 var(--slider-value), #E0E4E8 100%);
    }
    
    /* Slider thumb */
    .stSlider > div > div > div > div > div {
        background-color: #0066CC;
        border: 2px solid white;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    }
    
    /* ===== CARD AND CONTAINER STYLES ===== */
    
    /* Expander containers */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background-color: rgba(240, 242, 245, 0.5);
        border: 1px solid rgba(224, 228, 232, 0.5);
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(240, 242, 245, 0.8);
    }
    
    /* Info, warning, error, and success boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        padding: 1rem;
    }
    
    /* ===== SIDEBAR STYLES ===== */
    
    /* Sidebar container */
    section[data-testid="stSidebar"] {
        background-color: #F0F2F5;
        border-right: 1px solid #E0E4E8;
    }
    
    /* Sidebar content padding */
    section[data-testid="stSidebar"] > div {
        padding: 2rem 1rem;
    }
    
    /* ===== TABLE STYLES ===== */
    
    /* Data tables and dataframes */
    .dataframe {
        border: none !important;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .dataframe thead th {
        background-color: #F0F2F5 !important;
        color: #1E2329 !important;
        font-weight: 600;
        padding: 0.75rem !important;
        border-bottom: 2px solid #E0E4E8 !important;
    }
    
    .dataframe tbody td {
        padding: 0.75rem !important;
        border-bottom: 1px solid #F0F2F5 !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(0, 102, 204, 0.02) !important;
    }
    
    /* ===== METRIC STYLES ===== */
    
    /* Metric containers */
    [data-testid="metric-container"] {
        background-color: rgba(240, 242, 245, 0.3);
        border: 1px solid rgba(224, 228, 232, 0.5);
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Metric values */
    [data-testid="metric-container"] > div > div > div > div > div {
        font-weight: 600;
    }
    
    /* ===== CHART STYLES ===== */
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        padding: 0.5rem;
        background-color: white;
    }
    
    /* ===== SPACING AND LAYOUT ===== */
    
    /* Consistent spacing between elements */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Main content area padding */
    .main > div {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* ===== TYPOGRAPHY ===== */
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1E2329;
        font-weight: 600;
        line-height: 1.4;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: 2.5rem;
        border-bottom: 2px solid #E0E4E8;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 2rem;
    }
    
    h3 {
        font-size: 1.5rem;
    }
    
    /* Paragraphs */
    p {
        line-height: 1.6;
        color: #4A5568;
    }
    
    /* Links */
    a {
        color: #0066CC;
        text-decoration: none;
        font-weight: 500;
    }
    
    a:hover {
        text-decoration: underline;
        color: #0052A3;
    }
    
    /* ===== ACCESSIBILITY IMPROVEMENTS ===== */
    
    /* Focus indicators for keyboard navigation */
    *:focus {
        outline: 2px solid #0066CC;
        outline-offset: 2px;
    }
    
    /* High contrast mode for better readability */
    @media (prefers-contrast: high) {
        * {
            border-width: 2px !important;
        }
        
        .stButton > button {
            border: 2px solid #1E2329 !important;
        }
    }
    
    /* ===== DARK MODE STYLES ===== */
    /* These styles will automatically apply when dark theme is enabled */
    
    @media (prefers-color-scheme: dark) {
        /* Dark mode button styles */
        .stButton > button {
            background-color: #242B3D;
            color: #E8EAED;
            border-color: rgba(0, 212, 255, 0.2);
        }
        
        .stButton > button:hover {
            background-color: #2A3142;
            box-shadow: 0 4px 8px rgba(0, 212, 255, 0.2);
            border-color: rgba(0, 212, 255, 0.4);
        }
        
        /* Dark mode input styles */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            background-color: #242B3D;
            border-color: #3A4255;
            color: #E8EAED;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > div:focus-within {
            border-color: #00D4FF;
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
        }
        
        /* Dark mode sidebar */
        section[data-testid="stSidebar"] {
            background-color: #242B3D;
            border-right-color: #3A4255;
        }
        
        /* Dark mode tables */
        .dataframe thead th {
            background-color: #242B3D !important;
            color: #E8EAED !important;
            border-bottom-color: #3A4255 !important;
        }
        
        .dataframe tbody td {
            background-color: #1A1F2E !important;
            color: #E8EAED !important;
            border-bottom-color: #242B3D !important;
        }
        
        .dataframe tbody tr:hover {
            background-color: rgba(0, 212, 255, 0.05) !important;
        }
        
        /* Dark mode metrics */
        [data-testid="metric-container"] {
            background-color: rgba(36, 43, 61, 0.5);
            border-color: rgba(58, 66, 85, 0.5);
        }
        
        /* Dark mode typography */
        h1, h2, h3, h4, h5, h6 {
            color: #E8EAED;
        }
        
        h1 {
            border-bottom-color: #3A4255;
        }
        
        p {
            color: #B8BCC8;
        }
        
        a {
            color: #00D4FF;
        }
        
        a:hover {
            color: #00A8CC;
        }
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main > div {
            padding: 1rem 0.5rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .stButton > button {
            width: 100%;
            padding: 0.75rem;
        }
    }
    
    /* ===== CUSTOM SCROLLBAR ===== */
    
    /* Webkit browsers */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F0F2F5;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #B8BCC8;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9CA3AF;
    }
    
    /* Firefox */
    * {
        scrollbar-width: thin;
        scrollbar-color: #B8BCC8 #F0F2F5;
    }
</style>
"""

# Function to inject the custom CSS into your Streamlit app
def apply_custom_theme():
    """
    Apply custom CSS theme to the Streamlit application.
    Call this function at the beginning of your app or page.
    
    Example usage:
        import streamlit as st
        from custom_theme_css import apply_custom_theme
        
        # Apply the custom theme
        apply_custom_theme()
        
        # Your app code continues here...
        st.title("My App")
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# If you want to use this directly without importing, just copy this line to your app:
# st.markdown(custom_css, unsafe_allow_html=True)
