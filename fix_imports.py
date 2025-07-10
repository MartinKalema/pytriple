#!/usr/bin/env python3
"""Fix relative imports to absolute imports."""
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix imports in a single file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace relative imports with absolute imports
    replacements = [
        (r'from \.\.\.domain', 'from domain'),
        (r'from \.\.\.infrastructure', 'from infrastructure'),
        (r'from \.\.\.application', 'from application'),
        (r'from \.\.\.presentation', 'from presentation'),
        (r'from \.\.domain', 'from domain'),
        (r'from \.\.infrastructure', 'from infrastructure'),
        (r'from \.\.application', 'from application'),
        (r'from \.\.presentation', 'from presentation'),
        (r'from \.\.dtos', 'from application.dtos'),
    ]
    
    modified = False
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            modified = True
            content = new_content
    
    if modified:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Fixed imports in {file_path}")

# Fix all Python files in src
src_dir = Path('src')
for py_file in src_dir.rglob('*.py'):
    fix_imports_in_file(py_file)

print("Import fixing complete!")