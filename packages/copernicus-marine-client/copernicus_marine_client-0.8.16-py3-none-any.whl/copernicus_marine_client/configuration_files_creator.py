import base64
import configparser
import logging
import pathlib
from dataclasses import dataclass
from datetime import timedelta
from netrc import netrc
from platform import system
from typing import Literal, Optional

import click
import lxml.html
import requests
from cachier import cachier


def load_credential_from_copernicus_marine_configuration_file(
    credential_type: Literal["username", "password"],
    configuration_filename: pathlib.Path,
) -> Optional[str]:
    configuration_file = open(configuration_filename)
    configuration_string = base64.standard_b64decode(
        configuration_file.read()
    ).decode("utf8")
    config = configparser.RawConfigParser()
    config.read_string(configuration_string)
    credential = config.get("credentials", credential_type)
    if credential:
        logging.debug(
            f"{credential_type} loaded from {configuration_filename}"
        )
    return credential


def load_credential_from_netrc_configuration_file(
    credential_type: Literal["username", "password"],
    configuration_filename: pathlib.Path,
    host: str,
) -> Optional[str]:
    authenticator = netrc(configuration_filename).authenticators(host=host)
    if authenticator:
        username, _, password = authenticator
        logging.debug(
            f"{credential_type} loaded from {configuration_filename}"
        )
        return username if credential_type == "username" else password
    else:
        return None


def load_credential_from_motu_configuration_file(
    credential_type: Literal["username", "password"],
    configuration_filename: pathlib.Path,
) -> Optional[str]:
    motu_file = open(configuration_filename)
    motu_credential_type = "user" if credential_type == "username" else "pwd"
    config = configparser.RawConfigParser()
    config.read_string(motu_file.read())
    credential = config.get("Main", motu_credential_type)
    if credential:
        logging.debug(
            f"{credential_type} loaded from {configuration_filename}"
        )
    return credential


def retrieve_credential_from_configuration_files(
    credential_type: Literal["username", "password"],
    configuration_file_directory: pathlib.Path,
    host: str = "default_host",
) -> Optional[str]:
    copernicus_marine_client_configuration_filename = pathlib.Path(
        configuration_file_directory, ".copernicus_marine_client_credentials"
    )
    netrc_type = "_netrc" if system() == "Windows" else ".netrc"
    netrc_filename = pathlib.Path(configuration_file_directory, netrc_type)
    motu_filename = pathlib.Path(
        configuration_file_directory, "motuclient-python.ini"
    )
    if copernicus_marine_client_configuration_filename.exists():
        credential = load_credential_from_copernicus_marine_configuration_file(
            credential_type, copernicus_marine_client_configuration_filename
        )
    elif netrc_filename.exists():
        credential = load_credential_from_netrc_configuration_file(
            credential_type, netrc_filename, host=host
        )
    elif motu_filename.exists():
        credential = load_credential_from_motu_configuration_file(
            credential_type, motu_filename
        )
    else:
        credential = None
    return credential


def create_copernicus_marine_client_configuration_file(
    username: str,
    password: str,
    configuration_file_directory: pathlib.Path,
    overwrite_configuration_file: bool,
) -> None:
    configuration_lines = [
        "[credentials]\n",
        f"username={username}\n",
        f"password={password}\n",
    ]
    configuration_filename = pathlib.Path(
        configuration_file_directory, ".copernicus_marine_client_credentials"
    )
    if configuration_filename.exists() and not overwrite_configuration_file:
        click.confirm(
            f"File {configuration_filename} already exists, overwrite it ?",
            abort=True,
        )
    configuration_file = open(configuration_filename, "w")
    configuration_string = base64.b64encode(
        "".join(configuration_lines).encode("ascii", "strict")
    ).decode("utf8")
    configuration_file.write(configuration_string)
    configuration_file.close()


@dataclass
class CheckCredentialsResponse:
    error: Optional[ConnectionRefusedError]


@cachier(stale_after=timedelta(hours=5))
def check_copernicus_marine_credentials(
    username: Optional[str], password: Optional[str]
) -> CheckCredentialsResponse:
    """
    Check provided Copernicus Marine Credentials are correct.

    Parameters
    ----------
    username : str
        Copernicus Marine Username, provided for free from https://marine.copernicus.eu
    password : str
        Copernicus Marine Password, provided for free from https://marine.copernicus.eu

    """
    cmems_cas_url = "https://cmems-cas.cls.fr/cas/login"
    conn_session = requests.session()
    login_session = conn_session.get(cmems_cas_url)
    login_from_html = lxml.html.fromstring(login_session.text)
    hidden_elements_from_html = login_from_html.xpath(
        '//form//input[@type="hidden"]'
    )
    playload = {
        he.attrib["name"]: he.attrib["value"]
        for he in hidden_elements_from_html
    }
    playload["username"] = username
    playload["password"] = password
    response = conn_session.post(cmems_cas_url, data=playload)
    if response.text.find("success") == -1:
        check_credentials_response = CheckCredentialsResponse(
            error=ConnectionRefusedError(
                "Incorrect username or password.\n"
                "Learn how to recover your credentials at: "
                "https://help.marine.copernicus.eu/en/articles/"
                "4444552-i-forgot-my-username-or-my-password-what-should-i-do"
            )
        )
        logging.error(check_credentials_response.error)
        return check_credentials_response
    return CheckCredentialsResponse(error=None)


def main(
    username: str,
    password: str,
    configuration_file_directory: pathlib.Path,
    overwrite_configuration_file: bool,
) -> None:
    if not configuration_file_directory.exists():
        pathlib.Path.mkdir(configuration_file_directory, parents=True)
    create_copernicus_marine_client_configuration_file(
        username=username,
        password=password,
        configuration_file_directory=configuration_file_directory,
        overwrite_configuration_file=overwrite_configuration_file,
    )
