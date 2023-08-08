from __future__ import annotations

import typing
from abc import abstractmethod
from collections.abc import Set
from typing import Protocol, Iterable, Sized, Collection, Literal, Mapping, TypeVar, Union

import pandas as pd

from mdata.core.header import ObservationSpec, Meta, Header
from mdata.core.shared_defs import TimeseriesFeatureLabel, TimeseriesFeatureLabels, ObservationTypeValue, \
    ObservationType, ObservationSpecLabel, ObservationSpecIdentifier, EventSpecLabel, MeasurementSpecLabel
from mdata.core.util import SlimMapping, intersection, symmetric_difference

P = typing.ParamSpec('P')


@typing.runtime_checkable
class ObservationTypeSpecific(Protocol):
    # observation_type: ClassVar[ObservationType]
    @property
    @abstractmethod
    def observation_type(self) -> ObservationType: ...


@typing.runtime_checkable
class EventSpecific(Protocol):
    E = ObservationType.E
    observation_type = E


@typing.runtime_checkable
class MeasurementSpecific(Protocol):
    M = ObservationType.M
    observation_type = M


@typing.runtime_checkable
class TimeseriesSpecProtocol(ObservationTypeSpecific, Iterable[str], Sized, Protocol):

    @classmethod
    def of(cls, label: ObservationSpecLabel, base_spec: ObservationSpec) -> typing.Self:
        ...

    @property
    @abstractmethod
    def identifier(self) -> ObservationSpecIdentifier:
        ...

    @property
    @abstractmethod
    def label(self) -> ObservationSpecLabel:
        ...

    @property
    @abstractmethod
    def base(self) -> ObservationSpec:
        ...

    @property
    @abstractmethod
    def features(self) -> TimeseriesFeatureLabels:
        ...

    @property
    @abstractmethod
    def long_names(self) -> TimeseriesFeatureLabels:
        ...

    @abstractmethod
    def feature_intersection(self, other: TimeseriesSpecProtocol) -> list[str]:
        ...

    @abstractmethod
    def feature_symmetric_difference(self, other: TimeseriesSpecProtocol) -> tuple[list[str], list[str]]:
        ...

    @abstractmethod
    def project(self, feature_selection: bool | str | Collection[str]) -> typing.Self: ...

    @abstractmethod
    def is_mergeable(self, other: TimeseriesSpecProtocol) -> bool:
        ...

    @abstractmethod
    def merge(self, other: typing.Self) -> typing.Self:
        ...


TSSpec = TypeVar('TSSpec', bound=TimeseriesSpecProtocol)


class TimeseriesViewProtocol(ObservationTypeSpecific, Protocol[TSSpec]):

    @property
    @abstractmethod
    def timeseries_spec(self) -> TSSpec: ...

    @property
    @abstractmethod
    def df(self) -> pd.DataFrame: ...

    @classmethod
    @abstractmethod
    def of(cls, timeseries_spec: TSSpec, df: pd.DataFrame, *args: P.args, **kwargs: P.kwargs) -> typing.Self: ...

    @property
    @abstractmethod
    def objects(self) -> Set[str]: ...

    @abstractmethod
    def feature_column_view(self, include_time_col=True, include_object_col=False, add_spec_id_prefix=False,
                            use_long_names=False) -> pd.DataFrame: ...


TSView = TypeVar('TSView', bound=TimeseriesViewProtocol)

TSContainer = TypeVar('TSContainer', bound='TimeseriesContainerProtocol')


class TimeseriesContainerProtocol(TimeseriesViewProtocol[TSSpec], SlimMapping[str, TSView],
                                  ObservationTypeSpecific,
                                  Protocol[TSSpec, TSView]):

    @property
    @abstractmethod
    def timeseries_spec(self) -> TSSpec: ...

    @timeseries_spec.setter
    @abstractmethod
    def timeseries_spec(self, value: TSSpec): ...

    @property
    @abstractmethod
    def df(self) -> pd.DataFrame: ...

    @df.setter
    @abstractmethod
    def df(self, value: pd.DataFrame): ...

    @classmethod
    @abstractmethod
    def of(cls, timeseries_spec: TSSpec, df: pd.DataFrame, *args, **kwargs) -> typing.Self:
        ...

    @property
    @abstractmethod
    def observation_count(self) -> int:
        ...

    @property
    @abstractmethod
    def time_series_count(self) -> int:
        ...

    @abstractmethod
    def view(self, *args: P.args, **kwargs: P.kwargs) -> TSView:
        ...

    @abstractmethod
    def merge(self, other: typing.Self,
              axis: Literal['horizontal', 'vertical'] = 'vertical') -> typing.Self:
        ...

    @classmethod
    def lifted_merge(cls, tscs: Mapping[str, TSContainer], o_tscs: Mapping[str, TSContainer],
                     axis: Literal['horizontal', 'vertical'] = 'vertical') -> tuple[dict[str, TSContainer], bool]:
        assert axis in {'horizontal', 'vertical'}
        ov = intersection(tscs.keys(), o_tscs.keys())
        s1, s2 = symmetric_difference(tscs.keys(), o_tscs.keys())
        res = {e: tscs[e] for e in s1} | {e: tscs[e].merge(o_tscs[e], axis=axis) for e in ov} | {e: o_tscs[e] for e in
                                                                                                 s2}
        return res, (axis == 'vertical') | (len(s2) > 0)


