from __future__ import annotations

import itertools
import typing
from collections.abc import Set
from dataclasses import dataclass
from typing import TypedDict, Required, Callable, Iterable, Generic, Mapping

import pandas as pd

from mdata.core import df_utils
from mdata.core.shared_defs import ObservationType, ObservationSpecLabel, ObservationSpecIdentifier, ObservationTypes, \
    ObservationTypeValue, MDConcepts, only_feature_columns
from mdata.core.extensions import metadata, Extension
from mdata.core.header import ObservationSpec, Meta
from mdata.core.base_machine_data import EventTimeseriesContainer, BaseMachineData, MeasurementTimeseriesContainer, \
    EventTimeseriesSpec, \
    MeasurementTimeseriesSpec, EventTimeseriesView, MeasurementTimeseriesView
from mdata.core.protocols import TSSpec, ETSC, MTSC, MachineData, \
    MachineDataProtocol, TSContainer, ETSView, ETSSpec, MTSView, MTSSpec
from mdata.core.raw import create_machine_data_from_raw, RawHeaderSpec, FeatureMetadata

md_columns_def = {MDConcepts.Object: str, MDConcepts.Time: str,
                  MDConcepts.Label: str, MDConcepts.Time + '_col': str, MDConcepts.Object + '_col': str,
                  MDConcepts.Type + '_col': str, MDConcepts.Label + '_col': str}
MDColumnsDef = TypedDict('MDColumnsDef', md_columns_def)
ObservationSeriesDef = TypedDict('ObservationSeriesDef',
                                 {'df': Required[pd.DataFrame],
                                  'feature_metadata': Mapping[str, FeatureMetadata]} | md_columns_def,
                                 total=False)


def define_observation_specs_by_groupby(df: pd.DataFrame, key: str | list[str],
                                        func: Callable[[pd.DataFrame], ObservationSeriesDef] = lambda
                                                df: ObservationSeriesDef(df=df)):
    return (func(df.loc[idx]) for idx in df.groupby(by=key).groups.values())


def machine_data_from_complete_df(df: pd.DataFrame, header: RawHeaderSpec) -> BaseMachineData:
    return create_machine_data_from_raw(df, header)


def prepare_observations_df(df: pd.DataFrame, copy=False, sort_by_time=False, **kwargs: MDColumnsDef) -> tuple[
    pd.DataFrame, ObservationSpecIdentifier]:
    df = df.copy() if copy else df

    def match_def_and_df(concept, col_idx, fallback=None) -> str:
        concept_def = None
        if concept + '_col' in kwargs:
            assert concept not in kwargs
            col = kwargs.get(concept + '_col')
            concept_def = df[col]
            if concept == MDConcepts.Time:
                concept_def = pd.to_datetime(concept_def, format='ISO8601')
        elif concept in kwargs:
            assert concept + '_col' not in kwargs
            concept_def = kwargs.get(concept)
            if concept == MDConcepts.Time and concept_def == 'artificial':
                concept_def = fallback()
        if concept_def is not None:
            assert concept not in df.columns
            df.insert(col_idx, concept, concept_def)
        elif len(df) > 0:
            concept_def = str(df.iloc[0][concept])
        return concept_def

    time_def = match_def_and_df(MDConcepts.Time, 0, fallback=lambda: df_utils.create_artificial_daterange(df))
    object_def = match_def_and_df(MDConcepts.Object, 1)
    type_def = match_def_and_df(MDConcepts.Type, 2)
    label_def = match_def_and_df(MDConcepts.Label, 3)
    assert time_def is not None
    assert object_def is not None
    assert type_def is not None
    assert label_def is not None

    # assert isinstance(type_def, ObservationTypeValue)
    type_def = typing.cast(ObservationTypeValue, type_def)

    if sort_by_time:
        df.sort_values(MDConcepts.Time, inplace=True)

    return df, (type_def, label_def)


