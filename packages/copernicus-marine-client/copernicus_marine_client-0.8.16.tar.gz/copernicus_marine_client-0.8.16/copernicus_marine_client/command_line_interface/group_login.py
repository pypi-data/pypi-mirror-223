import logging
import logging.config
import pathlib
from typing import Literal, Optional, Tuple

import click

from copernicus_marine_client.configuration_files_creator import (
    check_copernicus_marine_credentials,
)
from copernicus_marine_client.configuration_files_creator import (
    main as configuration_files_creator,
)
from copernicus_marine_client.configuration_files_creator import (
    retrieve_credential_from_configuration_files,
)
from copernicus_marine_client.utils import DEFAULT_CLIENT_BASE_DIRECTORY


@click.group()
def cli_group_login() -> None:
    pass


@cli_group_login.command(
    "login",
    short_help="Login to the Copernicus Marine Service",
    help="""
    Login to the Copernicus Marine Service.

    Create a configuration file under the $HOME/.copernicus_marine_client directory (overwritable with option --configuration-file-directory).
    """,  # noqa
    epilog="""
    Examples:

    \b
    COPERNICUS_MARINE_SERVICE_USERNAME=<USERNAME> COPERNICUS_MARINE_SERVICE_PASSWORD=<PASSWORD> copernicus-marine login

    \b
    copernicus-marine login --username <USERNAME> --password <PASSWORD>

    \b
    copernicus-marine login
    > Username: [USER-INPUT]
    > Password: [USER-INPUT]
    """,  # noqa
)
@click.option(
    "--username",
    prompt="username",
    envvar="COPERNICUS_MARINE_SERVICE_USERNAME",
    hide_input=False,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_USERNAME"
    + ", or else ask for user input",
)
@click.option(
    "--password",
    prompt="password",
    envvar="COPERNICUS_MARINE_SERVICE_PASSWORD",
    hide_input=True,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_PASSWORD"
    + ", or else ask for user input",
)
@click.option(
    "--configuration-file-directory",
    type=click.Path(path_type=pathlib.Path),
    default=DEFAULT_CLIENT_BASE_DIRECTORY,
    help="Path to the directory where the configuration file is stored",
)
@click.option(
    "--overwrite-configuration-file",
    "-overwrite",
    is_flag=True,
    default=False,
    help="Flag to skip confirmation before overwriting configuration file",
)
@click.option(
    "--verbose",
    type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "QUIET"]),
    default="INFO",
    help=(
        "Set the details printed to console by the command "
        "(based on standard logging library)."
    ),
)
def login(
    username: str,
    password: str,
    configuration_file_directory: pathlib.Path,
    overwrite_configuration_file: bool,
    verbose: str = "INFO",
) -> None:
    if verbose == "QUIET":
        logging.root.disabled = True
        logging.root.setLevel(level="CRITICAL")
    else:
        logging.root.setLevel(level=verbose)
    check_copernicus_marine_credentials(username, password)
    configuration_files_creator(
        username=username,
        password=password,
        configuration_file_directory=configuration_file_directory,
        overwrite_configuration_file=overwrite_configuration_file,
    )
    logging.info(
        f"Configuration files stored in {configuration_file_directory}"
    )


def get_credential(
    credential: Optional[str],
    credential_type: Literal["username", "password"],
    hide_input: bool,
    configuration_file_directory: pathlib.Path,
) -> str:
    if not credential:
        credential = retrieve_credential_from_configuration_files(
            credential_type=credential_type,
            configuration_file_directory=configuration_file_directory,
            host="my.cmems-du.eu",  # Same credentials for all hosts
        )
        if not credential:
            credential = click.prompt(credential_type, hide_input=hide_input)
            if not credential:
                raise ValueError(f"{credential} cannot be None")
    else:
        logging.debug(
            "Credentials loaded from function arguments or environment variable"
        )
    return credential


def get_username_password(
    username: Optional[str],
    password: Optional[str],
    configuration_file_directory: pathlib.Path,
) -> Tuple[str, str]:
    username = get_credential(
        username,
        "username",
        hide_input=False,
        configuration_file_directory=configuration_file_directory,
    )
    password = get_credential(
        password,
        "password",
        hide_input=True,
        configuration_file_directory=configuration_file_directory,
    )
    result_check = check_copernicus_marine_credentials(username, password)
    if result_check.error:
        logging.warning(
            "Invalid credentials, your download will not be authenticated"
        )
    return (username, password)


if __name__ == "__main__":
    cli_group_login()
