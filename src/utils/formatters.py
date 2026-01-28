"""
Formatting utilities for displaying data to users.

Handles conversion of bytes, timestamps, and other display formatting.
"""

import time
from typing import Union


def format_file_size(size_bytes: Union[int, float]) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB", "234 KB")
        
    Example:
        >>> format_file_size(1536)
        '1.50 KB'
        >>> format_file_size(1048576)
        '1.00 MB'
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def format_timestamp(format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Get current timestamp as formatted string.
    
    Args:
        format_str: strftime format string
        
    Returns:
        Formatted timestamp string
        
    Example:
        >>> format_timestamp()
        '2026-01-25 10:30:45'
    """
    return time.strftime(format_str)


def format_hash_display(hash_value: str, max_length: int = 50) -> str:
    """
    Truncate long hash values for display.
    
    Args:
        hash_value: Full hash string
        max_length: Maximum length before truncation
        
    Returns:
        Truncated hash with ellipsis if needed
        
    Example:
        >>> format_hash_display('a' * 100, 50)
        'aaaaaaaaaa...aaaaaaaaaa (100 chars)'
    """
    if len(hash_value) <= max_length:
        return hash_value
    
    # Show first and last parts
    show_chars = (max_length - 3) // 2
    return f"{hash_value[:show_chars]}...{hash_value[-show_chars:]}"


def format_algorithm_name(algo_name: str) -> str:
    """
    Format algorithm name for display.
    
    Args:
        algo_name: Algorithm name (e.g., 'SHA-256')
        
    Returns:
        Formatted name with proper styling
    """
    return algo_name.upper()


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
        
    Example:
        >>> format_duration(65.5)
        '1m 5.5s'
        >>> format_duration(3.2)
        '3.2s'
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes}m {remaining_seconds:.1f}s"


def pluralize(count: int, singular: str, plural: str = None) -> str:
    """
    Return singular or plural form based on count.
    
    Args:
        count: Number of items
        singular: Singular form
        plural: Plural form (defaults to singular + 's')
        
    Returns:
        Appropriate form with count
        
    Example:
        >>> pluralize(1, 'file')
        '1 file'
        >>> pluralize(5, 'file')
        '5 files'
    """
    if plural is None:
        plural = singular + 's'
    
    form = singular if count == 1 else plural
    return f"{count} {form}"

def format_combined_hash_label(num_algorithms: int) -> str:
    """
    Format label for combined hash.
    
    Args:
        num_algorithms: Number of algorithms combined
        
    Returns:
        Formatted label string
        
    Example:
        >>> format_combined_hash_label(3)
        'Combined (3 algorithms)'
    """
    return f"Combined ({num_algorithms} algorithms)"