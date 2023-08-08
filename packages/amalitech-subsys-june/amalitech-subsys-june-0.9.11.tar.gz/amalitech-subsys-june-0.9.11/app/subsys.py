import click
from commands.init import init
from commands.config import config
from commands.snap import snap
from commands.submit import submit


@click.group()
def cli():
    """ 
    Subsys is a streamlined version control system tailored for students and text-based projects.
    It offers an intuitive command-line interface for managing snapshots, tracking changes, and submitting work to a central server.
    """
    pass


cli.add_command(init)
cli.add_command(config)
cli.add_command(snap)
cli.add_command(submit)

if __name__ == "__main__":
    cli()
