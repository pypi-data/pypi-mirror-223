import click

from utils.misc import is_initialized, read_config, write_config


# Config command for interactive and non-interactive configuration
@click.command()
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode to input the code and student ID.")
@click.option("--code", "-c", help="Set the code.")
@click.option("--student_id", "-s", help="Set the student ID.")
def config(code, student_id, interactive):
    """
    Configures the repository with student and assignment details.
    """
    if not is_initialized():
        click.echo("Please initialize a repository.\nRun subsys init.")
        return
    
    if interactive:
        # Interactive mode
        code = click.prompt("Enter assignment code:")
        student_id = click.prompt("Enter the student ID:")

    if not student_id or not code:
        click.echo("Assignment code and student ID are required.")
        return
    
    write_config("Code", code) 
    write_config("StudentID", student_id) 

    # Read the configuration from the .subsysconfig file
    config = read_config()
    code_value = config.get("DEFAULT", "Code", fallback="")
    student_id_value = config.get("DEFAULT", "StudentID", fallback="")

    # Display the current configuration values.
    click.echo("Configuration saved successfully.")
    click.echo(f"Code: {code_value}")
    click.echo(f"Student ID: {student_id_value}")