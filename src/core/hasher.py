"""
Core hashing functionality.

This module handles all hash calculation operations independently of the UI.
"""

from typing import Dict, Callable, Optional
import config


class FileHasher:
    """
    Handles file hashing operations with progress tracking.
    
    This class is UI-agnostic and can be used in different contexts
    (CLI, GUI, API, etc.)
    """
    
    def __init__(self, chunk_size: int = config.CHUNK_SIZE):
        """
        Initialize the hasher.
        
        Args:
            chunk_size: Size of chunks to read from file (in bytes)
        """
        self.chunk_size = chunk_size
    
    def calculate_hashes(
        self,
        file_data: bytes,
        algorithms: Dict[str, Callable],
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, str]:
        """
        Calculate multiple hashes for file data.
        
        Args:
            file_data: Raw file bytes to hash
            algorithms: Dictionary mapping algorithm names to hash constructors
            progress_callback: Optional callback function(bytes_processed, total_bytes)
        
        Returns:
            Dictionary mapping algorithm names to their hex digest values
            
        Example:
            >>> hasher = FileHasher()
            >>> algorithms = {'SHA-256': hashlib.sha256, 'MD5': hashlib.md5}
            >>> hashes = hasher.calculate_hashes(file_data, algorithms)
            >>> print(hashes['SHA-256'])
            'a1b2c3d4...'
        """
        results = {}
        total_size = len(file_data)
        
        # Initialize all hash objects
        hash_objects = {name: algo() for name, algo in algorithms.items()}
        
        # Process file in chunks
        bytes_processed = 0
        for i in range(0, total_size, self.chunk_size):
            chunk = file_data[i:i + self.chunk_size]
            
            # Update all hash objects with the same chunk
            for hash_obj in hash_objects.values():
                hash_obj.update(chunk)
            
            # Update progress if callback provided
            bytes_processed += len(chunk)
            if progress_callback:
                progress_callback(bytes_processed, total_size)
        
        # Get final hash values
        for name, hash_obj in hash_objects.items():
            results[name] = hash_obj.hexdigest()
        
        return results
    
    def calculate_combined_hash(
        self,
        individual_hashes: Dict[str, str],
        algorithm: str = 'SHA-256'
    ) -> str:
        """
        Calculate a combined hash from multiple individual hashes.
        
        This creates a single hash value by concatenating all individual
        hash values and hashing the result.
        
        Args:
            individual_hashes: Dictionary of algorithm names to hash values
            algorithm: Algorithm to use for the combined hash (default: SHA-256)
            
        Returns:
            Combined hash digest as hexadecimal string
            
        Example:
            >>> hashes = {'SHA-256': 'abc123', 'MD5': 'def456'}
            >>> combined = hasher.calculate_combined_hash(hashes)
            >>> print(combined)
            'xyz789...'
        """
        if len(individual_hashes) <= 1:
            # No point in combined hash with only 1 algorithm
            return None
        
        # Sort by algorithm name for consistency
        sorted_algos = sorted(individual_hashes.keys())
        
        # Concatenate all hash values in alphabetical order
        concatenated = ''.join(individual_hashes[algo] for algo in sorted_algos)
        
        # Hash the concatenated string
        if algorithm not in config.HASH_ALGORITHMS:
            algorithm = 'SHA-256'  # Fallback to SHA-256
        
        hasher = config.HASH_ALGORITHMS[algorithm]()
        hasher.update(concatenated.encode('utf-8'))
        
        return hasher.hexdigest()
    
    @staticmethod
    def verify_hash(file_data: bytes, algorithm_name: str, expected_hash: str) -> bool:
        """
        Verify a file's hash matches an expected value.
        
        Args:
            file_data: Raw file bytes
            algorithm_name: Name of hash algorithm (e.g., 'SHA-256')
            expected_hash: Expected hash value to compare against
            
        Returns:
            True if hash matches, False otherwise
        """
        if algorithm_name not in config.HASH_ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
        
        algo = config.HASH_ALGORITHMS[algorithm_name]
        hasher = algo()
        hasher.update(file_data)
        calculated_hash = hasher.hexdigest()
        
        return calculated_hash.lower() == expected_hash.lower()
    
    @staticmethod
    def get_available_algorithms() -> list:
        """
        Get list of available hash algorithms.
        
        Returns:
            List of algorithm names
        """
        return list(config.HASH_ALGORITHMS.keys())


def calculate_single_hash(file_data: bytes, algorithm_name: str) -> str:
    """
    Quick helper to calculate a single hash.
    
    Args:
        file_data: Raw file bytes
        algorithm_name: Name of algorithm (e.g., 'SHA-256')
        
    Returns:
        Hex digest of the hash
        
    Raises:
        ValueError: If algorithm name is not recognized
    """
    if algorithm_name not in config.HASH_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    algo = config.HASH_ALGORITHMS[algorithm_name]
    hasher = algo()
    hasher.update(file_data)
    return hasher.hexdigest()