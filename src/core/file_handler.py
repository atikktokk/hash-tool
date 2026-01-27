"""
File handling and validation utilities.

Handles file uploads, validation, and metadata extraction.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
import config


@dataclass
class FileInfo:
    """
    Container for file metadata.
    
    Attributes:
        name: Original filename
        size: File size in bytes
        data: Raw file bytes
        is_valid: Whether file passes validation
        error_message: Error message if validation fails
    """
    name: str
    size: int
    data: bytes
    is_valid: bool = True
    error_message: str = ""


class FileValidator:
    """Validates uploaded files against constraints."""
    
    @staticmethod
    def validate_file_size(size: int) -> Tuple[bool, str]:
        """
        Check if file size is within limits.
        
        Args:
            size: File size in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if size > config.MAX_FILE_SIZE_BYTES:
            max_size = config.get_max_file_size_display()
            return False, f"File size exceeds {max_size} limit"
        
        if size == 0:
            return False, "File is empty"
        
        return True, ""
    
    @staticmethod
    def validate_file_count(count: int) -> Tuple[bool, str]:
        """
        Check if number of files is within limits.
        
        Args:
            count: Number of files
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if count < config.MIN_FILES_REQUIRED:
            return False, f"Please upload at least {config.MIN_FILES_REQUIRED} file(s)"
        
        if count > config.MAX_FILES_ALLOWED:
            return False, f"Maximum {config.MAX_FILES_ALLOWED} files allowed"
        
        return True, ""
    
    @staticmethod
    def validate_file(name: str, size: int, data: bytes) -> FileInfo:
        """
        Validate a single file.
        
        Args:
            name: Filename
            size: File size in bytes
            data: Raw file bytes
            
        Returns:
            FileInfo object with validation results
        """
        is_valid, error_msg = FileValidator.validate_file_size(size)
        
        return FileInfo(
            name=name,
            size=size,
            data=data,
            is_valid=is_valid,
            error_message=error_msg
        )


class FileProcessor:
    """Processes uploaded files and prepares them for hashing."""
    
    @staticmethod
    def process_uploaded_files(uploaded_files: List) -> Tuple[List[FileInfo], List[FileInfo]]:
        """
        Process and validate multiple uploaded files.
        
        Args:
            uploaded_files: List of Streamlit UploadedFile objects
            
        Returns:
            Tuple of (valid_files, invalid_files)
        """
        valid_files = []
        invalid_files = []
        
        for file in uploaded_files:
            file_data = file.getvalue()
            file_info = FileValidator.validate_file(
                name=file.name,
                size=len(file_data),
                data=file_data
            )
            
            if file_info.is_valid:
                valid_files.append(file_info)
            else:
                invalid_files.append(file_info)
        
        return valid_files, invalid_files
    
    @staticmethod
    def get_total_size(files: List[FileInfo]) -> int:
        """
        Calculate total size of all files.
        
        Args:
            files: List of FileInfo objects
            
        Returns:
            Total size in bytes
        """
        return sum(f.size for f in files)