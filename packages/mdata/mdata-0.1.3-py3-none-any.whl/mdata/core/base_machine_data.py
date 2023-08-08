from __future__ import annotations

import itertools
import logging
import typing
from abc import ABC
from collections.abc import Iterable, Collection, Mapping, Set, Iterator
from dataclasses import dataclass
from typing import Generic, Literal, Union

import numpy as np
import pandas as pd
from immutabledict import immutabledict

from .shared_defs import StrIndexer, TimeseriesFeatureLabel, TimeseriesFeatureLabels, ObservationTypeValue, \
    ObservationType, ObservationSpecLabel, ObservationSpecIdentifier, EventSpecLabel, MeasurementSpecLabel, \
    ObservationTypes, MDConcepts, only_feature_columns
from .df_utils import derive_categoricals
from .header import Header, ObservationSpec, Meta, FeatureSpec
from .protocols import EventSpecific, MeasurementSpecific, TimeseriesSpecProtocol, TimeseriesViewProtocol, \
    TimeseriesContainerProtocol, MachineDataProtocol, TSSpec, TSView, ETSC, MTSC, \
    ETSView, ETSSpec, MTSView, MTSSpec, TSContainer, MachineData
from .util import mangle_arg_to_set, mangle_arg_with_bool_fallback, mangle_arg_to_tuple, \
    assert_in


class TimeseriesTypeMergeException(Exception):
    pass


class TimeseriesCollectionMergeException(Exception):
    pass


class MachineDataMergeException(Exception):
    pass


@dataclass(frozen=True, unsafe_hash=True, eq=True, repr=False)
class TimeseriesSpec(TimeseriesSpecProtocol):
    observation_type: typing.ClassVar[ObservationType]
    _label: ObservationSpecLabel
    _base: ObservationSpec
    _features: TimeseriesFeatureLabels

    @classmethod
    def of(cls, label: ObservationSpecLabel, base_spec: ObservationSpec) -> typing.Self:
        return cls(label, base_spec, tuple((f.name for f in base_spec)))

    @property
    def type(self) -> ObservationTypeValue:
        return self.observation_type.value

    @property
    def label(self) -> ObservationSpecLabel:
        return self._label

    @property
    def identifier(self) -> ObservationSpecIdentifier:
        return self.type, self.label

    @property
    def base(self) -> ObservationSpec:
        return self._base

    @property
    def features(self) -> TimeseriesFeatureLabels:
        return self._features

    @property
    def long_names(self) -> TimeseriesFeatureLabels:
        return tuple((f.print_name for f in self.base))

    def __iter__(self) -> Iterator[str]:
        return iter(self.features)

    def __len__(self) -> int:
        return len(self.features)

    def __repr__(self):
        extended_feature_labels = tuple(
            (str(f) if f == ln else f'{f} ({ln})') for f, ln in zip(self.features, self.long_names))
        return f'{self.__class__.__name__}(spec_id=({self.observation_type}, {self.label}), features={extended_feature_labels})'

    def __str__(self):
        return self.__repr__()

    def is_mergeable(self, other: TimeseriesSpecProtocol) -> bool:
        return (self.__class__ == other.__class__) and self.identifier == other.identifier

    def feature_intersection(self, other: TimeseriesSpecProtocol) -> list[str]:
        return [f for f in self.features if f in set(other.features)]

    def feature_symmetric_difference(self, other: TimeseriesSpecProtocol) -> tuple[list[str], list[str]]:
        return [f for f in self.features if f not in set(other.features)], [f for f in other.features if
                                                                            f not in set(self.features)]

    def project(self, feature_selection: bool | str | Collection[str]) -> typing.Self:
        feature_selection = mangle_arg_with_bool_fallback(mangle_arg_to_tuple, feature_selection, if_true=self.features)
        assert all(f in self.features for f in feature_selection)
        return self.__class__.of(self.label, ObservationSpec.of(*(self.base[f] for f in feature_selection)))

    def merge(self, other: typing.Self) -> typing.Self:
        assert self.is_mergeable(other)
        specs = list(self.base.features)
        for fspec in other.base:
            if fspec not in self.base:
                specs.append(fspec)
            elif self.base[fspec.name] != fspec:
                print('redefined', self.base, self.base[fspec.name], fspec.name)
                raise TimeseriesTypeMergeException
        return self.__class__.of(self.label, ObservationSpec.of(*specs))


