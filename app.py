"""
File Hashing Tool - Main Application Entry Point

A professional web application for calculating and comparing file hashes.
Supports multiple hash algorithms with progress tracking and export capabilities.

Author: 
Version: 2.0 (Refactored)
"""

import streamlit as st
import config
from src.ui.layout import render_main_page

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.LAYOUT_MODE,
    initial_sidebar_state=config.SIDEBAR_STATE
)


def main():
    """Main application entry point."""
    render_main_page()


if __name__ == "__main__":
    main()