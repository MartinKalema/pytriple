"""
Click-based CLI for multiline string indentation fixer.
"""
import click
import sys
from pathlib import Path
from typing import List
from ...infrastructure.container import Container

class CLIContext:
    """Context object for CLI commands."""
    
    def __init__(self):
        self.container = Container()
        self.container.wire(modules=[__name__])
        
        # Get use cases from container
        self.fix_file_use_case = self.container.fix_file_use_case()
        self.fix_directory_use_case = self.container.fix_directory_use_case()
        
        # Access repositories if needed
        self.file_repo = self.container.file_repository()
        self.parser_repo = self.container.parser_repository()

@click.group()
@click.version_option(version='1.0.0')
@click.pass_context
def cli(ctx):
    """
    Multiline String Indentation Fixer
    
    A tool to automatically fix multiline string indentation in Python files.
    Preserves relative indentation while ensuring consistent base indentation.
    """
    ctx.ensure_object(CLIContext)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--backup/--no-backup', default=True, 
              help='Create backup before modifying file (default: create backup)')
@click.option('--dry-run', is_flag=True, 
              help='Show what would be changed without modifying files')
@click.pass_obj
def fix_file(ctx: CLIContext, file_path: Path, backup: bool, dry_run: bool):
    """Fix multiline string indentation in a single Python file."""
    
    if not file_path.suffix == '.py':
        click.echo(click.style(f"Error: {file_path} is not a Python file", fg='red'))
        sys.exit(1)
    
    if dry_run:
        click.echo(click.style(f"[DRY RUN] Would process: {file_path}", fg='yellow'))
        # TODO: Add dry run logic to show what would change
        return
    
    click.echo(f"Processing file: {file_path}")
    
    result = ctx.fix_file_use_case.execute(file_path, backup)
    
    if result.error:
        click.echo(click.style(f"Error: {result.error}", fg='red'))
        sys.exit(1)
    
    if result.was_modified:
        click.echo(click.style(f"✅ Fixed {result.strings_fixed} multiline strings", fg='green'))
        if result.backup_created:
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            click.echo(f"📁 Backup created: {backup_path}")
    else:
        click.echo(click.style("ℹ️  No changes needed", fg='blue'))

@cli.command()
@click.argument('directory_path', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option('--backup/--no-backup', default=True,
              help='Create backups before modifying files (default: create backups)')
@click.option('--dry-run', is_flag=True,
              help='Show what would be changed without modifying files')
@click.option('--exclude', multiple=True, 
              help='Exclude files matching pattern (can be used multiple times)')
@click.option('--verbose', '-v', is_flag=True,
              help='Show detailed output for each file')
@click.pass_obj
def fix_directory(ctx: CLIContext, directory_path: Path, backup: bool, 
                  dry_run: bool, exclude: List[str], verbose: bool):
    """Fix multiline string indentation in all Python files in a directory."""
    
    if dry_run:
        click.echo(click.style(f"[DRY RUN] Would process directory: {directory_path}", fg='yellow'))
        # TODO: Add dry run logic
        return
    
    click.echo(f"Processing directory: {directory_path}")
    
    # Convert exclude patterns
    exclude_patterns = list(exclude) if exclude else ['test_*', '*_test.py', 'fix_*.py']
    
    if exclude_patterns:
        click.echo(f"Excluding patterns: {', '.join(exclude_patterns)}")
    
    result = ctx.fix_directory_use_case.execute(directory_path, backup, exclude_patterns)
    
    if result.errors:
        click.echo(click.style("⚠️  Errors occurred:", fg='yellow'))
        for error in result.errors:
            click.echo(click.style(f"  {error}", fg='red'))
    
    if verbose:
        click.echo("\nFile details:")
        for file_result in result.file_results:
            status = "✅" if file_result.was_modified else "➖"
            click.echo(f"  {status} {file_result.file_path}")
            if file_result.was_modified:
                click.echo(f"    Fixed {file_result.strings_fixed} strings")
    
    # Summary
    click.echo(f"\n📊 Summary:")
    click.echo(f"  Files processed: {result.files_processed}")
    click.echo(f"  Files modified: {result.files_modified}")
    click.echo(f"  Total strings fixed: {result.total_strings_fixed}")
    
    if result.files_modified > 0:
        click.echo(click.style(f"✅ Successfully fixed {result.total_strings_fixed} multiline strings!", fg='green'))
    else:
        click.echo(click.style("ℹ️  No files needed fixing", fg='blue'))

@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.pass_obj
def check(ctx: CLIContext, file_path: Path):
    """Check if a file has multiline strings that need fixing (without modifying)."""
    
    if not file_path.suffix == '.py':
        click.echo(click.style(f"Error: {file_path} is not a Python file", fg='red'))
        sys.exit(1)
    
    source_file = ctx.file_repo.read_file(file_path)
    
    if not source_file:
        click.echo(click.style(f"Error: Could not read file {file_path}", fg='red'))
        sys.exit(1)
    
    if source_file.needs_fixing:
        fixable_strings = source_file.fixable_strings
        click.echo(click.style(f"⚠️  {len(fixable_strings)} multiline strings need fixing:", fg='yellow'))
        
        for i, ms in enumerate(fixable_strings, 1):
            click.echo(f"  {i}. Line {ms.location.start.line}: {ms.context.value}")
        
        sys.exit(1)  # Exit with error code if fixes are needed
    else:
        click.echo(click.style("✅ All multiline strings are properly indented", fg='green'))


if __name__ == '__main__':
    cli()