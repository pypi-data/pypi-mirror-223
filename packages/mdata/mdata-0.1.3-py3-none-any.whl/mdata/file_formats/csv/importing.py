from __future__ import annotations

import io
import os.path
from typing import Literal, Union, Mapping, Optional

import pandas as pd

from mdata.core import raw, MDConcepts, MachineData
from mdata.core.shared_defs import ObservationTypes
from mdata.core.extensions import metadata as metadata_ext, annotations as annotations_ext, registry
from mdata.file_formats import io_utils
from mdata.file_formats.csv.shared import mk_filename_pair, HeaderFormatLiterals, HeaderFileFormat
from mdata.file_formats.io_utils import DataSource


def read_raw_data(source: DataSource) -> pd.DataFrame:
    if isinstance(source, memoryview):
        source = source.tobytes()
    if isinstance(source, bytes):
        with io.BytesIO(source) as buf:
            df = pd.read_csv(buf, parse_dates=False)
    else:
        df = pd.read_csv(source, parse_dates=False)
    df[MDConcepts.Time] = pd.to_datetime(df[MDConcepts.Time], format='ISO8601')
    return df


def read_machine_data(header_source: DataSource, data_source: DataSource, validity_checking=True,
                      header_format: Union[Literal['infer'], HeaderFormatLiterals] = 'infer') -> MachineData:
    if header_format == 'infer' and isinstance(header_source, str):
        header_format = os.path.splitext(header_source)[1][1:]
    if header_format not in HeaderFileFormat:
        from mdata.file_formats.validity_checking_utils import UnsupportedHeaderFileFormat
        raise UnsupportedHeaderFileFormat(header_format)
    if validity_checking:
        def do_file_checks():
            if header_format == HeaderFileFormat.CSV:
                from .checking import check_if_readable_header_definition_file
                check_if_readable_header_definition_file(header_source)
            elif header_format == HeaderFileFormat.JSON:
                from .checking import check_if_readable_header_definition_file_json
                check_if_readable_header_definition_file_json(header_source)
            elif header_format == HeaderFileFormat.YAML:
                from .checking import check_if_readable_header_definition_file_yaml
                check_if_readable_header_definition_file_yaml(header_source)

        if isinstance(header_source, io.IOBase):
            if header_source.seekable():
                do_file_checks()
                header_source.seek(0)
            else:
                print('skipped file validity checking due to working on non-seekable buffer')
        else:
            do_file_checks()

    raw_header: Optional[raw.RawHeaderSpec] = None
    if header_format == HeaderFileFormat.CSV:
        raw_header = read_raw_header(header_source)
    elif header_format == HeaderFileFormat.JSON:
        raw_header = read_raw_header_json(header_source)
    elif header_format == HeaderFileFormat.YAML:
        raw_header = read_raw_header_yaml(header_source)

    if validity_checking:
        assert raw_header is not None
        from .checking import check_if_valid_raw_header
        check_if_valid_raw_header(raw_header)

    raw_data = read_raw_data(data_source)

    if validity_checking:
        from .checking import check_if_valid_raw_data
        from mdata.file_formats.validity_checking_utils import check_header_data_compatibility
        check_if_valid_raw_data(raw_data)
        check_header_data_compatibility(raw_header, raw_data)

    return raw.create_machine_data_from_raw(raw_data, raw_header)


def read_machine_data_canonical(basepath, validity_checking=True,
                                header_format: HeaderFormatLiterals = 'csv') -> MachineData:
    header_file, data_file = mk_filename_pair(basepath, header_format=header_format)
    return read_machine_data(header_file, data_file, validity_checking=validity_checking, header_format=header_format)


def read_raw_header_json(source: DataSource) -> raw.RawHeaderSpec:
    return io_utils.read_json_dict_from(source)


def read_raw_header_yaml(source: DataSource) -> raw.RawHeaderSpec:
    return io_utils.read_yaml_dict_from(source)


def read_raw_header(source: DataSource) -> raw.RawHeaderSpec:
    result = raw.RawHeaderSpec()
    result['event_specs'] = {}
    result['measurement_specs'] = {}

    def get_type_spec_dict(row: list[str]):
        subdict = {}
        type_spec_key = row.pop(0)
        if type_spec_key == ObservationTypes.E:
            subdict = result['event_specs']
        elif type_spec_key == ObservationTypes.M:
            subdict = result['measurement_specs']
        elif type_spec_key == annotations_ext.CSV_KEY:
            in_or_out_key: annotations_ext.AnnotationTypeLongNames = annotations_ext.AnnotationTypes.long_names[
                row.pop(0)]
            if 'annotation_specs' not in result:
                result['annotation_specs'] = {'input': {}, 'output': {}}
            subdict = result['annotation_specs']
            subdict = subdict[in_or_out_key]
        return subdict

    for row in io_utils.read_csv_lines_from(source):
        statement_identifier = row[0]
        if statement_identifier == registry.CSV_KEY:
            result['extensions'] = [e for e in row[1:] if e != '']
        if statement_identifier in {ObservationTypes.E, ObservationTypes.M, annotations_ext.CSV_KEY}:
            specs = get_type_spec_dict(row)
            label = row.pop(0)
            specs[label] = [f for f in row if f != '']
        elif statement_identifier == metadata_ext.CSV_KEY:
            row.pop(0)
            key = row.pop(0)
            spec_dict = get_type_spec_dict(row)
            features = spec_dict[row.pop(0)]
            target_feature = row.pop(0)
            value = row.pop(0)
            for j, f_spec in enumerate(features):
                if type(f_spec) is str and target_feature == f_spec:
                    features[j] = {target_feature: {key: value}}
                    break
                elif isinstance(f_spec, Mapping) and target_feature in f_spec:
                    f_spec[target_feature][key] = value
                    break
    return result
