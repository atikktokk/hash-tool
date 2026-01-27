"""
Theme management for dark/light mode.

Handles theme switching and CSS injection.
"""

import streamlit as st
import config


class ThemeManager:
    """Manages application theming and mode switching."""
    
    def __init__(self):
        """Initialize theme manager and session state."""
        if config.SESSION_KEYS['DARK_MODE'] not in st.session_state:
            st.session_state[config.SESSION_KEYS['DARK_MODE']] = False
    
    @property
    def is_dark_mode(self) -> bool:
        """Check if dark mode is currently enabled."""
        return st.session_state[config.SESSION_KEYS['DARK_MODE']]
    
    def toggle_theme(self):
        """Toggle between dark and light mode."""
        st.session_state[config.SESSION_KEYS['DARK_MODE']] = not self.is_dark_mode
    
    def apply_theme(self):
        """Apply the current theme's CSS."""
        if self.is_dark_mode:
            self._apply_dark_theme()
        else:
            self._apply_light_theme()
    
    def _apply_dark_theme(self):
        """Apply dark mode CSS styling."""
        st.markdown("""
        <style>
            /* Main background */
            .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }
            
            /* Force all text to be readable */
            .stApp * {
                color: #ffffff;
            }
            
            .stApp p, .stApp span, .stApp div:not([class*="stButton"]) {
                color: #e8e8e8 !important;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #1a1d29;
            }
            
            [data-testid="stSidebar"] * {
                color: #fafafa !important;
            }
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #fafafa !important;
            }
            
            /* All text elements */
            p, span, div, label, small {
                color: #e8e8e8 !important;
            }
            
            /* Strong/bold text */
            strong, b {
                color: #ffffff !important;
            }
            
            /* Input labels and descriptions */
            label[data-testid="stWidgetLabel"],
            .stMarkdown p {
                color: #ffffff !important;
            }
            
            /* Checkboxes and labels */
            [data-testid="stCheckbox"] label {
                color: #ffffff !important;
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                color: #00d4ff !important;
            }
            
            /* File uploader */
            [data-testid="stFileUploader"] {
                background-color: #1a1d29;
                border: 2px dashed #00d4ff;
                border-radius: 10px;
                padding: 20px;
            }
            
            [data-testid="stFileUploader"] label,
            [data-testid="stFileUploader"] p,
            [data-testid="stFileUploader"] span,
            [data-testid="stFileUploader"] div,
            [data-testid="stFileUploader"] small {
                color: #ffffff !important;
            }
            
            [data-testid="stFileUploader"] section {
                background-color: #2a2f3f !important;
                border: 2px dashed #00d4ff !important;
            }
            
            [data-testid="stFileUploader"] section * {
                color: #ffffff !important;
            }
            
            .uploadedFileName {
                color: #ffffff !important;
            }
            
            [data-testid="stFileUploader"] li,
            [data-testid="stFileUploader"] li * {
                color: #ffffff !important;
                background-color: #2a2f3f !important;
            }
            
            [data-testid="stFileUploader"] button {
                background-color: #00d4ff !important;
                color: #0e1117 !important;
                border: none !important;
            }
            
            /* Buttons */
            .stButton > button {
                background-color: #00d4ff !important;
                color: #0e1117 !important;
                font-weight: bold;
                border: none;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                background-color: #00a8cc !important;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
            }
            
            .stDownloadButton > button {
                background-color: #00d4ff !important;
                color: #0e1117 !important;
            }
            
            /* Code blocks */
            .stCodeBlock {
                background-color: #1a1d29 !important;
                border: 1px solid #00d4ff;
            }
            
            code {
                background-color: #1a1d29 !important;
                color: #00d4ff !important;
                padding: 10px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
            
            pre {
                background-color: #1a1d29 !important;
                color: #00d4ff !important;
            }
            
            [data-testid="stCodeBlock"] code {
                color: #00d4ff !important;
            }
            
            /* Success/Error/Warning boxes */
            .stSuccess {
                background-color: rgba(0, 212, 255, 0.15);
                border-left: 4px solid #00d4ff;
                color: #ffffff !important;
            }
            
            .stSuccess * {
                color: #ffffff !important;
            }
            
            .stError {
                background-color: rgba(255, 75, 75, 0.15);
                border-left: 4px solid #ff4b4b;
                color: #ffffff !important;
            }
            
            .stError * {
                color: #ffffff !important;
            }
            
            .stWarning {
                background-color: rgba(255, 196, 0, 0.15);
                border-left: 4px solid #ffc400;
                color: #ffffff !important;
            }
            
            .stWarning * {
                color: #ffffff !important;
            }
            
            .stInfo {
                background-color: rgba(0, 212, 255, 0.15);
                border-left: 4px solid #00d4ff;
                color: #ffffff !important;
            }
            
            .stInfo * {
                color: #ffffff !important;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #262c3d;
                color: #ffffff !important;
            }
            
            [data-testid="stExpander"] p,
            [data-testid="stExpander"] span {
                color: #ffffff !important;
            }
            
            .caption, [data-testid="stCaptionContainer"] {
                color: #a0a0a0 !important;
            }
            
            /* Divider */
            hr {
                border-color: #00d4ff;
                opacity: 0.3;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def _apply_light_theme(self):
        """Apply light mode CSS styling."""
        st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
                color: #31333f;
            }
            
            [data-testid="stSidebar"] {
                background-color: #f0f2f6;
            }
            
            [data-testid="stFileUploader"] {
                background-color: #f8f9fa;
                border: 2px dashed #1f77b4;
                border-radius: 10px;
                padding: 20px;
            }
            
            .stButton > button {
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(31, 119, 180, 0.3);
            }
            
            hr {
                border-color: #1f77b4;
                opacity: 0.3;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def render_theme_toggle(self):
        """Render the theme toggle button."""
        theme_icon = "🌙" if not self.is_dark_mode else "☀️"
        theme_label = "Dark" if not self.is_dark_mode else "Light"
        
        if st.button(f"{theme_icon} {theme_label}", key="theme_toggle", use_container_width=True):
            self.toggle_theme()
            st.rerun()