# @dataclass(frozen=True, repr=False)
class EventTimeseriesSpec(TimeseriesSpec, EventSpecific):
    observation_type = ObservationType.E


# @dataclass(frozen=True, repr=False)
class MeasurementTimeseriesSpec(TimeseriesSpec, MeasurementSpecific):
    observation_type = ObservationType.M


class TimeseriesView(TimeseriesViewProtocol[TSSpec], Generic[TSSpec]):

    def __init__(self, timeseries_spec: TSSpec, df: pd.DataFrame, objects: Collection[str] = None) -> None:
        super().__init__()
        self._timeseries_spec: TSSpec = timeseries_spec
        self._df = df
        self._objects = frozenset(objects) if objects is not None else frozenset()

    @property
    def observation_type(self) -> ObservationTypeValue:
        return self.timeseries_spec.observation_type

    @property
    def timeseries_spec(self) -> TSSpec:
        return self._timeseries_spec

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def feature_column_view(self, include_time_col=True, include_object_col=False, add_spec_id_prefix=False,
                            use_long_names=False) -> pd.DataFrame:
        return _feature_column_view(self.timeseries_spec, self.df, include_time_col=include_time_col,
                                    include_object_col=include_object_col, add_spec_id_prefix=add_spec_id_prefix,
                                    use_long_names=use_long_names)

    @classmethod
    def of(cls, timeseries_spec: TSSpec, df: pd.DataFrame, objects: Collection[str] = None, *args,
           **kwargs) -> typing.Self:
        c = cls(timeseries_spec, df, objects)
        return c

    @property
    def objects(self) -> Set[str]:
        return self._objects

    def __repr__(self):
        return f'{self.__class__.__name__}(spec={self.timeseries_spec}, #observations={len(self.df)}, objects={str(self.objects)})'

    def __str__(self):
        return repr(self)


cl = TimeseriesView[EventTimeseriesSpec]


class EventTimeseriesView(TimeseriesView[EventTimeseriesSpec]):

    def __init__(self, timeseries_spec: EventTimeseriesSpec, df: pd.DataFrame, objects: Collection[str] = None) -> None:
        super().__init__(timeseries_spec, df, objects)


class MeasurementTimeseriesView(TimeseriesView[MeasurementTimeseriesSpec]):

    def __init__(self, timeseries_spec: MeasurementTimeseriesSpec, df: pd.DataFrame,
                 objects: Collection[str] = None) -> None:
        super().__init__(timeseries_spec, df, objects)


def _feature_column_view(spec, df, include_time_col=True, include_object_col=False, add_spec_id_prefix=False,
                         use_long_names=False):
    cols = list(spec.features)
    if include_object_col:
        cols = [MDConcepts.Object] + cols
    if include_time_col:
        cols = [MDConcepts.Time] + cols

    view = df.loc[:, cols]

    renaming = {}

    def maybe_prefix(c):
        if add_spec_id_prefix:
            return spec.type + '_' + spec.label + '_' + c
        else:
            return c

    if use_long_names | add_spec_id_prefix:
        if use_long_names:
            renaming = {f: maybe_prefix(ln) for f, ln in
                        zip(spec.features, spec.long_names)}
        else:
            renaming = {f: maybe_prefix(f) for f in spec.features}

    return view.rename(renaming, inplace=False, axis='columns') if renaming else view


