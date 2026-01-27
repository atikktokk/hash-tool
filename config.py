"""
Configuration settings for the File Hashing Tool.

All application settings are centralized here for easy modification.
"""

import hashlib

# Application metadata
APP_TITLE = "File Hashing Tool"
APP_ICON = ""
APP_DESCRIPTION = "Upload multiple files and generate hash values for verification and integrity checking."

# File upload constraints
MAX_FILE_SIZE_BYTES = 1073741824  # 1GB in bytes
MAX_FILES_ALLOWED = 5
MIN_FILES_REQUIRED = 1

# Hash calculation settings
CHUNK_SIZE = 8192  # 8KB chunks for reading files

# Algorithm selection constraints
MIN_ALGORITHMS = 1
MAX_ALGORITHMS = 3

# Available hash algorithms
HASH_ALGORITHMS = {
    'MD5': hashlib.md5,
    'SHA-1': hashlib.sha1,
    'SHA-224': hashlib.sha224,
    'SHA-256': hashlib.sha256,
    'SHA-384': hashlib.sha384,
    'SHA-512': hashlib.sha512,
    'SHA3-256': hashlib.sha3_256,
    'SHA3-512': hashlib.sha3_512,
    'BLAKE2b': hashlib.blake2b,
    'BLAKE2s': hashlib.blake2s,
}

# Default selected algorithm
DEFAULT_ALGORITHM = 'SHA-256'

# UI settings
SIDEBAR_STATE = "expanded"
LAYOUT_MODE = "wide"

# Export settings
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
EXPORT_FILENAME_FORMAT = 'hash_results_{timestamp}'

# Theme colors (for reference in CSS)
DARK_MODE_COLORS = {
    'background': '#0e1117',
    'secondary_bg': '#1a1d29',
    'tertiary_bg': '#262c3d',
    'text': '#ffffff',
    'accent': '#00d4ff',
    'accent_hover': '#00a8cc',
}

LIGHT_MODE_COLORS = {
    'background': '#ffffff',
    'secondary_bg': '#f0f2f6',
    'text': '#31333f',
    'accent': '#1f77b4',
}

# Session state keys
SESSION_KEYS = {
    'HISTORY': 'hash_history',
    'DARK_MODE': 'dark_mode',
}

# Helper functions for common conversions
def get_max_file_size_display():
    """Return human-readable max file size."""
    return f"{MAX_FILE_SIZE_BYTES / (1024**3):.0f}GB"

def get_file_size_in_mb(size_bytes):
    """Convert bytes to MB."""
    return size_bytes / (1024**2)

def get_file_size_in_gb(size_bytes):
    """Convert bytes to GB."""
    return size_bytes / (1024**3)