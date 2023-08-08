import os
from pathlib import Path

import click


def create_repository():
    """
    Create a new "subsys" repository with the necessary directory structure.

    The function creates the following structure:
    - .subsys/
      - objects/
      - refs/heads/
      - HEAD (initialized with reference to the main branch)
      - main (initialized as an empty snap)

    The .subsys folder will be set as hidden on Windows.

    This function doesn't return anything, it directly creates the repository structure.

    """
    root_dir = Path(".subsys")
    root_dir.mkdir(parents=True, exist_ok=True)

    objects_dir = root_dir / "objects"
    objects_dir.mkdir(exist_ok=True)

    refs_dir = root_dir / "refs" / "heads"
    refs_dir.mkdir(parents=True, exist_ok=True)

    head_file = root_dir / "HEAD"
    head_file.write_text("refs/heads/main")

    main_branch_file = refs_dir / "main"
    main_branch_file.write_text("")

    if os.name == 'nt':
        try:
            os.system(f"attrib +h {str(root_dir)}")
        except Exception:
            pass

    click.echo("Initialized empty subsys repository.")