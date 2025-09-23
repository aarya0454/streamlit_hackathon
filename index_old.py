"""
Hydro-Assess Landing Page
Professional, trustworthy landing page for intelligent water potential assessment.
Designed with a modern engineering aesthetic and scientific credibility.
"""

import streamlit as st

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Hydro-Assess | Intelligent Water Potential Assessment",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional, modern design
st.markdown("""
    <style>
    /* Import Google Font - Inter for professional typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Hide Streamlit default elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none;}
    
    /* Global typography and layout */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Main container settings */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Professional static gradient background - Deep teal to navy */
    .stApp {
        background: linear-gradient(135deg, #004d40 0%, #011f4b 100%);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    /* Subtle overlay pattern for depth */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 150, 136, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 30%, rgba(0, 90, 156, 0.06) 0%, transparent 50%),
            radial-gradient(circle at 60% 70%, rgba(46, 139, 87, 0.04) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Remove white bar - transparent main container */
    .main-container {
        background: transparent;
        backdrop-filter: none;
        border-radius: 0;
        padding: 0;
        margin: 0;
        max-width: 100%;
        box-shadow: none;
    }
    
    /* Hero section - clean and minimal */
    .hero-section {
        text-align: center;
        padding: 5rem 1.5rem 3.5rem 1.5rem; /* More vertical padding */
        margin-bottom: 2rem;
        background: transparent;
        backdrop-filter: none;
        border-radius: 0;
        border: none;
        box-shadow: none;
    }
    
    /* Main title styling - Enhanced hierarchy */
    h1 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 1000;
        color: #ffffff !important;
        letter-spacing: -3px;
        text-align: center;
        font-size: 6rem;           /* Increased from 4.5rem */
        margin-bottom: 1.5rem;     /* Slightly more space below */
        text-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 2px 8px #1e3a8a;
        background: none !important;
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: unset !important;
        background-clip: unset !important;
        animation: titleGlow 2s ease-in-out infinite alternate;
        line-height: 1.08;
    }
    
    @keyframes titleGlow {
        0% { filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.4)) drop-shadow(0 0 40px rgba(30, 64, 175, 0.2)); }
        100% { filter: drop-shadow(0 0 30px rgba(59, 130, 246, 0.6)) drop-shadow(0 0 60px rgba(30, 64, 175, 0.3)); }
    }
    
    /* Tagline styling - Enhanced hierarchy */
    .tagline {
        font-size: 2.2rem;         /* Increased from 1.6rem */
        color: #ffffff;
        font-weight: 500;
        line-height: 1.4;
        margin-bottom: 2.5rem;
        text-align: center;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        opacity: 0.97;
        letter-spacing: 0.5px;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 0.95;
            transform: translateY(0);
        }
    }
    
    /* Section headers - Enhanced hierarchy */
    h2 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 800;
        color: #ffffff;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-size: 2.4rem;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        letter-spacing: -0.8px;
        animation: slideInLeft 0.8s ease-out;
        line-height: 1.2;
        text-align: center;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Content sections - clean and minimal */
    .content-section {
        background: transparent;
        backdrop-filter: none;
        padding: 1.5rem 0;
        border-radius: 0;
        margin: 2rem 0;
        border: none;
        box-shadow: none;
    }
    
    /* Paragraph text styling - Enhanced for better visibility */
    .stMarkdown p {
        font-size: 1.2rem;
        line-height: 1.8;
        color: #ffffff !important;
        font-weight: 300;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.5rem;
        letter-spacing: 0.3px;
    }
    
    /* Ensure all text is white */
    .stMarkdown, .stMarkdown * {
        color: #ffffff !important;
    }
    
    /* Fix any black text issues */
    p, span, div, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* CTA section styling - clean and minimal */
    .cta-section {
        margin: 2.5rem 0;
        text-align: center;
        background: transparent;
        backdrop-filter: none;
        padding: 1.5rem 0;
        border-radius: 0;
        border: none;
    }
    
    /* Button styling */
    .stLinkButton {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }
    
    .stLinkButton > a {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8, #1e40af) !important;
        color: white !important;
        padding: 1.2rem 3.5rem !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        border-radius: 50px !important;
        text-decoration: none !important;
        display: inline-block !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .stLinkButton > a::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stLinkButton > a:hover::before {
        left: 100%;
    }
    
    .stLinkButton > a:hover {
        background: linear-gradient(135deg, #1e40af, #1d4ed8, #3b82f6) !important;
        box-shadow: 0 15px 40px rgba(30, 64, 175, 0.6) !important;
        transform: translateY(-5px) scale(1.03) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Footer styling - clean and minimal */
    .custom-footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        margin-top: 4rem;
        padding: 2rem 0;
        background: transparent;
        backdrop-filter: none;
        border-radius: 0;
        border: none;
    }
    
    /* Enhanced hover effects for interactive elements */
    .interactive-card {
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
    }
    
    .interactive-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Enhanced button hover effects */
    .cta-button {
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.6) !important;
    }
    
    /* Pulse animation for important elements */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Enhanced mobile responsiveness */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.5rem;
            letter-spacing: -1px;
        }
        
        .tagline {
            font-size: 1.2rem;
            padding: 0 1rem;
        }
        
        .hero-section {
            padding: 2rem 1rem;
        }
        
        .content-section {
            padding: 1.5rem;
        }
        
        /* Mobile-specific grid adjustments */
        .mobile-grid {
            grid-template-columns: 1fr !important;
            gap: 1rem !important;
        }
        
        /* Mobile button adjustments */
        .mobile-button {
            padding: 1rem 2rem !important;
            font-size: 1.1rem !important;
        }
        
        /* Mobile text adjustments */
        .mobile-text {
            font-size: 0.9rem !important;
            line-height: 1.5 !important;
        }
        
        /* Ensure cards don't overflow on mobile */
        .stMarkdown div {
            max-width: 100% !important;
            overflow-x: hidden !important;
        }
        
        /* Mobile card adjustments */
        .stMarkdown div[style*="grid-template-columns"] {
            grid-template-columns: 1fr !important;
        }
    }
    
    @media (max-width: 480px) {
        h1 {
            font-size: 2rem;
        }
        
        .tagline {
            font-size: 1rem;
        }
        
        .hero-section {
            padding: 1.5rem 0.5rem;
        }
        
        /* Extra small mobile adjustments */
        .xs-mobile {
            padding: 1rem !important;
            margin: 0.5rem !important;
        }
        
        /* Ensure no horizontal scrolling */
        body, html {
            overflow-x: hidden !important;
        }
        
        .stApp {
            overflow-x: hidden !important;
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.2));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.4));
    }
    
    /* Simplified floating particles effect for better performance */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(30, 64, 175, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
        animation: float 30s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Enhanced text selection */
    ::selection {
        background: rgba(255, 255, 255, 0.3);
        color: #ffffff;
    }
    
    ::-moz-selection {
        background: rgba(255, 255, 255, 0.3);
        color: #ffffff;
    }
    
    /* Custom button styling to match theme */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8, #1e40af) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e40af, #1d4ed8, #3b82f6) !important;
        box-shadow: 0 12px 35px rgba(30, 64, 175, 0.6) !important;
        transform: translateY(-3px) scale(1.02) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Custom CSS for dark mode support
st.markdown("""
<style>
    /* Dark mode support for index page */
    .stApp[data-theme="dark"] h1,
    .stApp[data-theme="dark"] h2,
    .stApp[data-theme="dark"] h3,
    .stApp[data-theme="dark"] h4,
    .stApp[data-theme="dark"] h5,
    .stApp[data-theme="dark"] h6 {
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .stMarkdown {
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .stSelectbox label,
    .stApp[data-theme="dark"] .stNumberInput label,
    .stApp[data-theme="dark"] .stTextInput label {
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .stMetric {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .stMetric > div {
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .stMetric label {
        color: #ffffff !important;
    }
    
    /* Ensure hero section text is visible in dark mode */
    .stApp[data-theme="dark"] .hero-section h1 {
        color: #ffffff !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5) !important;
    }
    
    .stApp[data-theme="dark"] .hero-section p {
        color: rgba(255, 255, 255, 0.9) !important;
    }
</style>
""", unsafe_allow_html=True)

# Create main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Hero Section with enhanced design
st.markdown('<div class="hero-section">', unsafe_allow_html=True)

# Add floating elements for visual interest
st.markdown("""
<div style="position: relative; text-align: center;">
    <div style="position: absolute; top: -50px; left: 10%; width: 100px; height: 100px; background: radial-gradient(circle, rgba(59, 130, 246, 0.3), transparent); border-radius: 50%; animation: float 6s ease-in-out infinite;"></div>
    <div style="position: absolute; top: -30px; right: 15%; width: 60px; height: 60px; background: radial-gradient(circle, rgba(30, 64, 175, 0.2), transparent); border-radius: 50%; animation: float 8s ease-in-out infinite reverse;"></div>
    <div style="position: absolute; bottom: -40px; left: 20%; width: 80px; height: 80px; background: radial-gradient(circle, rgba(147, 197, 253, 0.25), transparent); border-radius: 50%; animation: float 7s ease-in-out infinite;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("# 🚰 Hydro-Asses")
st.markdown('<p class="tagline"><strong>From Rooftop to Aquifer: Instant, Intelligent Water Potential Assessment</strong></p>', 
            unsafe_allow_html=True)

# Add stats with hydro-geological themed icons
st.markdown("""
<div style="display: flex; justify-content: center; gap: 6rem; margin: 3rem 0; flex-wrap: wrap;">
    <div style="text-align: center;">
        <div style="font-size: 4.5rem; font-weight: 900; color: #ffffff; text-shadow: 0 6px 32px rgba(0, 0, 0, 0.4); margin-bottom: 1.2rem;">🌊</div>
        <div style="font-size: 2rem; color: #fff; font-weight: 800; text-shadow: 0 2px 12px rgba(0,0,0,0.25);">Instant Analysis</div>
    </div>
    <div style="text-align: center;">
        <div style="font-size: 4.5rem; font-weight: 900; color: #ffffff; text-shadow: 0 6px 32px rgba(0, 0, 0, 0.4); margin-bottom: 1.2rem;">🗺️</div>
        <div style="font-size: 2rem; color: #fff; font-weight: 800; text-shadow: 0 2px 12px rgba(0,0,0,0.25);">Global Coverage</div>
    </div>
    <div style="text-align: center;">
        <div style="font-size: 4.5rem; font-weight: 900; color: #ffffff; text-shadow: 0 6px 32px rgba(0, 0, 0, 0.4); margin-bottom: 1.2rem;">📱</div>
        <div style="font-size: 2rem; color: #fff; font-weight: 800; text-shadow: 0 2px 12px rgba(0,0,0,0.25);">Mobile-First</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Call-to-Action Section - Enhanced with multiple options
st.markdown('<div class="cta-section">', unsafe_allow_html=True)
st.markdown("## 🚀 Discover Your Property's Potential")
st.markdown("""
<p style="font-size: 1.4rem; margin-bottom: 2rem; text-align: center; color: rgba(255, 255, 255, 0.95); font-weight: 300; letter-spacing: 0.5px;">
✨ Get instant insights about your property's water management potential with our AI-powered assessment tool ✨
</p>
""", unsafe_allow_html=True)

# Create navigation buttons for different tools - Responsive design
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05)); padding: 2rem; border-radius: 20px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(15px); transition: all 0.3s ease; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💧</div>
        <h3 style="color: #ffffff; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Harvesting Potential</h3>
        <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 1.5rem; line-height: 1.6; font-size: 1rem;">Analyze your property's rainwater harvesting potential using soil data, rainfall patterns, and terrain analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💧 Analyze Harvesting Potential", key="calc_btn", use_container_width=True):
        st.switch_page("pages/calc.py")

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05)); padding: 2rem; border-radius: 20px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(15px); transition: all 0.3s ease; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🗺️</div>
        <h3 style="color: #ffffff; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Area Calculator</h3>
        <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 1.5rem; line-height: 1.6; font-size: 1rem;">Draw on satellite imagery to calculate precise areas for your water management projects.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗺️ Calculate Area", key="map_btn", use_container_width=True):
        st.switch_page("pages/map.py")

# Add a demo section - Responsive design
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)); padding: 2rem; border-radius: 20px; margin: 2rem 0; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(15px);">
    <h3 style="color: #ffffff; text-align: center; margin-bottom: 1.5rem; font-size: 1.8rem;">🎯 How It Works</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; text-align: center;">
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 15px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📍</div>
            <h4 style="color: #ffffff; margin-bottom: 0.5rem; font-size: 1.2rem; font-weight: 600;">Enter Location</h4>
            <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; line-height: 1.5;">Provide your property coordinates or use GPS</p>
        </div>
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 15px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔬</div>
            <h4 style="color: #ffffff; margin-bottom: 0.5rem; font-size: 1.2rem; font-weight: 600;">AI Analysis</h4>
            <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; line-height: 1.5;">Our system fetches soil and rainfall data</p>
        </div>
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 15px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <h4 style="color: #ffffff; margin-bottom: 0.5rem; font-size: 1.2rem; font-weight: 600;">Get Results</h4>
            <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; line-height: 1.5;">Receive instant water potential assessment</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Problem Section with enhanced readability
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown("## 🔍 The Challenge: A Disconnected Approach")
st.markdown("""
The current landscape of water management tools presents a critical gap. On one end, we have 
oversimplified calculators that provide basic collection estimates but miss the bigger picture. 
On the other, complex GIS platforms require extensive expertise and resources, making them 
inaccessible to most property owners and small-scale planners. 

**The core issue:** Users can calculate how much rainwater they can collect from their rooftops, 
but determining whether they can safely recharge it into the ground remains a mystery—leaving 
tremendous potential untapped.

<div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0; border-left: 4px solid #ff6b6b;">
<strong>💡 Key Insight:</strong> The disconnect between collection and recharge assessment is the 
biggest barrier to effective water management at the property level.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Solution Section with enhanced readability
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown("## 💡 Our Solution: An Integrated, Instant Assessment")
st.markdown("""
Hydro-Assess bridges this gap with a **mobile-first tool** that combines the simplicity of a 
smartphone app with the analytical power of professional GIS systems. By automatically 
leveraging your phone's GPS location, our platform instantly fetches critical local data—**rainfall 
patterns, soil composition, and terrain slope**—to deliver a comprehensive assessment of both 
rainwater harvesting and groundwater recharge potential. 

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
<div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1)); padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.3); backdrop-filter: blur(15px); transition: all 0.3s ease; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);">
<strong style="font-size: 1.2rem; display: block; margin-bottom: 0.8rem; color: #ffffff;">📱 Mobile-First</strong>
<span style="font-size: 1rem; opacity: 0.9; color: #ffffff;">Simple smartphone interface</span>
</div>
<div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1)); padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.3); backdrop-filter: blur(15px); transition: all 0.3s ease; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);">
<strong style="font-size: 1.2rem; display: block; margin-bottom: 0.8rem; color: #ffffff;">🌍 GPS-Powered</strong>
<span style="font-size: 1rem; opacity: 0.9; color: #ffffff;">Automatic location detection</span>
</div>
<div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1)); padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.3); backdrop-filter: blur(15px); transition: all 0.3s ease; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);">
<strong style="font-size: 1.2rem; display: block; margin-bottom: 0.8rem; color: #ffffff;">⚡ Instant Results</strong>
<span style="font-size: 1rem; opacity: 0.9; color: #ffffff;">No expertise required</span>
</div>
</div>
y
**No expertise required, no complex setup needed.** Just instant, actionable insights about your property's water management capacity.
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Add key features section - More authentic and professional
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)); padding: 3rem 2rem; border-radius: 20px; margin: 3rem 0; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(15px);">
    <h3 style="color: #ffffff; text-align: center; margin-bottom: 2rem; font-size: 2rem; font-weight: 700;">🔬 Powered by Advanced Technology</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #3b82f6;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🌍</div>
            <h4 style="color: #ffffff; margin-bottom: 0.5rem; font-size: 1.3rem; font-weight: 600;">ISRIC SoilGrids Integration</h4>
            <p style="color: rgba(255, 255, 255, 0.9); line-height: 1.6; font-size: 0.95rem;">Access global soil data from the world's most comprehensive soil database for accurate assessments.</p>
        </div>
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #1e40af;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🛰️</div>
            <h4 style="color: #ffffff; margin-bottom: 0.5rem; font-size: 1.3rem; font-weight: 600;">Satellite Imagery Analysis</h4>
            <p style="color: rgba(255, 255, 255, 0.9); line-height: 1.6; font-size: 0.95rem;">High-resolution satellite imagery for precise area calculations and terrain analysis.</p>
        </div>
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #1d4ed8;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">⚡</div>
            <h4 style="color: #ffffff; margin-bottom: 0.5rem; font-size: 1.3rem; font-weight: 600;">Real-time Processing</h4>
            <p style="color: rgba(255, 255, 255, 0.9); line-height: 1.6; font-size: 0.95rem;">Instant results powered by cloud computing and optimized algorithms for immediate insights.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
<div class="custom-footer">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 3rem; margin-bottom: 3rem; align-items: start;">
<div style="text-align: center;">
<div style="margin-bottom: 1rem; font-size: 3rem;">🏭</div>
<div style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #ffffff;">🇮🇳 Designed for India</div>
<div style="font-size: 0.95rem; opacity: 0.8; color: #ffffff;">Tailored for Indian water challenges and climate patterns</div>
</div>
<div style="text-align: center;">
<div style="font-size: 3rem; margin-bottom: 1rem;">🔬</div>
<div style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #ffffff;">Advanced Analytics</div>
<div style="font-size: 0.95rem; opacity: 0.8; color: #ffffff;">Powered by ISRIC SoilGrids and GIS technology</div>
</div>
<div style="text-align: center;">
<div style="font-size: 3rem; margin-bottom: 1rem;">📱</div>
<div style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #ffffff;">Mobile-First</div>
<div style="font-size: 0.95rem; opacity: 0.8; color: #ffffff;">Accessible anywhere, anytime on any device</div>
</div>
<div style="text-align: center;">
<div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
<div style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #ffffff;">Instant Results</div>
<div style="font-size: 0.95rem; opacity: 0.8; color: #ffffff;">Get assessments in seconds, not hours</div>
</div>
</div>

<div style="border-top: 1px solid rgba(255, 255, 255, 0.2); padding-top: 2rem; text-align: center;">
<div style="margin-bottom: 1rem;">
<span style="font-size: 1.5rem;">💧</span> <strong style="color: #ffffff; font-size: 1.2rem;">Smart water management for sustainable futures</strong>
</div>
<div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-top: 1rem;">
© 2024 Hydro-Assess. Empowering sustainable water management through technology.
</div>
</div>
</div>
""", unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)