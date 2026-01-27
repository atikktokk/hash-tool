"""
Reusable UI components.

Contains functions that render specific UI elements.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict
import config
from src.utils.formatters import format_file_size, pluralize


class AlgorithmSelector:
    """Component for selecting hash algorithms."""
    
    @staticmethod
    def render() -> Dict:
        """
        Render algorithm selection checkboxes.
        
        Returns:
            Dictionary mapping selected algorithm names to their constructors
        """
        st.header("⚙️ Hash Settings")
        st.subheader("Select Hash Algorithms")
        st.caption(f"Choose {config.MIN_ALGORITHMS}-{config.MAX_ALGORITHMS} algorithms for comparison")
        
        selected_algorithms = {}
        for algo_name in config.HASH_ALGORITHMS.keys():
            is_default = (algo_name == config.DEFAULT_ALGORITHM)
            if st.checkbox(algo_name, value=is_default):
                selected_algorithms[algo_name] = config.HASH_ALGORITHMS[algo_name]
        
        return selected_algorithms
    
    @staticmethod
    def show_validation(num_selected: int):
        """Show validation message for algorithm selection."""
        if num_selected < config.MIN_ALGORITHMS:
            st.warning(f"⚠️ Please select at least {config.MIN_ALGORITHMS} algorithm")
        elif num_selected > config.MAX_ALGORITHMS:
            st.error(f"❌ Please select maximum {config.MAX_ALGORITHMS} algorithms")
        else:
            st.success(f"✅ {pluralize(num_selected, 'algorithm')} selected")


class FileUploadComponent:
    """Component for file upload interface."""
    
    @staticmethod
    def render():
        """
        Render file upload widget.
        
        Returns:
            List of uploaded files or None
        """
        st.subheader("Upload Files")
        max_size = config.get_max_file_size_display()
        
        uploaded_files = st.file_uploader(
            f"Choose up to {config.MAX_FILES_ALLOWED} files (Max {max_size} each)",
            type=None,
            accept_multiple_files=True,
            help=f"Upload {config.MIN_FILES_REQUIRED}-{config.MAX_FILES_ALLOWED} files to hash and compare"
        )
        
        return uploaded_files
    
    @staticmethod
    def show_file_previews(valid_files: List, invalid_files: List):
        """Display preview of uploaded files."""
        total_files = len(valid_files) + len(invalid_files)
        
        if total_files > 0:
            st.info(f"📋 {pluralize(total_files, 'file')} uploaded")
            
            # Display file details in columns
            all_files = valid_files + invalid_files
            cols = st.columns(min(len(all_files), 3))
            
            for idx, file_info in enumerate(all_files):
                with cols[idx % 3]:
                    if file_info.is_valid:
                        st.success(f"✅ {file_info.name}")
                        st.caption(f"Size: {format_file_size(file_info.size)}")
                    else:
                        st.error(f"❌ {file_info.name}")
                        st.caption(file_info.error_message)


class HashResultsTable:
    """Component for displaying hash results in table format."""
    
    @staticmethod
    def render_dark_mode_table(df: pd.DataFrame):
        """Render custom HTML table for dark mode."""
        html_table = '<div style="overflow-x: auto; background-color: #1a1d29; padding: 10px; border-radius: 5px;">'
        html_table += '<table style="width: 100%; border-collapse: collapse; color: #ffffff;">'
        
        # Headers
        html_table += '<thead><tr style="background-color: #0e1117; border-bottom: 2px solid #00d4ff;">'
        for col in df.columns:
            html_table += f'<th style="padding: 12px; text-align: left; color: #00d4ff; font-weight: bold;">{col}</th>'
        html_table += '</tr></thead>'
        
        # Body
        html_table += '<tbody>'
        for idx, row in df.iterrows():
            bg_color = '#262c3d' if idx % 2 == 0 else '#1a1d29'
            html_table += f'<tr style="background-color: {bg_color}; border-bottom: 1px solid #333;">'
            for col in df.columns:
                value = str(row[col])
                # Truncate long hash values for display
                if len(value) > 50:
                    display_value = value[:47] + '...'
                    html_table += f'<td style="padding: 10px; color: #ffffff; font-family: monospace; cursor: pointer;" title="{value}" onclick="navigator.clipboard.writeText(\'{value}\')">{display_value}</td>'
                else:
                    html_table += f'<td style="padding: 10px; color: #ffffff;">{value}</td>'
            html_table += '</tr>'
        html_table += '</tbody></table></div>'
        
        st.markdown(html_table, unsafe_allow_html=True)
        st.caption("💡 Click any hash cell to copy to clipboard")
    
    @staticmethod
    def render_light_mode_table(df: pd.DataFrame):
        """Render standard Streamlit dataframe for light mode."""
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "File Name": st.column_config.TextColumn("File Name", width="medium"),
                "Size": st.column_config.TextColumn("Size", width="small"),
                "Time": st.column_config.TextColumn("Time", width="medium"),
            }
        )


class DetailedHashView:
    """Component for detailed hash view with expandable sections."""
    
    @staticmethod
    def render(history: List[Dict], is_dark_mode: bool):
        """Render detailed view of hash results."""
        st.subheader("🔍 Detailed View")
        
        for idx, entry in enumerate(history, 1):
            with st.expander(
                f"File #{idx}: {entry['file_name']} ({entry['file_size_formatted']})",
                expanded=False
            ):
                st.caption(f"Processed at: {entry['timestamp']}")
                
                for algo_name, hash_value in entry['hashes'].items():
                    col_a, col_b = st.columns([1, 5])
                    with col_a:
                        st.write(f"**{algo_name}**")
                    with col_b:
                        if is_dark_mode:
                            # Use custom styled div for dark mode
                            st.markdown(f"""
                            <div style="background-color: #1a1d29; padding: 10px; border-radius: 5px; 
                                 border: 1px solid #00d4ff; font-family: monospace; color: #00d4ff; 
                                 cursor: pointer; word-break: break-all;" 
                                 onclick="navigator.clipboard.writeText('{hash_value}')" 
                                 title="Click to copy">
                                {hash_value}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.code(hash_value, language=None)


class SessionInfoPanel:
    """Component for displaying session information."""
    
    @staticmethod
    def render(files_hashed: int, is_dark_mode: bool):
        """Render session info panel in sidebar."""
        st.subheader("📊 Session Info")
        st.metric("Files Hashed", files_hashed)
        st.metric("Theme", "Dark Mode 🌙" if is_dark_mode else "Light Mode ☀️")
        st.caption("History clears on browser refresh")