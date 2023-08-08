import datetime
import gzip
from pathlib import Path
import click

from utils.misc import find_repository_folder, generate_id, read_slug_file, save_slug


def snap_changes(slug):
    """
    Save staged files to a snapshot.

    :param slug: The slug to associate with the snapshot.
    :type slug: str
    """
    index_file = find_repository_folder() / "index"
    
    if index_file.exists():
        with index_file.open() as index:
            index_content = index.read()
    else:
        click.echo("Kindly add files to your project before taking a snapshot.")
        return

    if not index_content.strip():
        click.echo("Skipping snap command.")
        return

    head_file = find_repository_folder() / "HEAD"
    main_branch_file = find_repository_folder() / head_file.read_text().strip()
    prev_snap_id = main_branch_file.read_text().strip()

    snap_id = generate_id(index_content.encode())
    snap_timestamp = datetime.datetime.now().isoformat()

    # Create the snap object
    snap_content = f"snap {snap_id}\n"
    if prev_snap_id:
        snap_content += f"Parent: {prev_snap_id}\n"
    snap_content += f"Date: {snap_timestamp}\n"
    snap_content += f"Slug: {slug}\n"  

    # Read the existing index content and store the files that are already staged
    with index_file.open() as index:
        for line in index:
            file_hash, file_path = line.strip().split(" ", 1)
            snap_content += f"{file_hash} {file_path}\n"

    # Save the snap object to the objects directory
    snap_object = find_repository_folder() / "objects" / f"sn_{snap_id}"
    snap_object.write_text(snap_content)

    # Compress the contents of the files and save them to the objects directory
    for line in index_content.strip().split("\n"):
        file_hash, file_path = line.strip().split(" ", 1)

        if file_hash == "DELETED":
            continue
        
        file_path = Path(file_path)
        with file_path.open("rb") as file:
            compressed_content = gzip.compress(file.read())
            file_content_path = find_repository_folder() / "objects" / file_hash
            file_content_path.write_bytes(compressed_content)

    main_branch_file.write_text(snap_id)
    index_file.write_text("")

    save_slug(slug, snap_id)
    click.echo(f"Snapshot saved successfully.")

def get_snaps(slug=None):
    """
    Get the list of snaps to be submitted.

    :param slug: The optional slug to filter snaps. Default is None.
    :type slug: str or None
    :return: A list of tuples, each containing the snap hash and a list of file hashes and paths.
    :rtype: list[(str, list[(str, str)])]
    """
    snaps_to_submit = []
    objects_dir = find_repository_folder() / "objects"

    for snap_file in objects_dir.iterdir():
        if snap_file.name.startswith("sn_"):
            with snap_file.open() as snap:
                snap_hash = snap.readline().strip().split(" ")[1]

                if slug and not any(line.strip().startswith("Slug:") and line.strip().endswith(slug) for line in snap):
                    continue

                snap_content = snap.read()
                file_hashes_and_paths = [line.strip().split(" ", 1) for line in snap_content.splitlines()]

                snaps_to_submit.append((snap_hash, file_hashes_and_paths))

    return snaps_to_submit

def show_previous_snap_files():
    """
    Show files from the previous snap, if available.
    """
    last_snap_files = get_last_snap_files()

    if not last_snap_files:
        click.echo("No previous snap found.")
        return

    click.echo("Files from the previous snap:")
    for snap_hash, file_path in last_snap_files:
        click.echo(f"{snap_hash} {file_path}")

def get_last_snap_files():
    """
    Get file hashes and paths from the last snap, if available.

    :return: A list of tuples, each containing a file hash and its path from the last snap.
    :rtype: list[(str, str)]
    """
    head_file = find_repository_folder() / "HEAD"
    main_branch_file = find_repository_folder() / head_file.read_text().strip()

    if not main_branch_file.exists() or not main_branch_file.read_text():
        return []

    snap_id = main_branch_file.read_text().strip()
    snap_object = find_repository_folder() / "objects" / f"sn_{snap_id}" 

    if not snap_object.exists():
        return []

    with snap_object.open() as snap_file:
        snap_content = snap_file.read()

    snap_lines = snap_content.strip().split("\n")

    last_snap_files = []

    for line in snap_lines:
        if line.startswith("snap") or line.startswith("Date:") or line.startswith("Slug:"):
            continue
        else:
            file_hash, file_path = line.split(" ", 1)
            last_snap_files.append((file_hash, file_path.strip()))

    return last_snap_files

def get_snap_files_content(snap_id, exclude_large_files=True, max_file_size=1048576):
    """
    Get the content of files from a snap, excluding large files if specified.

    :param snap_id: The ID of the snap.
    :type snap_id: str
    :param exclude_large_files: Whether to exclude large files. Default is True.
    :type exclude_large_files: bool
    :param max_file_size: The maximum size of a file to include. Default is 1048576 bytes (1 MB).
    :type max_file_size: int
    :return: A dictionary mapping file paths to their content.
    :rtype: dict[str, bytes]
    :raises ValueError: If the specified snap ID does not exist.
    """
    snap_object = find_repository_folder() / "objects" / f"sn_{snap_id}"
    if not snap_object.exists():
        raise ValueError(f"Snap with ID '{snap_id}' does not exist.")

    with snap_object.open() as snap_file:
        snap_content = snap_file.read()

    lines = snap_content.splitlines()[1:]
    files_content = {}

    for line in lines:
        if line.startswith("Parent:") or line.startswith("Date:") or line.startswith("Slug:"):
            continue

        file_hash, file_path = line.strip().split(" ", 1)

        if file_hash == "DELETED":
            continue

        file_path = Path(file_path)
        file_content_path = find_repository_folder() / "objects" / file_hash

        if exclude_large_files and file_content_path.stat().st_size > max_file_size:
            continue

        file_content = file_content_path.read_bytes()
        files_content[file_path] = file_content

    parent_snap_id = None
    for line in lines:
        if line.startswith("Parent:"):
            parent_snap_id = line.split(":", 1)[1].strip()
            break

    if parent_snap_id:
        parent_files_content = get_snap_files_content(parent_snap_id)
        files_content.update(parent_files_content)

    return files_content

def get_all_snaps():
    """
    Get a list of all snaps from the objects folder.

    :return: A list of Path objects representing snap files.
    :rtype: list[pathlib.Path]
    """
    objects_dir = find_repository_folder() / "objects"
    snap_files = []

    for snap_file in objects_dir.iterdir():
        if snap_file.name.startswith("sn_"):
            snap_files.append(snap_file)

    return snap_files

def get_snap_by_slug(slug):
    """
    Get a specific snap file by its slug.

    :param slug: The slug associated with the snap.
    :type slug: str
    :return: The path to the snap file if found, None otherwise.
    :rtype: pathlib.Path or None
    """
    slugs = read_slug_file()

    snap_id = slugs.get(slug)
    if not snap_id:
        click.echo("Snapshot not found.")
        return None

    snap_file = find_repository_folder() / "objects" / f"sn_{snap_id}"
    if not snap_file.exists():
        return None

    return snap_file
