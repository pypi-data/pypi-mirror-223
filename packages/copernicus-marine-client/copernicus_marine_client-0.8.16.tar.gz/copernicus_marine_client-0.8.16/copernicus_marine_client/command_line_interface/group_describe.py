import logging
import logging.config
from json import dumps

import click

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineCatalogue,
    filter_catalogue_with_strings,
    parse_catalogue,
)
from copernicus_marine_client.command_line_interface.utils import (
    MutuallyExclusiveOption,
)


@click.group()
def cli_group_describe() -> None:
    pass


@cli_group_describe.command(
    "describe",
    short_help="Print Copernicus Marine catalog as JSON",
    help="""
    Print Copernicus Marine catalog as JSON.

    The default display contains information on the products, and more data
    can be displayed using the --include-<argument> flags.

    The --contains option allows the user to specify one or several strings to
    filter through the catalogue display. The search is performed recursively
    on all attributes of the catalogue, and the tokens only need to be
    contained in one of the attributes (i.e. not exact match).
    """,
    epilog="""
    Examples:

    \b
    copernicus-marine describe --contains METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 --include-datasets

    \b
    copernicus-marine describe -c METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
    """,  # noqa
)
@click.option(
    "--include-description",
    type=bool,
    is_flag=True,
    default=False,
    help="Include product description in output.",
)
@click.option(
    "--include-datasets",
    type=bool,
    is_flag=True,
    default=False,
    help="Include product dataset details in output.",
)
@click.option(
    "--include-keywords",
    type=bool,
    is_flag=True,
    default=False,
    help="Include product keyword details in output.",
)
@click.option(
    "--contains",
    "-c",
    type=str,
    multiple=True,
    help="Filter catalogue output. Returns products with attributes"
    "matching a string token.",
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
def describe(
    include_description: bool,
    include_datasets: bool,
    include_keywords: bool,
    contains: list[str],
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
    log_level: str,
) -> None:
    if log_level == "QUIET":
        logging.root.disabled = True
        logging.root.setLevel(level="CRITICAL")
    else:
        logging.root.setLevel(level=log_level)

    base_catalogue: CopernicusMarineCatalogue = parse_catalogue(
        overwrite_metadata_cache=overwrite_metadata_cache,
        no_metadata_cache=no_metadata_cache,
    )

    catalogue_dict = (
        filter_catalogue_with_strings(base_catalogue, contains)
        if contains
        else base_catalogue
    )

    def default_filter(obj):
        attributes = obj.__dict__
        attributes.pop("_name_", None)
        attributes.pop("_value_", None)
        attributes.pop("__objclass__", None)
        if not include_description:
            attributes.pop("description", None)
        if not include_datasets:
            attributes.pop("datasets", None)
        if not include_keywords:
            attributes.pop("keywords", None)
        return obj.__dict__

    json_dump = dumps(
        catalogue_dict, default=default_filter, sort_keys=False, indent=2
    )
    logger = logging.getLogger("blank_logger")
    logger.warn(json_dump)


if __name__ == "__main__":
    cli_group_describe()
