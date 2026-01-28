"""
Main page layout and orchestration.

Assembles all components into the final application interface.
"""

import streamlit as st
import time
import config
from src.core.hasher import FileHasher
from src.core.file_handler import FileProcessor
from src.utils.formatters import format_file_size, pluralize
from src.utils.exporters import HashExporter, HashResultFormatter
from src.ui.components import (
    AlgorithmSelector,
    FileUploadComponent,
    HashResultsTable,
    DetailedHashView,
    SessionInfoPanel
)
from src.ui.theme import ThemeManager


def initialize_session_state():
    """Initialize session state variables."""
    if config.SESSION_KEYS['HISTORY'] not in st.session_state:
        st.session_state[config.SESSION_KEYS['HISTORY']] = []


def render_header(theme_manager: ThemeManager):
    """Render page header with theme toggle."""
    col_title, col_theme = st.columns([6, 1])
    
    with col_title:
        st.title(f"{config.APP_ICON} {config.APP_TITLE}")
        st.markdown(config.APP_DESCRIPTION)
    
    with col_theme:
        theme_manager.render_theme_toggle()


def render_sidebar(theme_manager: ThemeManager):
    """Render sidebar with settings."""
    with st.sidebar:
        # Algorithm selection
        selected_algorithms = AlgorithmSelector.render()
        num_selected = len(selected_algorithms)
        AlgorithmSelector.show_validation(num_selected)
        
        st.divider()
        
        # Session info
        history = st.session_state[config.SESSION_KEYS['HISTORY']]
        SessionInfoPanel.render(len(history), theme_manager.is_dark_mode)
        
        return selected_algorithms, num_selected


def render_file_upload():
    """Render file upload section."""
    st.divider()
    uploaded_files = FileUploadComponent.render()
    
    if not uploaded_files:
        return None, [], []
    
    # Validate file count
    if len(uploaded_files) > config.MAX_FILES_ALLOWED:
        st.error(f"❌ Too many files! Maximum {config.MAX_FILES_ALLOWED} files allowed.")
        uploaded_files = uploaded_files[:config.MAX_FILES_ALLOWED]
        st.warning(f"⚠️ Only processing the first {config.MAX_FILES_ALLOWED} files")
    
    # Process files
    valid_files, invalid_files = FileProcessor.process_uploaded_files(uploaded_files)
    
    # Show previews
    FileUploadComponent.show_file_previews(valid_files, invalid_files)
    
    return uploaded_files, valid_files, invalid_files


def render_action_buttons(can_generate: bool):
    """Render action buttons."""
    st.divider()
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        generate_button = st.button(
            "🚀 Generate Hashes",
            type="primary",
            disabled=not can_generate,
            use_container_width=True
        )
    
    with col2:
        history = st.session_state[config.SESSION_KEYS['HISTORY']]
        clear_button = st.button(
            "🗑️ Clear History",
            use_container_width=True,
            disabled=len(history) == 0
        )
    
    return generate_button, clear_button


def process_files(valid_files, selected_algorithms):
    """Process files and calculate hashes."""
    st.subheader("⏳ Processing Files...")
    hasher = FileHasher()
    
    for file_info in valid_files:
        with st.container():
            st.write(f"**{file_info.name}** ({format_file_size(file_info.size)})")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Define progress callback
            def update_progress(bytes_processed, total_bytes):
                progress = bytes_processed / total_bytes
                progress_bar.progress(progress)
                status_text.text(
                    f"Hashing {file_info.name}: {format_file_size(bytes_processed)} / {format_file_size(total_bytes)}"
                )
            
            # Calculate hashes
            start_time = time.time()
            hashes = hasher.calculate_hashes(
                file_info.data,
                selected_algorithms,
                progress_callback=update_progress
            )
            elapsed_time = time.time() - start_time
            
            #Calculate combined hash if multiple algorithms selected
            combined_hash = None
            if len(selected_algorithms) > 1:
                combined_hash = hasher.calculate_combined_hash(hashes)

            # Clear progress indicators
            progress_bar.empty()
            status_text.success(f"✅ Completed in {elapsed_time:.2f}s")
            
            # Add to history
            entry = HashResultFormatter.create_history_entry(
                file_name=file_info.name,
                file_size=file_info.size,
                file_size_formatted=format_file_size(file_info.size),
                hashes=hashes,
                combined_hash=combined_hash
            )
            st.session_state[config.SESSION_KEYS['HISTORY']].append(entry)
    
    st.success("🎉 All files processed successfully!")
    time.sleep(0.5)


def render_results(theme_manager: ThemeManager):
    """Render hash results section."""
    history = st.session_state[config.SESSION_KEYS['HISTORY']]
    
    if not history:
        st.info("👆 Upload files and click 'Generate Hashes' to see results here")
        return
    
    st.divider()
    st.subheader("{Hash Results}")
    
    # Prepare and display table
    df = HashResultFormatter.format_for_table(history)
    
    if theme_manager.is_dark_mode:
        HashResultsTable.render_dark_mode_table(df)
    else:
        HashResultsTable.render_light_mode_table(df)
    
    # Export options
    render_export_buttons(history)
    
    # Detailed view
    st.divider()
    DetailedHashView.render(history, theme_manager.is_dark_mode)


def render_export_buttons(history):
    """Render export buttons."""
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        text_export = HashExporter.to_text(history)
        if text_export:
            st.download_button(
                label="📋 Copy All (Text)",
                data=text_export,
                file_name=HashExporter.get_export_filename('txt'),
                mime="text/plain",
                use_container_width=True
            )
    
    with col2:
        csv_export = HashExporter.to_csv(history)
        if csv_export:
            st.download_button(
                label="💾 Download CSV",
                data=csv_export,
                file_name=HashExporter.get_export_filename('csv'),
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        st.info("💡 Click any cell to copy hash")


def render_footer(theme_manager: ThemeManager):
    """Render page footer."""
    st.divider()
    footer_col1, footer_col2 = st.columns([3, 1])
    
    with footer_col1:
        max_size = config.get_max_file_size_display()
        st.caption(
            f"Built with Streamlit | Session-based history | "
            f"Supports up to {config.MAX_FILES_ALLOWED} files, {max_size} each"
        )
    
    with footer_col2:
        mode_text = '🌙 Dark Mode' if theme_manager.is_dark_mode else '☀️ Light Mode'
        st.caption(mode_text)


def render_main_page():
    """Main page rendering function."""
    # Initialize
    initialize_session_state()
    theme_manager = ThemeManager()
    theme_manager.apply_theme()
    
    # Header
    render_header(theme_manager)
    
    # Sidebar
    selected_algorithms, num_selected = render_sidebar(theme_manager)
    
    # File upload
    uploaded_files, valid_files, invalid_files = render_file_upload()
    
    # Determine if can generate
    can_generate = (
        uploaded_files is not None and
        len(valid_files) > 0 and
        config.MIN_ALGORITHMS <= num_selected <= config.MAX_ALGORITHMS
    )
    
    # Action buttons
    generate_button, clear_button = render_action_buttons(can_generate)
    
    # Handle clear history
    if clear_button:
        st.session_state[config.SESSION_KEYS['HISTORY']] = []
        st.rerun()
    
    # Handle hash generation
    if generate_button and valid_files:
        process_files(valid_files, selected_algorithms)
        st.rerun()
    
    # Display results
    render_results(theme_manager)
    
    # Footer
    render_footer(theme_manager)