class AbstractTimeseriesContainer(TimeseriesContainerProtocol[TSSpec, TSView], Generic[TSSpec, TSView], ABC):
    _ts_spec_cls: type[TSSpec] = None
    _ts_view_cls: type[TSView] = None

    def __init__(self, timeseries_spec: TSSpec, df: pd.DataFrame) -> None:
        super().__init__()
        assert isinstance(timeseries_spec, self._ts_spec_cls)
        self.timeseries_spec = timeseries_spec
        self.df = df

        self._internal_index = None
        self._object_map: Mapping[str, TSView] = {}
        self._repopulate_internal_index()

    @property
    def observation_type(self) -> ObservationType:
        return self.timeseries_spec.observation_type

    @property
    def timeseries_spec(self) -> TSSpec:
        return self._timeseries_spec

    @timeseries_spec.setter
    def timeseries_spec(self, value: TSSpec):
        self._timeseries_spec = value

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, value: pd.DataFrame):
        self._df = value

    @classmethod
    def of(cls, timeseries_spec: TSSpec, df: pd.DataFrame, *args, **kwargs) -> typing.Self:
        return cls(timeseries_spec, df)

    @property
    def objects(self) -> Set[str]:
        return self._object_map.keys()

    @property
    def observation_count(self) -> int:
        return len(self.df)

    @property
    def time_series_count(self) -> int:
        return len(self.objects)

    def __contains__(self, item) -> bool:
        return item in self._object_map

    def __getitem__(self, item: str) -> TSView:
        return self._object_map[item]

    def __len__(self) -> int:
        return len(self.objects)

    def __iter__(self) -> Iterator[TSView]:
        return iter(self._object_map.values())

    def __str__(self):
        return f'{self.__class__.__name__}(spec={self.timeseries_spec}, #obs={self.observation_count}, #objects={len(self.objects)})'

    def __repr__(self) -> str:
        return str(self)

    def feature_column_view(self, include_time_col=True, include_object_col=False, add_spec_id_prefix=False,
                            use_long_names=False) -> pd.DataFrame:
        return _feature_column_view(self.timeseries_spec, self.df, include_time_col=include_time_col,
                                    include_object_col=include_object_col, add_spec_id_prefix=add_spec_id_prefix,
                                    use_long_names=use_long_names)

    def view(self, objs: StrIndexer) -> TSView:
        if not objs:
            objs = []
        elif objs is True:
            objs = slice(None)
        return self._mk_timeseries_view(self.timeseries_spec, objs)

    def merge(self, other: typing.Self,
              axis: Literal['horizontal', 'vertical'] = 'vertical') -> typing.Self:
        assert axis in {'horizontal', 'vertical'}
        if axis == 'horizontal':
            assert self.timeseries_spec.is_mergeable(other.timeseries_spec)
            ov = self.timeseries_spec.feature_intersection(other.timeseries_spec)
            if ov:
                assert self.df.loc[:, ov].equals(
                    other.df.loc[:, ov])  # np.array_equal(self.df.loc[:, ov].values, other.df.loc[:, ov].values)
            _, new_fs = self.timeseries_spec.feature_symmetric_difference(other.timeseries_spec)
            if new_fs:
                assert self.df[MDConcepts.Time].equals(other.df[MDConcepts.Time])
                df = pd.concat([self.df, other.df.loc[:, new_fs]], axis='columns', copy=True)
                return self.__class__(self.timeseries_spec.merge(other.timeseries_spec), df)
            return self
        elif axis == 'vertical':
            assert self.timeseries_spec == other.timeseries_spec
            df = pd.concat([self.df, other.df], axis='index', ignore_index=True, copy=True)
            df.sort_values(MDConcepts.Time, ignore_index=True, inplace=True)
            return self.__class__(self.timeseries_spec, df)

    def _repopulate_internal_index(self):
        self._internal_index = pd.Series(self.df.index, index=self.df[MDConcepts.Object])
        self._object_map: dict[str, TSView] = {obj: self.view(obj) for obj in self._internal_index.index.unique()}

    def _check_ts_features(self):
        return set(self.timeseries_spec.features) <= set(self.df.columns)

    def _mk_timeseries_view(self, timeseries_spec, objs) -> TSView:
        df = self.df.loc[self._internal_index.loc[objs]]
        return self._ts_view_cls(timeseries_spec, df, objects=set(df[MDConcepts.Object]))

    def _update_timeseries_spec(self, timeseries_spec: TSSpec = None) -> None:
        self.timeseries_spec = self._derive_timeseries_spec() if timeseries_spec is None else timeseries_spec
        assert self._check_ts_features()

    def _derive_timeseries_spec(self) -> TSSpec:
        current_features = only_feature_columns(self.df.columns)
        from .extensions import metadata

        specs: list[FeatureSpec] = []
        for f in current_features:
            fdt = metadata.get_type(self.df.loc[:, f])
            long_name = f
            if f in self.timeseries_spec.base:
                fspec: FeatureSpec = self.timeseries_spec.base[f]
                long_name = fspec.print_name
            specs.append(FeatureSpec(f, long_name, fdt))

        return self._ts_spec_cls(self.timeseries_spec.label, ObservationSpec(*specs))

    def update_index(self):
        self._repopulate_internal_index()

    def fit_to_data(self) -> None:
        self._update_timeseries_spec()
        self.update_index()


