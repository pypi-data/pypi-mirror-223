import configparser
import hashlib
from pathlib import Path


# Global constant for the .subsys folder
SUBSYS_FOLDER = Path(".subsys")

def generate_id(content):
    """
    Generate a unique ID based on content using SHA-1 hash.

    :param content: The content to generate the hash from.
    :type content: bytes
    :return: The generated unique ID.
    :rtype: str
    """
    sha1 = hashlib.sha1()
    sha1.update(content)
    return sha1.hexdigest()

def find_repository_folder(start_path=None):
    """
    Function to find the repository till root or return None if not found.

    :param start_path: The starting path for searching. If None, the current working directory is used.
    :type start_path: str or None
    :return: The path of the repository folder if found, else None.
    :rtype: pathlib.Path or None
    """
    if start_path is None:
        start_path = Path.cwd()
    current_directory = Path(start_path)

    while current_directory != Path(current_directory.parts[0]):
        subsys_folder = current_directory / SUBSYS_FOLDER
        if subsys_folder.exists():
            return subsys_folder
        
        current_directory = current_directory.parent

    return None

def is_initialized():
    """
    Check if the repository has been initialized with .subsys.

    :return: True if initialized, False otherwise.
    :rtype: bool
    """
    if find_repository_folder():
        return True

    return False

def write_config(name, variable):
    """
    Write a configuration value to the config file inside the .subsys folder.

    :param name: The name of the configuration value.
    :type name: str
    :param variable: The value to be written.
    :type variable: str
    """
    config_folder = find_repository_folder()
    config_path = config_folder / ".subsysconfig"

    config = configparser.ConfigParser()
    if config_path.exists():
        config.read(config_path)

    if "DEFAULT" not in config:
        config["DEFAULT"] = {}

    config["DEFAULT"][name] = variable

    with open(config_path, "w") as configfile:
        config.write(configfile)

def read_config():
    """
    Read the configuration from the config file inside the .subsys folder.

    :return: The parsed configuration.
    :rtype: configparser.ConfigParser
    """
    config = configparser.ConfigParser()
    config_file = find_repository_folder() / ".subsysconfig"
    if config_file.exists():
        config.read(config_file)
    return config

def update_submission_id(submission_id):
    """
    Update the configuration with the submission ID.

    :param submission_id: The submission ID to update.
    :type submission_id: str
    """
    config = read_config()
    config.set("DEFAULT", "SubmissionID", submission_id)

    config_file = find_repository_folder() / ".subsysconfig"
    with open(config_file, "w") as configfile:
        config.write(configfile)

def list_all_files(directory, ignore_list):
    """
    Recursively list all files in a directory, excluding certain files and directories.

    :param directory: The directory to start listing from.
    :type directory: pathlib.Path
    :param ignore_list: A list of filenames to ignore.
    :type ignore_list: list[str]
    :return: A list of paths to all the files found.
    :rtype: list[pathlib.Path]
    """
    all_files = []
    for path in directory.rglob("*"):
        if path.is_file() and not str(path).startswith(".subsys") and path.name not in ignore_list:
            ignore_file = any(ignore_pattern in str(path) for ignore_pattern in ignore_list)
            if not ignore_file:
                all_files.append(path)
    return all_files

def read_ignore_file():
    """
    Read the contents of the .subsysignore file.

    :return: A list of filenames to ignore.
    :rtype: list[str]
    """
    ignore_list = []
    ignore_file = find_repository_folder().parent / ".subsysignore"
    if ignore_file.exists():
        with ignore_file.open() as f:
            ignore_list = f.read().splitlines()
    return ignore_list

def save_slug(slug, snap_id):
    """
    Save the provided slug and snap ID to the SLUGS file.

    :param slug: The slug to save.
    :type slug: str
    :param snap_id: The associated snap ID.
    :type snap_id: str
    """
    slugs_file = find_repository_folder() / "SLUGS"
    with slugs_file.open("a") as f:
        f.write(f"{slug} {snap_id}\n")

def read_slug_file():
    """
    Read the slugs and their corresponding snap IDs from the SLUGS file.

    :return: A dictionary mapping slugs to snap IDs.
    :rtype: dict[str, str]
    """
    slugs_file = find_repository_folder() / "SLUGS"
    slugs = {}

    if slugs_file.exists():
        with slugs_file.open() as f:
            for line in f:
                slug, snap_id = line.strip().split(" ")
                slugs[slug] = snap_id

    return slugs
