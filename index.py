"""
Hydro-Assess - Smart India Hackathon 2025
A water management assessment tool for rainwater harvesting
Built by Team Aether Spark for SIH 2025
"""

import streamlit as st
import datetime
from translator import T, language_selector, main_page_language_selector 
from locales import translations


# Initialize language in session state FIRST
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Page configuration - must be the first Streamlit command
# Use a generic title initially, will be updated via JavaScript
st.set_page_config(
    page_title='Hydro-Assess',
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"  # Changed to expanded to show language selector
)

# Professional CSS with static gradient and clean typography
st.markdown("""
    <style>
    /* Import Google Font - Inter for professional typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none;}
    
    /* Global typography and layout */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Main container settings */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1280px;
        margin: 0 auto;
    }
    
    /* Mobile responsive container */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-bottom: 1rem;
        }
    }
    
    /* Professional static gradient background */
    .stApp {
        background: linear-gradient(135deg, #004d40 0%, #011f4b 100%);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    /* Subtle topographical pattern overlay */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
    }
    
    /* Typography hierarchy */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #ffffff;
        font-size: 3.5rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    h2 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #ffffff;
        font-size: 2.25rem;
        line-height: 1.2;
        letter-spacing: -0.01em;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #ffffff;
        font-size: 1.5rem;
        line-height: 1.3;
        margin-bottom: 1rem;
    }
    
    p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.125rem;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Mobile responsive typography */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        h2 {
            font-size: 1.75rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            font-size: 1.25rem;
            margin-bottom: 0.75rem;
        }
        
        p {
            font-size: 1rem;
            line-height: 1.6;
        }
    }
    
    /* Card styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 2.5rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 320px;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        box-sizing: border-box;
        width: 100%;
        max-width: 100%;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
        border-color: rgba(46, 139, 87, 0.3);
    }
    
    .feature-card h3 {
        margin-bottom: 1.25rem;
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .feature-card p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
        flex-grow: 1;
        text-align: center;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Mobile responsive feature cards */
    @media (max-width: 768px) {
        .feature-card {
            padding: 1.5rem;
            margin: 0.5rem 0;
            min-height: 280px;
            border-radius: 12px;
        }
        
        .feature-card h3 {
            font-size: 1.25rem;
            margin-bottom: 1rem;
        }
        
        .feature-card p {
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .feature-card {
            padding: 1.25rem;
            min-height: 250px;
        }
        
        .feature-card h3 {
            font-size: 1.125rem;
        }
        
        .feature-card p {
            font-size: 0.875rem;
        }
    }
    
    .icon-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 64px;
        height: 64px;
        margin: 0 auto 1.5rem auto;
        background: rgba(46, 139, 87, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(46, 139, 87, 0.2);
    }
    
    .icon-wrapper svg {
        width: 32px;
        height: 32px;
    }
    
    /* Mobile responsive icon wrapper */
    @media (max-width: 768px) {
        .icon-wrapper {
            width: 56px;
            height: 56px;
            margin: 0 auto 1rem auto;
        }
        
        .icon-wrapper svg {
            width: 28px;
            height: 28px;
        }
    }
    
    @media (max-width: 480px) {
        .icon-wrapper {
            width: 48px;
            height: 48px;
        }
        
        .icon-wrapper svg {
            width: 24px;
            height: 24px;
        }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57 0%, #005A9C 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        padding: 1rem 2.5rem;
        font-size: 1.125rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(46, 139, 87, 0.3);
        text-transform: none;
        font-family: 'Inter', sans-serif;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(46, 139, 87, 0.4);
        background: linear-gradient(135deg, #247349 0%, #004d85 100%);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Mobile responsive buttons */
    @media (max-width: 768px) {
        .stButton > button {
            padding: 0.875rem 2rem;
            font-size: 1rem;
            border-radius: 40px;
        }
    }
    
    @media (max-width: 480px) {
        .stButton > button {
            padding: 0.75rem 1.5rem;
            font-size: 0.9rem;
            letter-spacing: 0.25px;
        }
    }
    
    /* Icon styling */
    .icon-wrapper {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        margin-bottom: 1rem;
    }
    
    .icon-wrapper svg {
        width: 100%;
        height: 100%;
    }
    
    /* Section styling */
    .section {
        margin: 4rem 0;
        position: relative;
        z-index: 1;
    }
    
    /* Header bar - transparent centered design */
    .header-bar {
        background: transparent;
        padding: 3rem 0 2rem 0;
        margin-bottom: 1rem;
    }

    .header-content {
        max-width: 1280px;
        margin: 0 auto;
        padding: 0 2rem;
        text-align: center;
    }

    .logo-section {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 0.75rem;
    }

    .logo-icon {
        font-size: 4.5rem;
        filter: drop-shadow(0 6px 12px rgba(46, 139, 87, 0.4));
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .logo-text {
        font-size: 3.25rem;
        font-weight: 900;
        color: white;
        line-height: 1;
        letter-spacing: -0.025em;
        text-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
        background: linear-gradient(135deg, #ffffff 0%, #e0f2f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .logo-subtitle {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.85);
        font-weight: 500;
        margin-top: 0.75rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    
    /* Mobile responsive logo section */
    @media (max-width: 768px) {
        .logo-section {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
        }
        
        .logo-icon {
            font-size: 3.5rem;
        }
        
        .logo-text {
            font-size: 2.5rem;
        }
        
        .logo-subtitle {
            font-size: 1rem;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .logo-section {
            gap: 0.75rem;
        }
        
        .logo-icon {
            font-size: 3rem;
        }
        
        .logo-text {
            font-size: 2rem;
        }
        
        .logo-subtitle {
            font-size: 0.9rem;
            letter-spacing: 0.5px;
        }
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 2rem 0 3rem 0;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .hero-title {
        font-size: 3.75rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        color: #ffffff;
        line-height: 1.1;
        letter-spacing: -0.03em;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        margin-bottom: 2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .tagline {
        font-size: 1.375rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.9);
        margin: 2rem auto;
        line-height: 1.6;
        max-width: 900px;
        text-align: center;
        padding: 0 1rem;
    }
    
    /* Mobile responsive hero section */
    @media (max-width: 768px) {
        .hero-section {
            padding: 1.5rem 0 2rem 0;
            margin-bottom: 1.5rem;
        }
        
        .hero-title {
            font-size: 2.75rem;
            margin-bottom: 0.75rem;
        }
        
        .hero-subtitle {
            font-size: 1rem;
            letter-spacing: 1.5px;
            margin-bottom: 1.5rem;
        }
        
        .tagline {
            font-size: 1.125rem;
            margin: 1.5rem auto;
            padding: 0 0.5rem;
            max-width: 100%;
        }
    }
    
    @media (max-width: 480px) {
        .hero-section {
            padding: 1rem 0 1.5rem 0;
        }
        
        .hero-title {
            font-size: 2.25rem;
        }
        
        .hero-subtitle {
            font-size: 0.9rem;
            letter-spacing: 1px;
        }
        
        .tagline {
            font-size: 1rem;
            margin: 1rem auto;
        }
    }
    
    /* Step cards */
    .step-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 280px;
        box-sizing: border-box;
        width: 100%;
        max-width: 100%;
    }
    
    .step-card:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2E8B57 0%, #005A9C 100%);
        color: white;
        font-weight: 700;
        margin: 0 auto 1.5rem auto;
        font-size: 1.125rem;
    }
    
    .step-card h4 {
        color: white;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .step-card p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1rem;
        text-align: center;
        flex-grow: 1;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Mobile responsive step cards */
    @media (max-width: 768px) {
        .step-card {
            padding: 1.5rem;
            margin: 0.5rem 0;
            min-height: 240px;
            border-radius: 12px;
        }
        
        .step-number {
            width: 36px;
            height: 36px;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        
        .step-card h4 {
            font-size: 1.125rem;
            margin-bottom: 0.75rem;
        }
        
        .step-card p {
            font-size: 0.875rem;
            line-height: 1.5;
        }
    }
    
    @media (max-width: 480px) {
        .step-card {
            padding: 1.25rem;
            min-height: 220px;
        }
        
        .step-number {
            width: 32px;
            height: 32px;
            font-size: 0.9rem;
        }
        
        .step-card h4 {
            font-size: 1rem;
        }
        
        .step-card p {
            font-size: 0.8rem;
        }
    }
    
    /* Quote styling */
    .testimonial {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #2E8B57;
        padding: 1.5rem;
        border-radius: 8px;
        font-style: italic;
        margin: 2rem 0;
    }
    
    .testimonial-author {
        font-style: normal;
        font-weight: 600;
        color: #2E8B57;
        margin-top: 1rem;
        display: block;
    }
    
    /* About section */
    .about-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    .stat-box {
        text-align: center;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        box-sizing: border-box;
        width: 100%;
        max-width: 100%;
    }
    
    .stat-box:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(46, 139, 87, 0.5);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 900;
        color: #2E8B57;
        margin-bottom: 0.5rem;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Mobile responsive stat boxes */
    @media (max-width: 768px) {
        .stat-box {
            padding: 1.25rem;
            border-radius: 10px;
        }
        
        .stat-number {
            font-size: 2rem;
            margin-bottom: 0.4rem;
        }
    }
    
    @media (max-width: 480px) {
        .stat-box {
            padding: 1rem;
        }
        
        .stat-number {
            font-size: 1.75rem;
        }
    }
    
    /* Global mobile optimizations */
    @media (max-width: 768px) {
        /* Ensure all content fits within viewport */
        * {
            max-width: 100% !important;
            box-sizing: border-box !important;
        }
        
        /* Prevent horizontal overflow */
        .stApp, .main, .block-container {
            overflow-x: hidden !important;
        }
        
        /* Streamlit column responsiveness */
        .row-widget.stHorizontal > div {
            flex: 1 1 100% !important;
            min-width: 0 !important;
        }
    }
    
    @media (max-width: 480px) {
        /* Extra small screen optimizations */
        .section {
            margin: 2rem 0 !important;
        }
        
        .header-content {
            padding: 0 1rem !important;
        }
    }
    
    /* System works cards hover effects */
    .system-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .system-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2) !important;
        border-color: rgba(46, 139, 87, 0.4) !important;
        background: rgba(255, 255, 255, 0.12) !important;
    }

    .system-card:hover .icon-bg {
        background: linear-gradient(135deg, #247349, #004d85) !important;
        transform: scale(1.1);
    }

    .system-card:hover h4 {
        color: #ffffff !important;
    }
    
    /* Footer styling */
    .footer {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 4rem;
        padding-top: 2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.5rem;
        }
        
        .hero-title {
            font-size: 2.75rem;
        }
        
        .tagline {
            font-size: 1.25rem;
        }
        
        h2 {
            font-size: 1.875rem;
        }
        
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    
    /* Accessibility */
    a:focus,
    button:focus {
        outline: 2px solid #2E8B57;
        outline-offset: 2px;
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .feature-card {
            border: 2px solid rgba(255, 255, 255, 0.5);
        }
    }
    
    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Add language selector to main page (at the top)
main_page_language_selector()

# Centered Header
st.markdown(f"""
<div class="header-bar">
    <div class="header-content">
        <div class="logo-section">
            <div class="logo-icon">💧</div>
            <div>
                <div class="logo-text">{T('app_name')}</div>
                <div class="logo-subtitle">{T('app_subtitle')}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
<div class="hero-section">
    <div class="hero-subtitle">{T('hero_subtitle')}</div>
    <h1 class="hero-title">{T('hero_title')}</h1>
    <div style="max-width: 950px; margin: 0 auto; text-align: center; padding: 0 2rem;">
        <p class="tagline">
            {T('hero_description')}
        </p>
    </div>
    <div style="margin-top: 3rem; display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; max-width: 1100px; margin-left: auto; margin-right: auto; padding: 0 2rem; align-items: stretch;">
        <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.06); border-radius: 20px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; cursor: pointer; flex: 1; min-width: 240px; max-width: 320px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" onmouseover="this.style.transform='translateY(-8px)'; this.style.background='rgba(255,255,255,0.1)'; this.style.borderColor='rgba(46, 139, 87, 0.5)'; this.style.boxShadow='0 16px 48px rgba(0, 0, 0, 0.2)'; this.querySelector('.stat-number').style.color='#ffffff'; this.querySelector('.stat-number').style.transform='scale(1.15)'; this.querySelector('.stat-label').style.color='rgba(255, 255, 255, 0.95)'" onmouseout="this.style.transform='translateY(0px)'; this.style.background='rgba(255,255,255,0.06)'; this.style.borderColor='rgba(255,255,255,0.12)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.1)'; this.querySelector('.stat-number').style.color='#2E8B57'; this.querySelector('.stat-number').style.transform='scale(1)'; this.querySelector('.stat-label').style.color='rgba(255, 255, 255, 0.8)'">
            <div class="stat-number" style="font-size: 3rem; font-weight: 900; color: #2E8B57; margin-bottom: 1rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">2</div>
            <div class="stat-label" style="color: rgba(255,255,255,0.8); font-size: 1rem; font-weight: 600; line-height: 1.4;">{T('stat_api_integrations')}<br><span style="font-size: 0.875rem; font-weight: 400; opacity: 0.9;">{T('stat_api_subtitle')}</span></div>
        </div>
        <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.06); border-radius: 20px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; cursor: pointer; flex: 1; min-width: 240px; max-width: 320px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" onmouseover="this.style.transform='translateY(-8px)'; this.style.background='rgba(255,255,255,0.1)'; this.style.borderColor='rgba(46, 139, 87, 0.5)'; this.style.boxShadow='0 16px 48px rgba(0, 0, 0, 0.2)'; this.querySelector('.stat-number').style.color='#ffffff'; this.querySelector('.stat-number').style.transform='scale(1.15)'; this.querySelector('.stat-label').style.color='rgba(255, 255, 255, 0.95)'" onmouseout="this.style.transform='translateY(0px)'; this.style.background='rgba(255,255,255,0.06)'; this.style.borderColor='rgba(255,255,255,0.12)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.1)'; this.querySelector('.stat-number').style.color='#2E8B57'; this.querySelector('.stat-number').style.transform='scale(1)'; this.querySelector('.stat-label').style.color='rgba(255, 255, 255, 0.8)'">
            <div class="stat-number" style="font-size: 3rem; font-weight: 900; color: #2E8B57; margin-bottom: 1rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">3</div>
            <div class="stat-label" style="color: rgba(255,255,255,0.8); font-size: 1rem; font-weight: 600; line-height: 1.4;">{T('stat_system_types')}<br><span style="font-size: 0.875rem; font-weight: 400; opacity: 0.9;">{T('stat_system_subtitle')}</span></div>
        </div>
        <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.06); border-radius: 20px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; cursor: pointer; flex: 1; min-width: 240px; max-width: 320px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" onmouseover="this.style.transform='translateY(-8px)'; this.style.background='rgba(255,255,255,0.1)'; this.style.borderColor='rgba(46, 139, 87, 0.5)'; this.style.boxShadow='0 16px 48px rgba(0, 0, 0, 0.2)'; this.querySelector('.stat-number').style.color='#ffffff'; this.querySelector('.stat-number').style.transform='scale(1.15)'; this.querySelector('.stat-label').style.color='rgba(255, 255, 255, 0.95)'" onmouseout="this.style.transform='translateY(0px)'; this.style.background='rgba(255,255,255,0.06)'; this.style.borderColor='rgba(255,255,255,0.12)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.1)'; this.querySelector('.stat-number').style.color='#2E8B57'; this.querySelector('.stat-number').style.transform='scale(1)'; this.querySelector('.stat-label').style.color='rgba(255, 255, 255, 0.8)'">
            <div class="stat-number" style="font-size: 3rem; font-weight: 900; color: #2E8B57; margin-bottom: 1rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">6</div>
            <div class="stat-label" style="color: rgba(255,255,255,0.8); font-size: 1rem; font-weight: 600; line-height: 1.4;">{T('stat_team_members')}<br><span style="font-size: 0.875rem; font-weight: 400; opacity: 0.9;">{T('stat_team_subtitle')}</span></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Primary CTAs
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="feature-card">
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7V12C2 16.5 4.23 20.68 7.62 23.15L12 21L16.38 23.15C19.77 20.68 22 16.5 22 12V7L12 2Z" stroke="#2E8B57" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 8V16" stroke="#2E8B57" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="12" r="3" stroke="#2E8B57" stroke-width="2"/>
            </svg>
        </div>
        <h3>{T('feature_map_title')}</h3>
        <p style="font-size: 1rem; color: rgba(255,255,255,0.8); margin-bottom: 1.5rem;">
            {T('feature_map_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(T('nav_map'), key="map_btn", use_container_width=True):
        st.switch_page("pages/map.py")

with col2:
    st.markdown(f"""
    <div class="feature-card">
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 9V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H8V12H16V22H20C20.5304 22 21.0391 21.7893 21.4142 21.4142C21.7893 21.0391 22 20.5304 22 20V9L12 2Z" stroke="#005A9C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 15H15" stroke="#005A9C" stroke-width="2" stroke-linecap="round"/>
            </svg>
        </div>
        <h3>{T('feature_assessment_title')}</h3>
        <p style="font-size: 1rem; color: rgba(255,255,255,0.8); margin-bottom: 1.5rem;">
            {T('feature_assessment_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(T('nav_start_assessment'), key="calc_btn", use_container_width=True):
        st.switch_page("pages/calc.py")

# About Our Team
st.markdown(f"""
<div class="section">
    <h2 style="text-align: center; margin-bottom: 3rem;">{T('about_title')}</h2>
    <div class="about-card">
        <p style="font-size: 1.125rem; text-align: center; margin-bottom: 2rem;">
            {T('about_description_1')} {T('about_description_2')}
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
            <div class="stat-box">
                <div class="stat-number">6</div>
                <div class="stat-label">{T('stat_team_members')}</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{T('stat_sih_year')}</div>
                <div class="stat-label">{T('stat_year_2025')}</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">3</div>
                <div class="stat-label">{T('features_title')}</div>
            </div>
        </div>
        <p style="text-align: center; font-size: 1rem; color: rgba(255,255,255,0.8); margin-top: 2rem;">
            {T('about_project_desc')}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# How It Works - Technical Details
st.markdown(f"""
<div class="section">
    <h2 style="text-align: center; margin-bottom: 4rem;">{T('how_it_works_title')}</h2>
    <div style="background: rgba(255,255,255,0.05); border-radius: 20px; padding: 3rem; margin-bottom: 3rem; border: 1px solid rgba(255,255,255,0.1);">
        <p style="font-size: 1.25rem; text-align: center; color: rgba(255,255,255,0.9); margin-bottom: 4rem; max-width: 900px; margin-left: auto; margin-right: auto;">
            {T('how_it_works_desc')}
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 2rem;">
            <div class="system-card" style="background: rgba(255,255,255,0.08); padding: 2.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div class="icon-bg" style="width: 48px; height: 48px; background: linear-gradient(135deg, #2E8B57, #005A9C); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; transition: all 0.3s ease;">
                        🗺️
                    </div>
                    <h4 style="color: #2E8B57; margin: 0; font-size: 1.3rem; font-weight: 600;">{T('system_interactive_mapping')}</h4>
                </div>
                <p style="font-size: 1rem; color: rgba(255,255,255,0.85); line-height: 1.7; margin: 0;">
                    {T('system_interactive_mapping_desc')}
                </p>
            </div>
            <div class="system-card" style="background: rgba(255,255,255,0.08); padding: 2.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div class="icon-bg" style="width: 48px; height: 48px; background: linear-gradient(135deg, #2E8B57, #005A9C); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; transition: all 0.3s ease;">
                        🌧️
                    </div>
                    <h4 style="color: #2E8B57; margin: 0; font-size: 1.3rem; font-weight: 600;">{T('system_rainfall_analysis')}</h4>
                </div>
                <p style="font-size: 1rem; color: rgba(255,255,255,0.85); line-height: 1.7; margin: 0;">
                    {T('system_rainfall_analysis_desc')}
                </p>
            </div>
            <div class="system-card" style="background: rgba(255,255,255,0.08); padding: 2.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div class="icon-bg" style="width: 48px; height: 48px; background: linear-gradient(135deg, #2E8B57, #005A9C); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; transition: all 0.3s ease;">
                        🔬
                    </div>
                    <h4 style="color: #2E8B57; margin: 0; font-size: 1.3rem; font-weight: 600;">{T('system_soil_intelligence')}</h4>
                </div>
                <p style="font-size: 1rem; color: rgba(255,255,255,0.85); line-height: 1.7; margin: 0;">
                    {T('system_soil_intelligence_desc')}
                </p>
            </div>
            <div class="system-card" style="background: rgba(255,255,255,0.08); padding: 2.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div class="icon-bg" style="width: 48px; height: 48px; background: linear-gradient(135deg, #2E8B57, #005A9C); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; transition: all 0.3s ease;">
                        📊
                    </div>
                    <h4 style="color: #2E8B57; margin: 0; font-size: 1.3rem; font-weight: 600;">{T('system_smart_recommendations')}</h4>
                </div>
                <p style="font-size: 1rem; color: rgba(255,255,255,0.85); line-height: 1.7; margin: 0;">
                    {T('system_smart_recommendations_desc')}
                </p>
            </div>
            <div class="system-card" style="background: rgba(255,255,255,0.08); padding: 2.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div class="icon-bg" style="width: 48px; height: 48px; background: linear-gradient(135deg, #2E8B57, #005A9C); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; transition: all 0.3s ease;">
                        💰
                    </div>
                    <h4 style="color: #2E8B57; margin: 0; font-size: 1.3rem; font-weight: 600;">{T('system_cost_analysis')}</h4>
                </div>
                <p style="font-size: 1rem; color: rgba(255,255,255,0.85); line-height: 1.7; margin: 0;">
                    {T('system_cost_analysis_desc')}
                </p>
            </div>
            <div class="system-card" style="background: rgba(255,255,255,0.08); padding: 2.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.12); transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div class="icon-bg" style="width: 48px; height: 48px; background: linear-gradient(135deg, #2E8B57, #005A9C); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; transition: all 0.3s ease;">
                        📄
                    </div>
                    <h4 style="color: #2E8B57; margin: 0; font-size: 1.3rem; font-weight: 600;">{T('system_professional_reports')}</h4>
                </div>
                <p style="font-size: 1rem; color: rgba(255,255,255,0.85); line-height: 1.7; margin: 0;">
                    {T('system_professional_reports_desc')}
                </p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# How It Works Section (3-Step Process)
st.markdown(f"""
<div class="section">
    <h2 style="text-align: center; margin-bottom: 3rem;">{T('process_title')}</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-number">1</div>
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 10C21 17 12 23 12 23S3 17 3 10C3 7.61305 3.94821 5.32387 5.63604 3.63604C7.32387 1.94821 9.61305 1 12 1C14.3869 1 16.6761 1.94821 18.364 3.63604C20.0518 5.32387 21 7.61305 21 10Z" stroke="white" stroke-width="1.5" stroke-opacity="0.8"/>
                <circle cx="12" cy="10" r="3" stroke="white" stroke-width="1.5" stroke-opacity="0.8"/>
            </svg>
        </div>
        <h4 style="color: white; font-size: 1.25rem; margin: 0.5rem 0;">{T('step1_title')}</h4>
        <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
            {T('step1_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-number">2</div>
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 11L12 14L22 4" stroke="white" stroke-width="1.5" stroke-opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 12V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H16" stroke="white" stroke-width="1.5" stroke-opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h4 style="color: white; font-size: 1.25rem; margin: 0.5rem 0;">{T('step2_title')}</h4>
        <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
            {T('step2_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-number">3</div>
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" stroke="white" stroke-width="1.5" stroke-opacity="0.8"/>
                <path d="M14 2V8H20" stroke="white" stroke-width="1.5" stroke-opacity="0.8"/>
                <path d="M16 13H8" stroke="white" stroke-width="1.5" stroke-opacity="0.8"/>
                <path d="M16 17H8" stroke="white" stroke-width="1.5" stroke-opacity="0.8"/>
            </svg>
        </div>
        <h4 style="color: white; font-size: 1.25rem; margin: 0.5rem 0;">{T('step3_title')}</h4>
        <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
            {T('step3_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)

# Features Section
st.markdown(f"""
<div class="section">
    <h2 style="text-align: center; margin-bottom: 4rem;">{T('features_title')}</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown(f"""
    <div class="feature-card">
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="3" width="18" height="18" rx="2" stroke="#2E8B57" stroke-width="1.5"/>
                <path d="M3 9H21" stroke="#2E8B57" stroke-width="1.5"/>
                <path d="M9 3V21" stroke="#2E8B57" stroke-width="1.5"/>
                <path d="M7 15L12 10L14 12L17 9" stroke="#2E8B57" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h3>{T('feature_precise_mapping')}</h3>
        <p>
            {T('feature_precise_mapping_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="feature-card">
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C17.523 2 22 6.477 22 12C22 17.523 17.523 22 12 22C6.477 22 2 17.523 2 12C2 6.477 6.477 2 12 2Z" stroke="#005A9C" stroke-width="1.5"/>
                <path d="M12 6V12L16 14" stroke="#005A9C" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <h3>{T('feature_api_driven')}</h3>
        <p>
            {T('feature_api_driven_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="feature-card">
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10.29 3.86L1.82 18C1.64539 18.3024 1.55296 18.6453 1.55199 18.9945C1.55102 19.3437 1.64153 19.6871 1.81442 19.9905C1.98731 20.2939 2.23674 20.5467 2.53771 20.7239C2.83868 20.901 3.1808 20.9962 3.53 21H20.47C20.8192 20.9962 21.1613 20.901 21.4623 20.7239C21.7633 20.5467 22.0127 20.2939 22.1856 19.9905C22.3585 19.6871 22.449 19.3437 22.448 18.9945C22.447 18.6453 22.3546 18.3024 22.18 18L13.71 3.86C13.5318 3.56611 13.2807 3.32313 12.9812 3.15449C12.6817 2.98585 12.3438 2.89726 12 2.89726C11.6562 2.89726 11.3183 2.98585 11.0188 3.15449C10.7193 3.32313 10.4682 3.56611 10.29 3.86Z" stroke="#2E8B57" stroke-width="1.5"/>
                <path d="M12 9V13" stroke="#2E8B57" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="12" cy="17" r="1" fill="#2E8B57"/>
            </svg>
        </div>
        <h3>{T('feature_automated_design')}</h3>
        <p>
            {T('feature_automated_design_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="feature-card">
        <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="7" width="20" height="14" rx="2" stroke="#005A9C" stroke-width="1.5"/>
                <path d="M16 7V5C16 3.89543 15.1046 3 14 3H10C8.89543 3 8 3.89543 8 5V7" stroke="#005A9C" stroke-width="1.5"/>
                <path d="M12 11V17" stroke="#005A9C" stroke-width="1.5"/>
                <path d="M9 14H15" stroke="#005A9C" stroke-width="1.5"/>
            </svg>
        </div>
        <h3>{T('feature_financial_analysis')}</h3>
        <p>
            {T('feature_financial_analysis_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)

# Credibility Section
st.markdown(f"""
<div class="section">
    <h2 style="text-align: center; margin-bottom: 3rem;">{T('credibility_title')}</h2>
    <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 2rem; border: 1px solid rgba(255,255,255,0.1);">
        <p style="text-align: center; font-size: 1.125rem; margin-bottom: 2rem; color: rgba(255,255,255,0.9);">
            {T('credibility_desc')}
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="font-weight: 700; color: #2E8B57; margin-bottom: 0.5rem;">{T('credibility_isric')}</div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">{T('credibility_isric_desc')}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-weight: 700; color: #2E8B57; margin-bottom: 0.5rem;">{T('credibility_openmeteo')}</div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">{T('credibility_openmeteo_desc')}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-weight: 700; color: #2E8B57; margin-bottom: 0.5rem;">{T('credibility_satellite')}</div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">{T('credibility_satellite_desc')}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



# Final CTA
st.markdown(f"""
<div class="section" style="text-align: center; margin-top: 4rem;">
    <h2 style="margin-bottom: 1.5rem;">{T('cta_title')}</h2>
    <p style="font-size: 1.25rem; color: rgba(255,255,255,0.9); margin-bottom: 2rem;">
        {T('cta_description')}
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button(T('cta_button'), key="final_cta", use_container_width=True):
        st.switch_page("pages/calc.py")

# Simple Footer
st.markdown(f"""
<div class="footer">
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💧</div>
        <h3 style="font-size: 1.25rem; margin-bottom: 1rem;">{T('app_name')}</h3>
        <p style="font-size: 0.875rem; color: rgba(255,255,255,0.6); margin-bottom: 1rem;">
            {T('footer_project')}
        </p>
        <p style="font-size: 0.875rem; color: rgba(255,255,255,0.7);">
            {T('footer_team')}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1.5rem; margin-top: 2rem; text-align: center;">
    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">
        {T('footer_copyright')}
    </p>
    <p style="font-size: 0.75rem; color: rgba(255,255,255,0.4); margin-top: 0.5rem;">
        Data Sources: ISRIC SoilGrids API | Open-Meteo API | Folium Maps
    </p>
</div>
""", unsafe_allow_html=True)

# End of Hydro-Assess Landing Page