class EventTimeseriesContainer(AbstractTimeseriesContainer[EventTimeseriesSpec, EventTimeseriesView]):
    _ts_spec_cls = EventTimeseriesSpec
    _ts_view_cls = EventTimeseriesView


class MeasurementTimeseriesContainer(AbstractTimeseriesContainer[MeasurementTimeseriesSpec, MeasurementTimeseriesView]):
    _ts_spec_cls = MeasurementTimeseriesSpec
    _ts_view_cls = MeasurementTimeseriesView


class AbstractMachineData(MachineDataProtocol[ETSSpec, ETSView, ETSC, MTSSpec, MTSView, MTSC], ABC):
    _etsc_cls: type[ETSC] = None
    _mtsc_cls: type[MTSC] = None

    def __init__(self, meta: Meta, events: Iterable[ETSC],
                 measurements: Iterable[MTSC],
                 index_frame: pd.DataFrame = None) -> None:

        self.meta: Meta = meta
        self.event_series: Mapping[EventSpecLabel, ETSC] = immutabledict(
            {etc.timeseries_spec.label: etc for etc in events})
        self.measurement_series: Mapping[MeasurementSpecLabel, MTSC] = immutabledict(
            {mtc.timeseries_spec.label: mtc for mtc in
             measurements})

        for etsc in self.event_series.values():
            assert isinstance(etsc, self._etsc_cls)
        for mtsc in self.measurement_series.values():
            assert isinstance(mtsc, self._mtsc_cls)

        # derived fields/maps
        self._event_specs = None
        self._measurement_specs = None
        self._index_frame: pd.DataFrame = index_frame
        self._objects = None
        self._series_containers: typing.Optional[tuple[typing.Union[ETSC | MTSC], ...]] = tuple(
            itertools.chain(self.event_series.values(), self.measurement_series.values()))

    @classmethod
    def of(cls, meta: Meta = Meta(), events: Iterable[ETSC] = (),
           measurements: Iterable[MTSC] = (), lazy_index_creation=False, lazy_map_creation=True,
           *args,
           **kwargs) -> typing.Self:
        md = cls(meta, events, measurements, **kwargs)
        if not lazy_index_creation:
            md.recalculate_index()
        if not lazy_map_creation:
            md._repopulate_maps()
        return md

    @property
    def header(self) -> Header:
        return Header(self.meta, {e: tspec.base for e, tspec in self.event_specs.items()},
                      {m: tspec.base for m, tspec in self.measurement_specs.items()})

    @property
    def index_frame(self) -> pd.DataFrame:
        if self._index_frame is None:
            self.recalculate_index()
        return self._index_frame

    @index_frame.setter
    def index_frame(self, value: pd.DataFrame):
        self._index_frame = value

    @property
    def objects(self) -> Set[str]:
        if self._objects is None:
            self._repopulate_maps()
        return self._objects

    @property
    def observation_count(self) -> int:
        return len(self.index_frame)

    @property
    def series_containers(self) -> tuple[Union[ETSC | MTSC], ...]:
        if self._series_containers is None:
            self._repopulate_maps()
        return self._series_containers

    @property
    def event_specs(self) -> Mapping[EventSpecLabel, ETSSpec]:
        if self._event_specs is None:
            self._repopulate_maps()
        return self._event_specs

    @property
    def measurement_specs(self) -> Mapping[MeasurementSpecLabel, MTSSpec]:
        if self._measurement_specs is None:
            self._repopulate_maps()
        return self._measurement_specs

    def __getitem__(self, item: ObservationSpecIdentifier) -> ETSC | MTSC:
        t, label = item
        match t:
            case ObservationTypes.E:
                return self.event_series[label]
            case ObservationTypes.M:
                return self.measurement_series[label]
            case _:
                raise KeyError

    def __contains__(self, item: object) -> bool:
        if not isinstance(item, tuple):
            return False
        try:
            self[item]
        except KeyError:
            return False
        return True

    def __len__(self) -> int:
        return len(self.series_containers)

    def __iter__(self) -> Iterator[ETSC | MTSC]:
        return iter(self.series_containers)

    def get_spec(self, identifier: ObservationSpecIdentifier, *args) -> ETSSpec | MTSSpec:
        if len(args) > 0:
            t, label = identifier, args[0]
        else:
            t, label = identifier
        match t:
            case ObservationTypes.E:
                return self.event_specs[label]
            case ObservationTypes.M:
                return self.measurement_specs[label]
            case _:
                raise KeyError

    def get_events(self, label: EventSpecLabel) -> ETSC:
        return self.event_series[label]

    def get_measurements(self, label: MeasurementSpecLabel) -> MTSC:
        return self.measurement_series[label]

    def view_event_series(self, label: EventSpecLabel, objs: StrIndexer = slice(None), *args,
                          **kwargs) -> ETSView:
        return self.event_series[label].view(objs=objs, **kwargs)

    def view_measurement_series(self, label: MeasurementSpecLabel, objs: StrIndexer = slice(None), *args,
                                **kwargs) -> MTSView:
        return self.measurement_series[label].view(objs=objs, **kwargs)

    def recalculate_index(self, override_categorical_types=True, sort_by_time=True, **kwargs):
        self._index_frame = build_shared_index(self.series_containers,
                                               override_categorical_types=override_categorical_types,
                                               sort_by_time=sort_by_time, **kwargs)

    def _repopulate_maps(self):
        self._series_containers = tuple(self.event_series.values()) + tuple(self.measurement_series.values())
        self._event_specs = immutabledict({es.timeseries_spec.label: es.timeseries_spec for es in
                                           self.event_series.values()})
        self._measurement_specs = immutabledict({ms.timeseries_spec.label: ms.timeseries_spec for ms in
                                                 self.measurement_series.values()})
        self._objects = frozenset(self.index_frame[MDConcepts.Object])

    def fit_to_data(self, ignore_index=False):
        for tsc in self.series_containers:
            # retain only the rows that are referenced in the overall index
            if not ignore_index:
                tsc.df = tsc.df.filter(items=self.index_frame.index, axis=0)
            tsc.fit_to_data()

        if ignore_index:
            self.recalculate_index()
        else:
            old_index = self.index_frame.index
            mask = pd.Series(False, index=old_index)
            for tsc in self.series_containers:
                mask |= old_index.isin(tsc.df.index)
            self._index_frame = self.index_frame[mask]

    def create_joined_df(self, event_series_labels: Iterable[EventSpecLabel] | bool = None,
                         measurement_series_labels: Iterable[MeasurementSpecLabel] | bool = None,
                         prefix_columns_to_avoid_collisions=True, copy=False):
        event_keys = self.event_specs.keys()
        esl = mangle_arg_with_bool_fallback(mangle_arg_to_tuple, event_series_labels,
                                            if_true=event_keys,
                                            rm_duplicates=True, preserve_order=True)
        assert_in(esl, event_keys)
        measurement_keys = self.measurement_specs.keys()
        msl = mangle_arg_with_bool_fallback(mangle_arg_to_tuple, measurement_series_labels,
                                            if_true=measurement_keys,
                                            rm_duplicates=True, preserve_order=True)
        assert_in(msl, measurement_keys)
        it: Iterable[ETSC | MTSC] = itertools.chain((self.event_series[e] for e in esl),
                                                    (self.measurement_series[m] for m in msl))
        return pd.concat([self.index_frame] + [
            tsc.feature_column_view(add_spec_id_prefix=prefix_columns_to_avoid_collisions, include_time_col=False,
                                    include_object_col=False) for
            tsc in it], axis='columns', copy=copy)

    def create_index_view(self, typ: ObservationTypeValue = None, types: Iterable[ObservationTypeValue] = None,
                          obj: str = None, objs: Iterable[str] = None,
                          label: ObservationSpecLabel = None,
                          labels: Iterable[ObservationSpecLabel] = None) -> pd.DataFrame:
        assert typ is None or types is None
        assert obj is None or objs is None
        assert label is None or labels is None

        mask = pd.Series(True, index=self.index_frame.index)
        if obj is not None:
            mask &= (self.index_frame[MDConcepts.Object] == obj)
        elif objs is not None:
            mask &= (self.index_frame[MDConcepts.Object].isin(mangle_arg_to_set(objs)))
        if label is not None:
            mask &= (self.index_frame[MDConcepts.Label] == label)
        elif labels is not None:
            mask &= (self.index_frame[MDConcepts.Label].isin(mangle_arg_to_set(labels)))
        if typ is not None:
            mask &= (self.index_frame[MDConcepts.Type] == typ)
        elif types is not None:
            mask &= (self.index_frame[MDConcepts.Type].isin(mangle_arg_to_set(typ)))

        return self.index_frame.loc[mask]

    def project(self,
                event_feature_selection: Mapping[
                    EventSpecLabel, bool | Collection[TimeseriesFeatureLabel]] = immutabledict(),
                measurement_feature_selection: Mapping[
                    MeasurementSpecLabel, bool | Collection[TimeseriesFeatureLabel]] = immutabledict(),
                project_underlying_dfs=False, copy_underlying_dfs=False) -> typing.Self:
        def proj(tsc: TimeseriesContainerProtocol, fs):
            tspec = tsc.timeseries_spec
            fs = mangle_arg_with_bool_fallback(mangle_arg_to_tuple, fs, if_true=tspec.features, preserve_order=True)
            spec_proj = tspec.project(fs)
            df_proj = tsc.df.loc[:,
                      MDConcepts.base_columns + list(spec_proj.features)] if project_underlying_dfs else tsc.df
            return spec_proj, (df_proj.copy() if copy_underlying_dfs else df_proj)

        es = [self._etsc_cls(*proj(self.event_series[e], fs)) for e, fs in event_feature_selection.items()]
        ms = [self._mtsc_cls(*proj(self.measurement_series[m], fs)) for m, fs in
              measurement_feature_selection.items()]

        index_view = self.create_index_view(
            labels=itertools.chain(event_feature_selection.keys(), measurement_feature_selection.keys()))
        if copy_underlying_dfs:
            index_view = index_view.copy()
        return self.__class__.of(meta=self.meta, events=es, measurements=ms, index_frame=index_view,
                                 lazy_index_creation=True,
                                 lazy_map_creation=True)

    def is_mergeable(self, other: MachineDataProtocol) -> bool:
        if self.__class__ != other.__class__:
            return False
        other: typing.Self = other
        for e, et in self.event_specs.items():
            if o_et := other.event_specs.get(e):
                if not et.is_mergeable(o_et):
                    return False
        for m, mt in self.measurement_specs.items():
            if o_mt := other.measurement_specs.get(m):
                if not mt.is_mergeable(o_mt):
                    return False
        return True

    def merge(self, other: MachineData,
              axis: Literal['horizontal', 'vertical'] = 'horizontal') -> MachineData:
        assert axis in {'horizontal', 'vertical'}
        assert self.is_mergeable(other)
        es, e_index_change = self._etsc_cls.lifted_merge(self.event_series, other.event_series, axis=axis)
        ms, m_index_change = self._mtsc_cls.lifted_merge(self.measurement_series, other.measurement_series, axis=axis)
        meta = self.meta.merge(other.meta)
        return self.__class__.of(meta=meta, events=es.values(), measurements=ms.values(), lazy_index_creation=True,
                                 lazy_map_creation=True,
                                 index_frame=(None if e_index_change | m_index_change else self.index_frame))

    def summary(self) -> str:
        first = min(self.index_frame[MDConcepts.Time])
        last = max(self.index_frame[MDConcepts.Time])
        return f'#Observations: {self.observation_count} between {first} and {last}.' + '\n' + f'#Objects: {len(self.objects)}' + '\n' + f'#Event Specs: {len(self.event_specs)}' + '\n' + f'#Measurement Specs: {len(self.measurement_specs)}'

    def __str__(self):
        def spec_strings(specs_dict):
            return '\n'.join([f'\t{label}: {", ".join(tspec.features)}' for label, tspec in specs_dict.items()])

        e_specs = spec_strings(self.event_specs)
        m_specs = spec_strings(self.measurement_specs)
        objs = ' ' + ', '.join(self.objects)
        return 'MachineData {' + '\n' + 'Event Specs:' + (
            '\n' + e_specs if e_specs != "" else "[]") + '\n' + 'Measurement Specs:' + (
            '\n' + m_specs if m_specs != "" else "[]") + '\n' + 'Objects:' + objs + '\n' + f'Observations: {self.observation_count}' + '\n' + '}'

    def __repr__(self):
        return str(self)


