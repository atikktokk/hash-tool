"""
Export utilities for generating downloadable files.

Handles creation of CSV and text file exports.
"""

import pandas as pd
from typing import List, Dict
import config
from src.utils.formatters import format_timestamp


class HashExporter:
    """Handles exporting hash results to various formats."""
    
    @staticmethod
    def to_csv(history: List[Dict]) -> str:
        """
        Export hash history to CSV format.
        
        Args:
            history: List of hash history entries
            
        Returns:
            CSV string ready for download
        """
        if not history:
            return ""
        
        # Prepare data for CSV
        csv_data = []
        for entry in history:
            row = {
                'File Name': entry['file_name'],
                'File Size': entry['file_size_formatted'],
                'Timestamp': entry['timestamp']
            }
            # Add hash values
            for algo_name, hash_value in entry['hashes'].items():
                row[algo_name] = hash_value
            csv_data.append(row)
        
        # Convert to CSV string
        df = pd.DataFrame(csv_data)
        return df.to_csv(index=False)
    
    @staticmethod
    def to_text(history: List[Dict]) -> str:
        """
        Export hash history to formatted text.
        
        Args:
            history: List of hash history entries
            
        Returns:
            Formatted text string ready for download
        """
        if not history:
            return ""
        
        output = []
        output.append("=" * 80)
        output.append("FILE HASH RESULTS")
        output.append("=" * 80)
        output.append(f"Generated: {format_timestamp()}")
        output.append(f"Total Files: {len(history)}")
        output.append("")
        
        for idx, entry in enumerate(history, 1):
            output.append("-" * 80)
            output.append(f"File #{idx}: {entry['file_name']}")
            output.append(f"Size: {entry['file_size_formatted']}")
            output.append(f"Processed: {entry['timestamp']}")
            output.append("-" * 80)
            
            for algo_name, hash_value in entry['hashes'].items():
                output.append(f"{algo_name:12} : {hash_value}")
            
            output.append("")
        
        output.append("=" * 80)
        output.append(f"End of Report - {len(history)} file(s) processed")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    @staticmethod
    def get_export_filename(extension: str) -> str:
        """
        Generate filename for export with timestamp.
        
        Args:
            extension: File extension (e.g., 'csv', 'txt')
            
        Returns:
            Filename string
        """
        timestamp = format_timestamp('%Y%m%d_%H%M%S')
        return f"{config.EXPORT_FILENAME_FORMAT.format(timestamp=timestamp)}.{extension}"


class HashResultFormatter:
    """Formats hash results for display."""
    
    @staticmethod
    def create_history_entry(
        file_name: str,
        file_size: int,
        file_size_formatted: str,
        hashes: Dict[str, str],
        timestamp: str = None
    ) -> Dict:
        """
        Create a standardized history entry.
        
        Args:
            file_name: Name of the file
            file_size: Size in bytes
            file_size_formatted: Human-readable size
            hashes: Dictionary of algorithm:hash pairs
            timestamp: Optional timestamp (uses current time if not provided)
            
        Returns:
            Dictionary containing all entry information
        """
        if timestamp is None:
            timestamp = format_timestamp(config.TIMESTAMP_FORMAT)
        
        return {
            'file_name': file_name,
            'file_size': file_size,
            'file_size_formatted': file_size_formatted,
            'hashes': hashes,
            'timestamp': timestamp
        }
    
    @staticmethod
    def format_for_table(history: List[Dict]) -> pd.DataFrame:
        """
        Format history for table display.
        
        Args:
            history: List of hash history entries
            
        Returns:
            Pandas DataFrame ready for display
        """
        table_data = []
        for entry in history:
            row = {
                'File Name': entry['file_name'],
                'Size': entry['file_size_formatted'],
                'Time': entry['timestamp']
            }
            # Add hash columns
            for algo_name, hash_value in entry['hashes'].items():
                row[algo_name] = hash_value
            table_data.append(row)
        
        return pd.DataFrame(table_data)