import logging
import logging.config
import pathlib
import sys
from datetime import datetime
from typing import List, Optional

import click

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineDatasetServiceType,
    parse_catalogue,
)
from copernicus_marine_client.catalogue_parser.request_structure import (
    SubsetRequest,
    convert_motu_api_request_to_structure,
    subset_request_from_file,
)
from copernicus_marine_client.command_line_interface.exception_handler import (
    log_exception_and_exit,
)
from copernicus_marine_client.command_line_interface.group_login import (
    get_username_password,
)
from copernicus_marine_client.command_line_interface.utils import (
    MutuallyExclusiveOption,
)
from copernicus_marine_client.download_functions.download_arco_series import (
    download_zarr,
)
from copernicus_marine_client.download_functions.download_motu import (
    download_motu,
)
from copernicus_marine_client.download_functions.download_opendap import (
    download_opendap,
)
from copernicus_marine_client.services_utils import (
    CommandType,
    get_dataset_service,
)
from copernicus_marine_client.utils import (
    DEFAULT_CLIENT_BASE_DIRECTORY,
    OVERWRITE_LONG_OPTION,
    OVERWRITE_OPTION_HELP_TEXT,
    OVERWRITE_SHORT_OPTION,
)


@click.group()
def cli_group_subset() -> None:
    pass


