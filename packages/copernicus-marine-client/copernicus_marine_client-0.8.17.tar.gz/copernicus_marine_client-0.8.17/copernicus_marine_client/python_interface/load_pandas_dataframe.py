import pathlib
from datetime import datetime
from typing import List, Optional

import pandas

from copernicus_marine_client.catalogue_parser.request_structure import (
    LoadRequest,
)
from copernicus_marine_client.core_functions.utils import (
    DEFAULT_CLIENT_BASE_DIRECTORY,
)
from copernicus_marine_client.download_functions.download_arco_series import (
    load_pandas_dataframe_from_arco_series,
)
from copernicus_marine_client.download_functions.download_opendap import (
    load_pandas_dataframe_from_opendap,
)
from copernicus_marine_client.download_functions.subset_parameters import (
    DepthParameters,
    GeographicalParameters,
    LatitudeParameters,
    LongitudeParameters,
    TemporalParameters,
)
from copernicus_marine_client.python_interface.load_utils import (
    load_data_object_from_load_request,
)


def load_pandas_dataframe(
    dataset_url: Optional[str] = None,
    dataset_id: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    variables: Optional[List[str]] = None,
    minimal_longitude: Optional[float] = None,
    maximal_longitude: Optional[float] = None,
    minimal_latitude: Optional[float] = None,
    maximal_latitude: Optional[float] = None,
    minimal_depth: Optional[float] = None,
    maximal_depth: Optional[float] = None,
    vertical_dimension_as_originally_produced: bool = False,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    force_service: Optional[str] = None,
    credentials_file: pathlib.Path = DEFAULT_CLIENT_BASE_DIRECTORY,
    overwrite_metadata_cache: bool = False,
    no_metadata_cache: bool = False,
) -> pandas.DataFrame:
    load_request = LoadRequest(
        dataset_url=dataset_url,
        dataset_id=dataset_id,
        username=username,
        password=password,
        variables=variables,
        geographical_parameters=GeographicalParameters(
            latitude_parameters=LatitudeParameters(
                minimal_latitude=minimal_latitude,
                maximal_latitude=maximal_latitude,
            ),
            longitude_parameters=LongitudeParameters(
                minimal_longitude=minimal_longitude,
                maximal_longitude=maximal_longitude,
            ),
        ),
        temporal_parameters=TemporalParameters(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        ),
        depth_parameters=DepthParameters(
            minimal_depth=minimal_depth,
            maximal_depth=maximal_depth,
            vertical_dimension_as_originally_produced=vertical_dimension_as_originally_produced,  # noqa
        ),
        force_service=force_service,
        credentials_file=credentials_file,
        overwrite_metadata_cache=overwrite_metadata_cache,
        no_metadata_cache=no_metadata_cache,
    )
    dataset = load_data_object_from_load_request(
        load_request,
        load_pandas_dataframe_from_arco_series,
        load_pandas_dataframe_from_opendap,
    )
    return dataset
