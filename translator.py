"""
Translation utility functions for Hydro-Assess application
Provides language selection and translation helpers
"""

import streamlit as st
from locales import translations


def T(key: str) -> str:
    """
    Translation function that retrieves the correct translated string
    based on the current language setting in session state.
    
    Args:
        key: The translation key to look up
        
    Returns:
        The translated string in the current language, or the English version
        if the translation is not found, or the key itself if not found at all
    """
    # Get current language from session state, default to English
    # Handle case where session state might not be initialized yet
    try:
        current_lang = st.session_state.get('language', 'en')
    except:
        current_lang = 'en'
    
    # Try to get the translation for the current language
    if current_lang in translations and key in translations[current_lang]:
        return translations[current_lang][key]
    
    # Fallback to English if translation not found in current language
    if key in translations['en']:
        return translations['en'][key]
    
    # If key not found at all, return the key itself (for debugging)
    return key


def language_selector():
    """
    Creates a language selector widget in the Streamlit sidebar.
    When a new language is selected, it updates the session state
    and triggers a rerun of the app to apply the new language.
    """
    # Language options with flags
    languages = {
        'en': '🇬🇧 English',
        'hi': '🇮🇳 हिन्दी (Hindi)',
        'ta': '🇹🇳 தமிழ் (Tamil)'
    }
    
    # Initialize language in session state if not present
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Create the selectbox in the sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🌐 Language / भाषा")
        
        # Get the current language
        current_lang = st.session_state.language
        current_index = list(languages.keys()).index(current_lang)
        
        # Create selectbox
        selected_lang = st.selectbox(
            "Select Language / भाषा चुनें",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            index=current_index,
            key='language_selector_widget',
            help="Choose your preferred language / अपनी पसंदीदा भाषा चुनें"
        )
        
        # Update session state and rerun if language changed
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
        
        st.markdown("---")


def get_current_language() -> str:
    """
    Returns the current language code.
    
    Returns:
        The current language code ('en' or 'hi')
    """
    return st.session_state.get('language', 'en')


def is_hindi() -> bool:
    """
    Check if the current language is Hindi.
    
    Returns:
        True if current language is Hindi, False otherwise
    """
    return get_current_language() == 'hi'


def is_english() -> bool:
    """
    Check if the current language is English.
    
    Returns:
        True if current language is English, False otherwise
    """
    return get_current_language() == 'en'


def is_tamil() -> bool:
    """
    Check if the current language is Tamil.
    
    Returns:
        True if current language is Tamil, False otherwise
    """
    return get_current_language() == 'ta'


def main_page_language_selector():
    """
    Creates a language selector widget for the main page (not sidebar).
    Returns a container with the language selector styled appropriately.
    """
    import streamlit as st
    
    # Language options with flags
    languages = {
        'en': '🇬🇧 English',
        'hi': '🇮🇳 हिन्दी (Hindi)',
        'ta': '🇹🇳 தமிழ் (Tamil)'
    }
    
    # Initialize language in session state if not present
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Get the current language
    current_lang = st.session_state.language
    current_index = list(languages.keys()).index(current_lang)
    
    # Create a container for the language selector
    col1, col2, col3 = st.columns([1, 1, 8])
    with col2:
        selected_lang = st.selectbox(
            "🌐 Language / भाषा / மொழி",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            index=current_index,
            key='main_language_selector',
            help="Choose your preferred language / अपनी पसंदीदा भाषा चुनें / உங்கள் விருப்ப மொழியைத் தேர்ந்தெடுக்கவும்"
        )
        
        # Update session state and rerun if language changed
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
