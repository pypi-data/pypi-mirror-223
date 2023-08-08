import click

from utils.misc import is_initialized
from utils.repository import create_repository


@click.command()
def init():
    """
    Initializes a new repository in the current directory.
    """
    if is_initialized():
        click.echo("Error: subsys repository already initialized.")
    else:
        create_repository()