@cli_group_subset.command(
    "subset",
    short_help="Download subsets of datasets as NetCDF files or Zarr stores",
    help="""
    Download subsets of datasets as NetCDF files or Zarr stores.

    Either one of --dataset-id or --dataset-url is required (can be found via the "describe" command).
    The arguments value passed individually through the CLI take precedence over the values from the --motu-api-request option,
    which takes precedence over the ones from the --request-file option
    """,  # noqa
    epilog="""
    Examples:

    \b
    copernicus-marine subset
    --dataset-id METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
    --variable analysed_sst --variable sea_ice_fraction
    --start-datetime 2021-01-01 --end-datetime 2021-01-02
    --minimal-longitude 0.0 --maximal-longitude 0.1
    --minimal-latitude 0.0 --maximal-latitude 0.1

    \b
    copernicus-marine subset -i METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v analysed_sst -v sea_ice_fraction -t 2021-01-01 -T 2021-01-02 -x 0.0 -X 0.1 -y 0.0 -Y 0.1
    """,  # noqa
)
@click.option(
    "--dataset-url",
    "-u",
    type=str,
    help="The full dataset URL.",
)
@click.option(
    "--dataset-id",
    "-i",
    type=str,
    help="The dataset id.",
)
@click.option(
    "--username",
    type=str,
    envvar="COPERNICUS_MARINE_SERVICE_USERNAME",
    default=None,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_USERNAME"
    + ", or else look for configuration files, or else ask for user input.",
)
@click.option(
    "--password",
    type=str,
    envvar="COPERNICUS_MARINE_SERVICE_PASSWORD",
    default=None,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_PASSWORD"
    + ", or else look for configuration files, or else ask for user input.",
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=str,
    help="Specify dataset variables",
    multiple=True,
)
@click.option(
    "--minimal-longitude",
    "-x",
    type=float,
    help=(
        "Minimal longitude for the subset. "
        "The value will be reduced to the interval [-180; 360[."
    ),
)
@click.option(
    "--maximal-longitude",
    "-X",
    type=float,
    help=(
        "Maximal longitude for the subset. "
        "The value will be reduced to the interval [-180; 360[."
    ),
)
@click.option(
    "--minimal-latitude",
    "-y",
    type=click.FloatRange(min=-90, max=90),
    help="Minimal latitude for the subset. Requires a float within this range:",
)
@click.option(
    "--maximal-latitude",
    "-Y",
    type=click.FloatRange(min=-90, max=90),
    help="Maximal latitude for the subset. Requires a float within this range:",
)
@click.option(
    "--minimal-depth",
    "-z",
    type=click.FloatRange(min=0),
    help="Minimal depth for the subset. Requires a float within this range:",
)
@click.option(
    "--maximal-depth",
    "-Z",
    type=click.FloatRange(min=0),
    help="Maximal depth for the subset. Requires a float within this range:",
)
@click.option(
    "--vertical-dimension-as-originally-produced",
    type=bool,
    default=True,
    show_default=True,
    help=(
        "Consolidate the vertical dimension (the z-axis) as it is in the "
        "dataset originally produced, "
        "named `depth` with descending positive values."
    ),
)
@click.option(
    "--start-datetime",
    "-t",
    type=click.DateTime(
        ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
    ),
    help="The start datetime of the temporal subset. Caution: encapsulate date "
    + 'with " " to ensure valid expression for format "%Y-%m-%d %H:%M:%S".',
)
@click.option(
    "--end-datetime",
    "-T",
    type=click.DateTime(
        ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
    ),
    help="The end datetime of the temporal subset. Caution: encapsulate date "
    + 'with " " to ensure valid expression for format "%Y-%m-%d %H:%M:%S".',
)
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(path_type=pathlib.Path),
    help="The destination folder for the downloaded files."
    + " Default is the current directory.",
)
@click.option(
    "--configuration-file-directory",
    type=click.Path(path_type=pathlib.Path),
    default=DEFAULT_CLIENT_BASE_DIRECTORY,
    help="Path to a directory where a configuration file is stored. Accepts "
    + ".copernicus_marine_client_credentials / .netrc or _netrc / "
    + "motuclient-python.ini files.",
)
@click.option(
    "--output-filename",
    "-f",
    type=click.Path(path_type=pathlib.Path),
    help=(
        "Concatenate the downloaded data in the given file name "
        "(under the output directory). If "
        "the output-filename argument ends with '.nc' suffix, the file will be "
        "downloaded as a netCDF file."
    ),
)
@click.option(
    "--force-download",
    is_flag=True,
    default=False,
    help="Flag to skip confirmation before download.",
)
@click.option(
    OVERWRITE_LONG_OPTION,
    OVERWRITE_SHORT_OPTION,
    is_flag=True,
    default=False,
    help=OVERWRITE_OPTION_HELP_TEXT,
)
@click.option(
    "--force-service",
    "-s",
    type=str,
    help=(
        "Force download through one of the available services "
        f"using the service name among {CommandType.SUBSET.service_names()} "
        f"or its short name among {CommandType.SUBSET.service_short_names()}."
    ),
)
@click.option(
    "--request-file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Option to pass a file containing CLI arguments. "
    "The file MUST follow the structure of dataclass 'SubsetRequest'.",
)
@click.option(
    "--motu-api-request",
    type=str,
    help=(
        "Option to pass a complete MOTU api request as a string. "
        'Caution, user has to replace double quotes " with single '
        "quotes ' in the request."
    ),
)
@click.option(
    "--overwrite-metadata-cache",
    cls=MutuallyExclusiveOption,
    type=bool,
    is_flag=True,
    default=False,
    help="Force to refresh the catalogue by overwriting the local cache.",
    mutually_exclusive=["no_metadata_cache"],
)
@click.option(
    "--no-metadata-cache",
    cls=MutuallyExclusiveOption,
    type=bool,
    is_flag=True,
    default=False,
    help="Bypass the use of cache.",
    mutually_exclusive=["overwrite_metadata_cache"],
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "QUIET"]),
    default="INFO",
    help=(
        "Set the details printed to console by the command "
        "(based on standard logging library)."
    ),
)
@log_exception_and_exit
def subset(
    dataset_url: Optional[str],
    dataset_id: Optional[str],
    username: Optional[str],
    password: Optional[str],
    variables: Optional[List[str]],
    minimal_longitude: Optional[float],
    maximal_longitude: Optional[float],
    minimal_latitude: Optional[float],
    maximal_latitude: Optional[float],
    minimal_depth: Optional[float],
    maximal_depth: Optional[float],
    vertical_dimension_as_originally_produced: bool,
    start_datetime: Optional[datetime],
    end_datetime: Optional[datetime],
    output_filename: Optional[pathlib.Path],
    force_service: Optional[str],
    request_file: Optional[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    configuration_file_directory: pathlib.Path,
    motu_api_request: Optional[str],
    force_download: bool,
    overwrite_output_data: bool,
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
    log_level: str,
):
    if log_level == "QUIET":
        logging.root.disabled = True
        logging.root.setLevel(level="CRITICAL")
    else:
        logging.root.setLevel(level=log_level)
    subset_request = SubsetRequest()
    if request_file:
        subset_request = subset_request_from_file(request_file)
    if motu_api_request:
        motu_api_subset_request = convert_motu_api_request_to_structure(
            motu_api_request
        )
        subset_request.update(motu_api_subset_request.__dict__)
    request_update_dict = {
        "dataset_url": dataset_url,
        "dataset_id": dataset_id,
        "variables": variables,
        "minimal_longitude": minimal_longitude,
        "maximal_longitude": maximal_longitude,
        "minimal_latitude": minimal_latitude,
        "maximal_latitude": maximal_latitude,
        "minimal_depth": minimal_depth,
        "maximal_depth": maximal_depth,
        "vertical_dimension_as_originally_produced": vertical_dimension_as_originally_produced,  # noqa
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "output_filename": output_filename,
        "force_service": force_service,
        "output_directory": output_directory,
    }
    subset_request.update(request_update_dict)
    if all(
        e is None
        for e in [
            subset_request.variables,
            subset_request.minimal_longitude,
            subset_request.maximal_longitude,
            subset_request.minimal_latitude,
            subset_request.maximal_latitude,
            subset_request.minimal_depth,
            subset_request.maximal_depth,
            subset_request.start_datetime,
            subset_request.end_datetime,
        ]
    ):
        logging.error(
            "The requested dataset is not subset, "
            "please use the 'get' command instead."
        )
        sys.exit(1)
    # Specific treatment for default values:
    # In order to not overload arguments with default values
    if force_download:
        subset_request.force_download = force_download
    if overwrite_output_data:
        subset_request.overwrite_output_data = overwrite_output_data

    subset_function(
        username,
        password,
        subset_request,
        configuration_file_directory,
        overwrite_metadata_cache,
        no_metadata_cache,
    )


def subset_function(
    username: Optional[str],
    password: Optional[str],
    subset_request: SubsetRequest,
    configuration_file_directory: pathlib.Path,
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
):
    catalogue = parse_catalogue(overwrite_metadata_cache, no_metadata_cache)
    dataset_service = get_dataset_service(
        catalogue,
        subset_request.dataset_id,
        subset_request.dataset_url,
        subset_request.force_service,
        CommandType.SUBSET,
        subset_request,
    )
    username, password = get_username_password(
        username,
        password,
        configuration_file_directory,
    )
    subset_request.dataset_url = dataset_service.uri
    logging.info(
        "Downloading using service "
        f"{dataset_service.service_type.service_name.value}..."
    )
    if dataset_service.service_type in [
        CopernicusMarineDatasetServiceType.GEOSERIES,
        CopernicusMarineDatasetServiceType.TIMESERIES,
    ]:
        download_zarr(
            username,
            password,
            subset_request,
        )
    elif (
        dataset_service.service_type
        == CopernicusMarineDatasetServiceType.OPENDAP
    ):
        download_opendap(
            username,
            password,
            subset_request,
        )
    elif (
        dataset_service.service_type == CopernicusMarineDatasetServiceType.MOTU
    ):
        download_motu(
            username,
            password,
            subset_request,
            catalogue=catalogue,
        )
