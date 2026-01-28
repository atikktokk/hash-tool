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
            
            # Add combined hash if available
            if entry.get('combined_hash'):
                row['Combined Hash'] = entry['combined_hash']
            
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
            
            # add combined hash if available
            if entry.get('combined_hash'):
                output.append("-" * 80)
                output.append(f"{'COMBINED':12} : {entry['combined_hash']}")
                output.append(f"Note: Combined hash is SHA-256 of all individual hashes concatenated")

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
    combined_hash: str = None,
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
        'combined_hash': combined_hash,
        'timestamp': timestamp
        }       
    
    @staticmethod
    def format_for_table(history: List[Dict]) -> pd.DataFrame:
        """
        Format history for table display.
    
        Args:
            history: List of hash history entries
        
        Returns:
            Pandas DataFrame ready for display with Combined Hash as rightmost column
        """
        table_data = []
        for entry in history:
            # Start with fixed columns
            row = {
                'File Name': entry['file_name'],
                'Size': entry['file_size_formatted'],
                'Time': entry['timestamp']
            }
            
            # Add individual hash columns in sorted order (for consistency)
            sorted_algos = sorted(entry['hashes'].keys())
            for algo_name in sorted_algos:
                row[algo_name] = entry['hashes'][algo_name]
            
            # Add combined hash column LAST if available
            if entry.get('combined_hash'):
                row['Combined Hash'] = entry['combined_hash']
            
            table_data.append(row)
        
        # Create DataFrame with explicit column order
        df = pd.DataFrame(table_data)
        
        # Ensure Combined Hash is the last column if it exists
        if 'Combined Hash' in df.columns:
            # Get all columns except Combined Hash
            cols = [col for col in df.columns if col != 'Combined Hash']
            # Add Combined Hash at the end
            cols.append('Combined Hash')
            # Reorder DataFrame
            df = df[cols]
        
        return df