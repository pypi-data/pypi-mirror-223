import json
from typing import Any

from copernicus_marine_client.core_functions.describe import describe_function


def describe(
    include_description: bool = False,
    include_datasets: bool = False,
    include_keywords: bool = False,
    contains: list[str] = [],
    overwrite_metadata_cache: bool = False,
    no_metadata_cache: bool = False,
) -> dict[str, Any]:
    catalogue_json = describe_function(
        include_description,
        include_datasets,
        include_keywords,
        contains,
        overwrite_metadata_cache,
        no_metadata_cache,
    )
    catalogue = json.loads(catalogue_json)
    return catalogue
