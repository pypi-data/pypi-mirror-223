import pathlib
from typing import Optional

from copernicus_marine_client.core_functions.get import get_function
from copernicus_marine_client.core_functions.utils import (
    DEFAULT_CLIENT_BASE_DIRECTORY,
)


def get(
    dataset_url: Optional[str] = None,
    dataset_id: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    no_directories: bool = False,
    show_outputnames: bool = False,
    output_directory: Optional[pathlib.Path] = None,
    credentials_file: pathlib.Path = DEFAULT_CLIENT_BASE_DIRECTORY,
    overwrite_output_data: bool = False,
    request_file: Optional[pathlib.Path] = None,
    force_service: Optional[str] = None,
    overwrite_metadata_cache: bool = False,
    no_metadata_cache: bool = False,
    filter: Optional[str] = None,
    regex: Optional[str] = None,
):
    return get_function(
        dataset_url,
        dataset_id,
        username,
        password,
        no_directories,
        show_outputnames,
        output_directory,
        credentials_file,
        True,
        overwrite_output_data,
        request_file,
        force_service,
        overwrite_metadata_cache,
        no_metadata_cache,
        filter,
        regex,
    )
