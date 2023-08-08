from pathlib import Path
import click

from utils.misc import find_repository_folder, generate_id, list_all_files, read_ignore_file


# Global constant for the .subsys folder
WORKING_DIR = find_repository_folder()

# Function to stage changes by adding files to the index
def stage_changes(files, ignore_list):
    """
    Stage changes by adding files to the index.

    :param files: List of files to stage changes for.
    :type files: list[pathlib.Path]
    :param ignore_list: List of patterns to ignore when staging changes.
    :type ignore_list: list[str]
    """
    index_file = find_repository_folder() / "index"
    staged_files = set()

    if index_file.exists():
        with index_file.open() as index:
            for line in index:
                file_hash, file_path = line.strip().split(" ", 1)
                staged_files.add(file_path)

    all_snap_files = []
    deleted_paths = set()
    head_file = find_repository_folder() / "HEAD"
    main_branch_file = find_repository_folder() / head_file.read_text().strip()

    current_snap_id = main_branch_file.read_text().strip()
    while current_snap_id:
        current_snap_object = find_repository_folder() / "objects" / f"sn_{current_snap_id}"
        with current_snap_object.open() as snap_file:
            snap_content = snap_file.read()
            snap_lines = snap_content.strip().split("\n")
            for line in snap_lines:
                if not line.startswith("snap") and not line.startswith("Date:") and not line.startswith("Slug:") and not line.startswith("Parent:"):
                    file_hash, file_path = line.split(" ", 1)
                    if file_hash == "DELETED":
                        deleted_paths.add(Path(file_path.strip()))
                    all_snap_files.append((file_hash, file_path.strip()))

        parent_snap_id = None
        for line in snap_lines:
            if line.startswith("Parent:"):
                parent_snap_id = line.split(":", 1)[1].strip()
                break

        current_snap_id = parent_snap_id

    ignored_paths = set()
    for ignore_pattern in ignore_list:
        ignored_paths.update(Path(".").rglob(ignore_pattern))

    # Determine the changes for each file in the working directory
    for file in files:
        if file not in ignored_paths:
            file_hash = generate_id(file.read_bytes())

            # Check if the file has changed, is newly added
            last_snap_hash = next((hash for hash, path in all_snap_files if path == str(file)), None)
            if last_snap_hash is None:
                with index_file.open("a") as index:
                    index.write(f"{file_hash} {file}\n")
                    staged_files.add(file_hash)
            elif file_hash != last_snap_hash:
                with index_file.open("a") as index:
                    index.write(f"{file_hash} {file}\n")
                    staged_files.add(file_hash)

    # Check for deleted files
    for hash, path in all_snap_files:
        file_path = Path(path)
        if file_path not in files and file_path not in ignored_paths and file_path not in deleted_paths:
            with index_file.open("a") as index:
                index.write(f"DELETED {path}\n")
                staged_files.add("DELETED")

    if not staged_files:
        click.echo("No changes found to stage.")
    else:
        click.echo("Staged changes successfully.")

def add():
    """
    Stage all changed files to index.
    """
    ignore_list = read_ignore_file()

    root_dir = WORKING_DIR.relative_to(WORKING_DIR)
    files = list_all_files(root_dir, ignore_list)

    stage_changes(files, ignore_list)
