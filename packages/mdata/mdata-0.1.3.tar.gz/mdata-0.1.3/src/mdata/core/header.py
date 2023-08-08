from __future__ import annotations

from collections.abc import Collection, Iterator, Mapping
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from immutabledict import immutabledict

from .extensions.annotations import AnnotationTypes
from .extensions.metadata import FeatureDataType
from .extensions.registry import Extension
from .util import take_first

if TYPE_CHECKING:
    from mdata.core.raw import RawHeaderSpec, RawBaseFeatureSpec, RawMetadataFeatureSpec


@dataclass(frozen=True, eq=True, repr=True)
class FeatureSpec:
    name: str
    print_name: str
    data_type: FeatureDataType = field(default=FeatureDataType.Infer)

    @classmethod
    def from_raw(cls, arg: RawBaseFeatureSpec | RawMetadataFeatureSpec) -> FeatureSpec:
        from .raw import RawMetadataFeatureSpec
        if isinstance(arg, str):
            arg: RawBaseFeatureSpec
            return cls(arg, arg)
        elif isinstance(arg, Mapping):
            f, spec = take_first(arg.items())
            spec: RawMetadataFeatureSpec
            data_type = spec.get('data_type', None)
            if data_type is not None:
                data_type = FeatureDataType(data_type)
            return cls(name=f, print_name=spec.get('print_name', f), data_type=data_type)

    def to_raw(self, use_metadata=True) -> RawBaseFeatureSpec | RawMetadataFeatureSpec:
        from .raw import RawMetadataFeatureSpec, FeatureMetadata, RawBaseFeatureSpec
        if use_metadata:
            if self.name == self.print_name and self.data_type is FeatureDataType.Infer:
                return RawBaseFeatureSpec(self.name)
            else:
                return RawMetadataFeatureSpec(
                    {'self.name': FeatureMetadata(print_name=self.print_name, data_type=self.data_type.value)})
        else:
            return RawBaseFeatureSpec(self.name)


@dataclass(frozen=True, eq=True, repr=True, init=True)
class ObservationSpec(Collection):
    features: tuple[FeatureSpec] = field(default_factory=tuple)

    # def __int__(self, *features: FeatureSpec) -> None:
    #     super().__init__()
    #     object.__setattr__(self, 'features', tuple(*features))

    def __contains__(self, item: object) -> bool:
        if type(item) is str:
            return any(f.name == item for f in self.features)
        elif isinstance(item, FeatureSpec):
            return item in self.features

    def __len__(self) -> int:
        return len(self.features)

    def __iter__(self) -> Iterator[FeatureSpec]:
        return iter(self.features)

    def __getitem__(self, item) -> FeatureSpec:
        if type(item) is int:
            return self.features[item]
        elif type(item) is str:
            return take_first((f for f in self if f.name == item))

    @classmethod
    def of(cls, *features: FeatureSpec):
        return cls(features)

    @classmethod
    def from_raw(cls, arg: list[RawBaseFeatureSpec | RawMetadataFeatureSpec]) -> ObservationSpec:
        return cls(tuple(FeatureSpec.from_raw(f) for f in arg))

    def to_raw(self, use_metadata=True) -> list[RawBaseFeatureSpec | RawMetadataFeatureSpec]:
        return [f.to_raw(use_metadata=use_metadata) for f in self.features]


ObservationSpecs = Mapping[str, ObservationSpec]


@dataclass(frozen=True, eq=True, repr=True)
class AnnotationSpecs:
    input: ObservationSpecs = field(default_factory=immutabledict)
    output: ObservationSpecs = field(default_factory=immutabledict)

    def to_raw(self, use_metadata=True):
        from .raw import RawAnnotationSpecs
        return RawAnnotationSpecs(input={a: spec.to_raw(use_metadata=use_metadata) for a, spec in self.input.items()},
                                  output={a: spec.to_raw(use_metadata=use_metadata) for a, spec in self.output.items()})


class NotMergeableException(Exception):
    pass


@dataclass(frozen=True, eq=True, repr=True)
class Meta:
    extensions: frozenset[Extension] = field(default_factory=frozenset)
    metadata: immutabledict[str, Any] = field(default_factory=immutabledict)

    @classmethod
    def of(cls, extensions: Collection[Extension], metadata: Mapping[str, Any]):
        return cls(frozenset(extensions), immutabledict(metadata))

    def is_mergeable(self, other: Meta):
        return self.extensions == other.extensions

    def merge(self, b: Meta) -> Meta:
        if not self.is_mergeable(b):
            raise NotMergeableException
        return Meta.of(self.extensions | b.extensions, dict(self.metadata) | dict(b.metadata))


@dataclass(frozen=True, eq=True, repr=True)
class Header:
    meta: Meta = field(default_factory=Meta)
    event_specs: ObservationSpecs = field(default_factory=immutabledict)
    measurement_specs: ObservationSpecs = field(default_factory=immutabledict)
    annotation_specs: AnnotationSpecs = field(default_factory=AnnotationSpecs)

    def lookup_feature(self, spec_type, label, feature) -> FeatureSpec:
        return self.lookup_spec(spec_type, label).features[feature]

    def lookup_spec(self, spec_type, label) -> ObservationSpec:
        from .shared_defs import ObservationTypes
        if spec_type == ObservationTypes.E:
            return self.event_specs.get(label)
        elif spec_type == ObservationTypes.M:
            return self.measurement_specs.get(label)
        elif spec_type in AnnotationTypes.csv_tuple_qualifiers:
            _, subtype = spec_type
            if subtype == AnnotationTypes.Input:
                return self.annotation_specs.input.get(label)
            elif subtype == AnnotationTypes.Output:
                return self.annotation_specs.output.get(label)

    @classmethod
    def from_raw(cls, raw_header: RawHeaderSpec) -> Header:
        meta = Meta.of({Extension(e) for e in raw_header.get('extensions', [])}, raw_header.get('metadata', {}))

        def make_specs(mapping):
            return {k: ObservationSpec.of(*(FeatureSpec.from_raw(f) for f in fs))
                    for k, fs in mapping.items()}

        event_specs = make_specs(raw_header['event_specs'])
        measurement_specs = make_specs(raw_header['measurement_specs'])

        annotation_specs = None
        if Extension.Annotations in meta.extensions:
            annotation_specs = AnnotationSpecs(make_specs(raw_header['annotation_specs']['input']),
                                               make_specs(raw_header['annotation_specs']['output']))

        return Header(meta, event_specs, measurement_specs, annotation_specs=annotation_specs)

    def to_raw(self) -> RawHeaderSpec:
        from .raw import RawHeaderSpec
        use_metadata = Extension.Metadata in self.meta.extensions
        include_annotations = Extension.Annotations in self.meta.extensions

        def specs_to_raw(spec_dict: Mapping[str, ObservationSpec]):
            return {s: spec.to_raw(use_metadata=use_metadata) for s, spec in spec_dict.items()}

        rh = RawHeaderSpec(event_specs=specs_to_raw(self.event_specs),
                           measurement_specs=specs_to_raw(self.measurement_specs))

        if len(self.meta.extensions) > 0:
            rh['extensions'] = [e.value for e in self.meta.extensions]
        if include_annotations:
            rh['annotation_specs'] = self.annotation_specs.to_raw(use_metadata=use_metadata)
        if use_metadata:
            rh['metadata'] = dict(self.meta.metadata)

        return rh


def create_header_from_raw(raw_header: RawHeaderSpec) -> Header:
    return Header.from_raw(raw_header)


def convert_header_to_raw(header: Header) -> RawHeaderSpec:
    return header.to_raw()
