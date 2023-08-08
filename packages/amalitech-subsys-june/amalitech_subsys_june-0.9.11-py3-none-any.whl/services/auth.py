import click
import requests
from tqdm import tqdm

from utils.misc import read_config


def authenticate(password):
    """
    Authenticate the user using the provided password and student ID.

    :param password: The password for authentication.
    :type password: str
    :return: The session cookie upon successful authentication, None otherwise.
    :rtype: str or None
    """
    api_url = "https://gitinspired-june-api.amalitech-dev.net/api/auth/login"
    config = read_config()
    student_id = config.get("DEFAULT", "StudentID", fallback="")
    
    session = requests.Session()
    
    # Perform authentication with the server using the student ID and password
    try:
        with tqdm(total=100, desc="Logging in", unit="%", unit_divisor=1, ncols=80) as pbar:
            response = requests.post(api_url, data={"loginId": student_id, "password": password}, stream=True)
            response.raise_for_status()

            # Retrieve the session cookie from the response headers
            session_cookie = response.cookies.get("connect.sid")

            # Set the session cookie in the headers for subsequent requests
            session.headers.update({"Cookie": f"connect.sid={session_cookie}"})

            for chunk in response.iter_content(chunk_size=1024):
                pbar.update(len(chunk))

        click.echo("\n================================\nAuthentication successful")
        return session_cookie
    except requests.exceptions.RequestException as e:
        click.echo("\nAuthentication failed! try again.")
        return None