@dataclass
class Factory(Generic[ETSSpec, ETSView, ETSC, MTSSpec, MTSView, MTSC, MachineData]):
    ets_spec_cls: type[ETSSpec]
    ets_view_cls: type[ETSView]
    ets_cont_cls: type[ETSC]
    mts_spec_cls: type[MTSSpec]
    mts_view_cls: type[MTSView]
    mts_cont_cls: type[MTSC]
    md_cls: type[MachineDataProtocol[ETSSpec, ETSView, ETSC, MTSSpec, MTSView, MTSC]]

    def __post_init__(self):
        self.ets_spec_factory: TimeseriesSpecFactory[ETSSpec] = TimeseriesSpecFactory.for_cls(ObservationType.E,
                                                                                              self.ets_spec_cls)
        self.mts_spec_factory: TimeseriesSpecFactory[MTSSpec] = TimeseriesSpecFactory.for_cls(ObservationType.M,
                                                                                              self.mts_spec_cls)
        self.ets_cont_factory: TimeseriesContainerFactory[ETSC] = TimeseriesContainerFactory.for_cls(self.ets_cont_cls)
        self.mts_cont_factory: TimeseriesContainerFactory[MTSC] = TimeseriesContainerFactory.for_cls(self.mts_cont_cls)
        self.md_factory: MachineDataFactory[
            MachineDataProtocol[ETSSpec, ETSView, ETSC, MTSSpec, MTSView, MTSC]] = MachineDataFactory.for_cls(
            self.md_cls)

    def make_ts_spec(self, spec_id: ObservationSpecIdentifier, base_spec: ObservationSpec) -> ETSSpec | MTSSpec:
        observation_type, observation_label = spec_id
        match observation_type:
            case ObservationTypes.E:
                return self.ets_spec_factory.make(observation_label, base_spec)
            case ObservationTypes.M:
                return self.mts_spec_factory.make(observation_label, base_spec)

    def make_ts_spec_from_data(self, spec_id: ObservationSpecIdentifier, df: pd.DataFrame,
                               extra_metadata: typing.Mapping[str, FeatureMetadata]) -> ETSSpec | MTSSpec:
        features = only_feature_columns(df.columns)
        base_spec = ObservationSpec.from_raw(
            [({f: extra_metadata[f]} if (extra_metadata and f in extra_metadata) else f) for f in features])
        return self.make_ts_spec(spec_id, base_spec)

    def make_ts_container(self, ts_spec: ETSSpec | MTSSpec, df: pd.DataFrame, copy=False,
                          convert_dtypes=False) -> ETSC | MTSC:
        if convert_dtypes:
            df = metadata.convert_df(df, {f.name: f.data_type for f in ts_spec.base}, inplace=not copy)
        elif copy:
            df = df.copy()
        match ts_spec.observation_type:
            case ObservationType.E:
                return self.ets_cont_factory.make(ts_spec, df)
            case ObservationType.M:
                return self.mts_cont_factory.make(ts_spec, df)

    def make_ts_container_from_data(self, series_def: ObservationSeriesDef, copy=False, convert_dtypes=False,
                                    sort_by_time=False) -> ETSC | MTSC:
        df, spec_id = prepare_observations_df(copy=copy, sort_by_time=sort_by_time, **series_def)
        ts_spec = self.make_ts_spec_from_data(spec_id, df, extra_metadata=series_def.get('feature_metadata'))
        return self.make_ts_container(ts_spec, df, copy=False, convert_dtypes=convert_dtypes)

    def make_from_data(self, *series_defs: ObservationSeriesDef, meta: Meta = Meta(), sort_by_time=True, copy_dfs=False,
                       convert_dtypes=False) -> MachineDataProtocol[ETSSpec, ETSView, ETSC, MTSSpec, MTSView, MTSC]:
        events, measurements = [], []
        for sd in series_defs:
            sd: ObservationSeriesDef
            tsc = self.make_ts_container_from_data(sd, copy=copy_dfs, convert_dtypes=convert_dtypes,
                                                   sort_by_time=sort_by_time)
            match tsc.observation_type:
                case ObservationType.E:
                    events.append(tsc)
                case ObservationType.M:
                    measurements.append(tsc)

        return self.make(meta=meta, events=events, measurements=measurements, lazy=False)

    def make(self, meta: Meta = Meta(), events: Iterable[ETSC] = (), measurements: Iterable[MTSC] = (),
             series_containers: Iterable[ETSC | MTSC] = (), lazy=False, index_frame: pd.DataFrame = None,
             **kwargs) -> MachineDataProtocol[ETSSpec, ETSView, ETSC, MTSSpec, MTSView, MTSC]:
        series_containers = list(series_containers)
        events = itertools.chain(events,
                                 (tsc for tsc in series_containers if tsc.observation_type == ObservationType.E))
        measurements = itertools.chain(measurements,
                                       (tsc for tsc in series_containers if tsc.observation_type == ObservationType.M))
        return self.md_factory.make(meta=meta, events=events, measurements=measurements, lazy=lazy,
                                    index_frame=index_frame, **kwargs)


