from __future__ import annotations

from typing import Collection, Literal

import pandas as pd

from mdata.core.util import StringEnumeration

TimeIndexer = bool | pd.Timestamp | Collection[pd.Timestamp] | slice
StrIndexer = bool | str | Collection[str] | slice
TimeseriesFeatureLabel = str
TimeseriesFeatureLabels = tuple[TimeseriesFeatureLabel, ...]
ObservationTypeValue = Literal['E', 'M']


class ObservationTypes(StringEnumeration):
    E: ObservationTypeValue = 'E'
    M: ObservationTypeValue = 'M'


ObservationType = ObservationTypes.derive_enum()
ObservationSpecLabel = str
ObservationSpecIdentifier = tuple[ObservationTypeValue, ObservationSpecLabel]
EventSpecLabel = str
MeasurementSpecLabel = str


class MDConcepts(StringEnumeration):
    Time = 'time'
    Object = 'object'
    Type = 'type'
    Label = 'label'

    base_columns = [Time, Object, Type, Label]


class MDExtensionConcepts(StringEnumeration):
    #Index = 'series_index'

    extension_columns = []
    combined_columns = MDConcepts.base_columns + extension_columns


def only_feature_columns(cols):
    return [c for c in cols if (c not in MDConcepts.base_columns) and (c not in MDExtensionConcepts.extension_columns)]


def project_on_feature_columns(df: pd.DataFrame):
    return df[only_feature_columns(df.columns)]
