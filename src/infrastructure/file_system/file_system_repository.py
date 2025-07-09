"""
File system implementation of file repository.
"""
import os
from pathlib import Path
from typing import List, Optional
from ...domain.entities.source_file import SourceFile
from ...domain.repositories.parser_repository import ParserRepository

class FileSystemRepository:
    """File system implementation of file repository."""
    
    def __init__(self, parser_repo: ParserRepository):
        self.parser_repo = parser_repo
    
    def read_file(self, path: Path) -> Optional[SourceFile]:
        """Read a Python source file."""
        try:
            if not path.exists() or not path.is_file():
                return None
            
            if path.suffix != '.py':
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse multiline strings (empty files will have no strings)
            multiline_strings = []
            if content.strip():  # Only parse non-empty files
                multiline_strings = self.parser_repo.parse_multiline_strings(content)
            
            return SourceFile(
                path=path,
                content=content,
                multiline_strings=multiline_strings
            )
            
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return None
    
    def write_file(self, source_file: SourceFile) -> bool:
        """Write a source file with fixed content."""
        try:
            with open(source_file.path, 'w', encoding='utf-8') as f:
                f.write(source_file.content)
            return True
            
        except Exception as e:
            print(f"Error writing file {source_file.path}: {e}")
            return False
    
    def create_backup(self, source_file: SourceFile) -> bool:
        """Create a backup of the source file."""
        try:
            backup_path = source_file.create_backup_path()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(source_file.content)
            
            return True
            
        except Exception as e:
            print(f"Error creating backup for {source_file.path}: {e}")
            return False
    
    def find_python_files(self, directory: Path) -> List[Path]:
        """Find all Python files in a directory."""
        python_files = []
        
        try:
            for root, dirs, files in os.walk(directory):
                # Skip hidden directories and __pycache__
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(Path(root) / file)
            
            return python_files
            
        except Exception as e:
            print(f"Error finding Python files in {directory}: {e}")
            return []
    
    def file_exists(self, path: Path) -> bool:
        """Check if a file exists."""
        return path.exists() and path.is_file()