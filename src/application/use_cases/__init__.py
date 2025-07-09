"""Use cases for multiline string indentation fixer."""

from .fix_file_indentation import FixFileIndentationUseCase, FixFileResult
from .fix_directory_indentation import FixDirectoryIndentationUseCase, FixDirectoryResult

__all__ = [
    'FixFileIndentationUseCase', 
    'FixFileResult',
    'FixDirectoryIndentationUseCase', 
    'FixDirectoryResult'
]