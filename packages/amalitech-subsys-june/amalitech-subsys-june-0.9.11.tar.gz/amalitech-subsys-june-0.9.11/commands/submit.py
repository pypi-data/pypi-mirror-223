import click

from services.auth import authenticate
from services.submit import submit_snap
from utils.misc import is_initialized
from utils.snap import get_all_snaps, get_snap_by_slug


@click.command()
@click.option("--snapshot", "-s", help="Submit a specific snap corresponding to the provided snapshot.")
def submit(snapshot):
    """
    Submits the assignment snapshots to the central repository.
    """
    if not is_initialized():
        click.echo("Please initialize a repository.\nRun subsys init.")
        return

    # Authenticate the user before proceeding with the submission
    password = click.prompt("Enter your password", hide_input=True)
    session_cookie = authenticate(password)
    if not session_cookie:
        click.echo("Submission aborted.")
        return

    if snapshot:
        # Submit a specific snap corresponding to the provided snapshot
        snap_file = get_snap_by_slug(snapshot)
        if not snap_file:
            click.echo(f"Error: Snapshot with snapshot '{snapshot}' not found.")
            return

        snap_id = snap_file.name[len("sn_"):]
        submit_snap(snap_id, session_cookie)
    else:
        # Submit all available snaps one by one
        snaps_to_submit = get_all_snaps()
        if not snaps_to_submit:
            click.echo("No snaps found to submit.")
            return

        for snap_file in snaps_to_submit:
            snap_id = snap_file.name[len("sn_"):]
            submit_snap(snap_id, session_cookie)