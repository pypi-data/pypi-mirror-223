from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LatitudeParameters:
    minimal_latitude: Optional[float]
    maximal_latitude: Optional[float]


@dataclass
class LongitudeParameters:
    minimal_longitude: Optional[float]
    maximal_longitude: Optional[float]


@dataclass
class GeographicalParameters:
    latitude_parameters: LatitudeParameters
    longitude_parameters: LongitudeParameters


@dataclass
class TemporalParameters:
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]


@dataclass
class DepthParameters:
    minimal_depth: Optional[float]
    maximal_depth: Optional[float]
    vertical_dimension_as_originally_produced: bool = True