class TimeseriesSpecFactory(Generic[TSSpec]):
    constructors = {ObservationType.E: {EventTimeseriesSpec: EventTimeseriesSpec.of},
                    ObservationType.M: {MeasurementTimeseriesSpec:
                                            MeasurementTimeseriesSpec.of}}

    def __init__(self, observation_type: ObservationType, ts_spec_cls: type[TSSpec] = None) -> None:
        ts_spec_cls = typing.get_args(self.__class__)[0] if ts_spec_cls is None else ts_spec_cls
        self.constr: Callable[[ObservationSpecLabel, ObservationSpec], TSSpec] = self.constructors[observation_type][
            ts_spec_cls]
        self.__call__ = self.make

    def make(self, label: ObservationSpecLabel, base_spec: ObservationSpec) -> TSSpec:
        return self.constr(label, base_spec)

    @classmethod
    def for_cls(cls, observation_type: ObservationType, ts_spec_cls: type[TSSpec]) -> TimeseriesSpecFactory[TSSpec]:
        v: TimeseriesSpecFactory[TSSpec] = cls[ts_spec_cls](observation_type, ts_spec_cls)
        return v


class TimeseriesContainerFactory(Generic[TSContainer]):
    constructors = {EventTimeseriesContainer: EventTimeseriesContainer,
                    MeasurementTimeseriesContainer: MeasurementTimeseriesContainer}

    def __init__(self, ts_cont_cls: type[TSContainer]):
        self.constr = self.constructors[ts_cont_cls]
        self.__call__ = self.make

    def make(self, ts_spec: TSSpec, df: pd.DataFrame) -> TSContainer:
        return self.constr(ts_spec, df)

    @classmethod
    def for_cls(cls, ts_cont_cls: type[TSContainer]) -> TimeseriesContainerFactory[TSContainer]:
        v: TimeseriesContainerFactory[TSContainer] = cls[ts_cont_cls](ts_cont_cls)
        return v


class MachineDataFactory(Generic[MachineData]):
    constructors = {BaseMachineData: BaseMachineData.of}

    def __init__(self, md_cls: type[MachineData]) -> None:
        self.constr = self.constructors[md_cls]
        self.__call__ = self.make

    def make(self, meta: Meta, events: Iterable[ETSC], measurements: Iterable[MTSC], index_frame: pd.DataFrame = None,
             lazy=True,
             **kwargs) -> MachineData:
        return self.constr(meta=meta, events=events, measurements=measurements, index_frame=index_frame,
                           lazy_map_creation=lazy,
                           lazy_index_creation=lazy, **kwargs)

    @classmethod
    def for_cls(cls, md_cls: type[MachineData]) -> MachineDataFactory[MachineData]:
        v: MachineDataFactory[MachineData] = cls[md_cls](md_cls)
        return v


base_factory = Factory[EventTimeseriesSpec, EventTimeseriesView, EventTimeseriesContainer, MeasurementTimeseriesSpec,
MeasurementTimeseriesView, MeasurementTimeseriesContainer, BaseMachineData](EventTimeseriesSpec,
                                                                            EventTimeseriesView,
                                                                            EventTimeseriesContainer,
                                                                            MeasurementTimeseriesSpec,
                                                                            MeasurementTimeseriesView,
                                                                            MeasurementTimeseriesContainer,
                                                                            BaseMachineData)


def get_factory(extensions: Set[Extension]):
    return base_factory