ETSSpec = TypeVar('ETSSpec', bound=TimeseriesSpecProtocol, covariant=True)
MTSSpec = TypeVar('MTSSpec', bound=TimeseriesSpecProtocol, covariant=True)
ETSView = TypeVar('ETSView', bound=TimeseriesViewProtocol, covariant=True)
MTSView = TypeVar('MTSView', bound=TimeseriesViewProtocol, covariant=True)
ETSC = TypeVar('ETSC', bound=TimeseriesContainerProtocol, covariant=True)
MTSC = TypeVar('MTSC', bound=TimeseriesContainerProtocol, covariant=True)

MachineData = TypeVar('MachineData', bound='MachineDataProtocol')


class MachineDataProtocol(SlimMapping[ObservationSpecIdentifier, ETSC | MTSC],
                          Protocol[ETSSpec, ETSView, ETSC, MTSSpec, MTSView, MTSC]):
    event_series: Mapping[EventSpecLabel, ETSC]
    measurement_series: Mapping[EventSpecLabel, MTSC]
    meta: Meta

    @abstractmethod
    def __getitem__(self, item: ObservationSpecIdentifier) -> ETSC | MTSC: ...

    # @deprecated
    @classmethod
    @abstractmethod
    def of(cls, meta: Meta = Meta(), events: Iterable[ETSC] = (), measurements: Iterable[MTSC] = (), *args: P.args,
           **kwargs: P.kwargs) -> typing.Self: ...

    @property
    @abstractmethod
    def header(self) -> Header: ...

    @property
    @abstractmethod
    def index_frame(self) -> pd.DataFrame: ...

    @property
    @abstractmethod
    def series_containers(self) -> tuple[Union[ETSC | MTSC], ...]: ...

    @property
    @abstractmethod
    def observation_count(self) -> int: ...

    @property
    @abstractmethod
    def objects(self) -> Set[str]: ...

    @property
    @abstractmethod
    def event_specs(self) -> Mapping[EventSpecLabel, ETSSpec]: ...

    @property
    @abstractmethod
    def measurement_specs(self) -> Mapping[MeasurementSpecLabel, MTSSpec]: ...

    @abstractmethod
    def get_spec(self, identifier: ObservationSpecIdentifier, *args) -> ETSSpec | MTSSpec: ...

    @abstractmethod
    def get_events(self, label: EventSpecLabel) -> ETSC: ...

    @abstractmethod
    def get_measurements(self, label: MeasurementSpecLabel) -> MTSC: ...

    @abstractmethod
    def view_event_series(self, label: EventSpecLabel, *args: P.args, **kwargs: P.kwargs) -> ETSView: ...

    @abstractmethod
    def view_measurement_series(self, label: MeasurementSpecLabel, *args: P.args, **kwargs: P.kwargs) -> MTSView: ...

    @abstractmethod
    def recalculate_index(self, override_categorical_types=True, sort_by_time=True, **kwargs): ...

    @abstractmethod
    def fit_to_data(self, recreate_index=False): ...

    @abstractmethod
    def create_joined_df(self, event_series_labels: Iterable[EventSpecLabel] | bool = None,
                         measurement_series_labels: Iterable[MeasurementSpecLabel] | bool = None,
                         prefix_columns_to_avoid_collisions=True, copy=False) -> pd.DataFrame: ...

    @abstractmethod
    def create_index_view(self, typ: ObservationTypeValue = None, types: Iterable[ObservationTypeValue] = None,
                          obj: str = None, objs: Iterable[str] = None,
                          label: ObservationSpecLabel = None,
                          labels: Iterable[ObservationSpecLabel] = None) -> pd.DataFrame: ...

    @abstractmethod
    def project(self,
                measurement_feature_selection: Mapping[
                    MeasurementSpecLabel, bool | Collection[TimeseriesFeatureLabel]] = None,
                event_feature_selection: Mapping[EventSpecLabel, bool | Collection[TimeseriesFeatureLabel]] = None,
                project_underlying_dfs=False, copy_underlying_dfs=False) -> typing.Self: ...

    @abstractmethod
    def is_mergeable(self, other: MachineDataProtocol) -> bool: ...

    @abstractmethod
    def merge(self, other: MachineData,
              axis: Literal['horizontal', 'vertical'] = 'horizontal') -> MachineData: ...

    @abstractmethod
    def summary(self) -> str: ...
