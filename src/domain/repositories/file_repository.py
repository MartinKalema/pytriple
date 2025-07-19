"""
Repository interface for file operations.
"""
from pathlib import Path
from typing import List, Optional, Protocol
from ..entities.source_file import SourceFile

class FileRepository(Protocol):
    """Repository protocol for file operations."""
    
    def read_file(self, path: Path) -> Optional[SourceFile]:
        """Read a Python source file.
        
        Args:
            path: Path to the Python file to read.
            
        Returns:
            Optional[SourceFile]: Parsed source file or None if file cannot be read.
        """
        ...
    
    def write_file(self, source_file: SourceFile) -> bool:
        """Write a source file with fixed content.
        
        Args:
            source_file: SourceFile entity with fixed content to write.
            
        Returns:
            bool: True if write was successful, False otherwise.
        """
        ...
    
    def create_backup(self, source_file: SourceFile) -> bool:
        """Create a backup of the source file.
        
        Args:
            source_file: SourceFile entity to backup.
            
        Returns:
            bool: True if backup was created successfully, False otherwise.
        """
        ...
    
    def find_python_files(self, directory: Path) -> List[Path]:
        """Find all Python files in a directory.
        
        Args:
            directory: Root directory to search for Python files.
            
        Returns:
            List[Path]: List of paths to all Python files found.
        """
        ...
    
    def file_exists(self, path: Path) -> bool:
        """Check if a file exists.
        
        Args:
            path: Path to check for existence.
            
        Returns:
            bool: True if file exists, False otherwise.
        """
        ...