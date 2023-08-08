from pathlib import Path
import click
import slugify

from utils.misc import find_repository_folder, is_initialized, read_slug_file
from utils.snap import snap_changes
from utils.stage import add


@click.command()
@click.option("--name", required=True, help="Unique slug to identify each snap.")
def snap(name):
    """
    Creates a new snapshot of the assignment progress.
    """
    if not is_initialized():
        click.echo("Please initialize a repository.\nRun subsys init.")
        return
    
    # Get the current working directory
    current_dir = Path.cwd()

    # Check if the current directory is the working directory
    if current_dir != find_repository_folder().parent:
        click.echo("Error: Please navigate to the working directory before using this command.")
        return
    
    # Validate the slug using slugify
    valid_slug = slugify.slugify(str(name))

    if name != valid_slug:
        click.echo("Error: Invalid slug provided. Please use only alphanumeric characters and hyphens.")
        return

    # Read the list of unique slugs
    unique_slugs = read_slug_file()

    if valid_slug in unique_slugs:
        click.echo(f"Error: Snapshot {name} already exists. Please enter a different name.")
        return
    
    # Stage all changes
    add()

    # Snap changes and create a new snap
    snap_changes(valid_slug)
    