class BaseMachineData(AbstractMachineData[
                      EventTimeseriesSpec, EventTimeseriesView, EventTimeseriesContainer, MeasurementTimeseriesSpec, MeasurementTimeseriesView, MeasurementTimeseriesContainer]):
    _etsc_cls = EventTimeseriesContainer
    _mtsc_cls = MeasurementTimeseriesContainer

    @classmethod
    def of(cls, meta: Meta = Meta(), events: Iterable[ETSC] = (), measurements: Iterable[MTSC] = (),
           lazy_index_creation=True,
           lazy_map_creation=True, *args, **kwargs) -> BaseMachineData:
        return super().of(meta, events, measurements, *args, lazy_index_creation=lazy_index_creation,
                          lazy_map_creation=lazy_map_creation, **kwargs)

    def merge(self, other: BaseMachineData, axis: Literal['horizontal', 'vertical'] = 'horizontal') -> BaseMachineData:
        return super().merge(other, axis)


def build_shared_index(series: Iterable[TSContainer], index_cols=None,
                       override_categorical_types=True,
                       sort_by_time=False) -> pd.DataFrame:
    if index_cols is None:
        index_cols = MDConcepts.base_columns
    series = list(series)
    lengths = [len(tsc.df) for tsc in series]
    orig_idx_ranges = np.empty(len(lengths) + 1, dtype=int)
    np.cumsum(lengths, out=orig_idx_ranges[1:])
    orig_idx_ranges[0] = 0

    frame = pd.concat((tsc.df.loc[:, index_cols] for tsc in series), ignore_index=True, join='inner',
                      copy=True)

    if sort_by_time:
        sorted_idx = np.argsort(frame[MDConcepts.Time].values)
        frame = frame.iloc[sorted_idx]
        frame.reset_index(drop=True, inplace=True)
        rev = np.empty_like(sorted_idx)
        rev[sorted_idx] = np.arange(len(sorted_idx))
        for tsc, start, end in zip(series, orig_idx_ranges[:-1], orig_idx_ranges[1:]):
            tsc.df.index = pd.Index(rev[start:end])
            tsc.update_index()
    else:
        logging.log(logging.WARN, 'machine data index was not sorted')
        for tsc, start, end in zip(series, orig_idx_ranges[:-1], orig_idx_ranges[1:]):
            tsc.df.index = pd.RangeIndex(start, end)
            tsc.update_index()

    cats = derive_categoricals(frame, [MDConcepts.Object, MDConcepts.Type, MDConcepts.Label])
    frame = frame.astype(cats, copy=False)
    if override_categorical_types:
        for tsc in series:
            tsc.df = tsc.df.astype(cats, copy=False)
    return frame
