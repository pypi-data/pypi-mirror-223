import os
from collections import defaultdict
from json import JSONDecodeError

import jsonschema
from yaml import YAMLError

from mdata.core.shared_defs import ObservationTypes
from mdata.core import raw
from mdata.core.extensions import registry, metadata, annotations
from mdata.file_formats.io_utils import DataSource
from .importing import read_raw_data, read_machine_data, read_machine_data_canonical
from .. import io_utils
from ..validity_checking_utils import *


def is_valid_canonical_file_pair(base_path):
    try:
        read_machine_data_canonical(base_path, validity_checking=True)
    except ValidityCheckingException:
        return False
    return True


def is_valid_file_pair(header_path, data_path):
    try:
        read_machine_data(header_path, data_path, validity_checking=True)
    except ValidityCheckingException:
        return False
    return True


def check_if_readable_header_definition_file(file: DataSource, do_full_check=True):
    seen = defaultdict(set)
    try:
        lines_from = io_utils.read_csv_lines_from(file)
    except Exception as e:
        raise MalformedHeaderFileException('Unparseable csv:\n' + str(e))
    if do_full_check:
        for k, row in enumerate(lines_from, start=1):
            if row[0] == MDConcepts.Type and row[1] == MDConcepts.Label:
                # skip header if included
                continue

            row_identifier = row[0]
            non_empty_idx = [0]
            if row_identifier in ObservationTypes:
                label = row[1]
                non_empty_idx.append(1)
                if label in seen[row_identifier]:
                    raise MalformedHeaderFileException(f'Duplicate observation type specification in line {k}.')
                seen[row_identifier].add(label)
            elif row_identifier == registry.CSV_KEY:
                if True in seen[row_identifier]:
                    raise MalformedHeaderFileException(f'Duplicate extension declaration in line {k}.')
                seen[row_identifier].add(True)
            elif row_identifier == metadata.CSV_KEY:
                non_empty_idx.extend([1, 2, 3, 4, 5])
                if row[2] in ObservationTypes:
                    e = tuple(row[1:5])
                elif row[2] == annotations.CSV_KEY:
                    e = tuple(row[1:6])
                    non_empty_idx.append(6)
                else:
                    raise MalformedHeaderFileException(f'Invalid symbol in metadata declaration in line {k}.')
                if e in seen[row_identifier]:
                    raise MalformedHeaderFileException(f'Duplicate metadata declaration in line {k}.')
                seen[row_identifier].add(e)
            elif row_identifier == annotations.CSV_KEY:
                non_empty_idx.extend([1, 2, 3])
                label = (row[1], row[2])
                if label in seen[row_identifier]:
                    raise MalformedHeaderFileException(f'Duplicate annotation declaration in line {k}.')
                seen[row_identifier].add(label)
            else:
                raise MalformedHeaderFileException(f'Invalid specification symbol in first column in line {k}.')
            if any(row[i] == '' for i in non_empty_idx):
                raise MalformedHeaderFileException(f'Incomplete specification line in Line {k}.')
    return True


def check_if_readable_header_definition_file_yaml(file: DataSource, do_full_check=True):
    try:
        header = io_utils.read_yaml_dict_from(file, swallow_exceptions=False)
        if do_full_check:
            check_if_valid_raw_header(header)
    except YAMLError as e:
        raise MalformedHeaderFileException('Unparseable yaml:\n' + str(e))

    return True


def check_if_readable_header_definition_file_json(file: DataSource, do_full_check=True):
    try:
        header = io_utils.read_json_dict_from(file, swallow_exceptions=False)
        if do_full_check:
            check_if_valid_raw_header(header)
    except JSONDecodeError as e:
        raise MalformedHeaderFileException('Unparseable json:\n' + str(e))
    return True


header_schema = io_utils.read_json_dict_from(os.path.join(os.path.dirname(__file__), '..', 'header_schema.json'))


def check_if_valid_raw_header(raw_header: raw.RawHeaderSpec):
    try:
        jsonschema.validate(raw_header, header_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise MalformedHeaderFileException('Schema validation failed.\n' + str(e))
    return True


def check_if_valid_data_file(path):
    df = read_raw_data(path)
    check_if_valid_raw_data(df)
    return True


def check_if_valid_raw_data(df):
    if any(c not in df.columns for c in MDConcepts.base_columns):
        raise MalformedDataFileException(
            f'Data is missing base column(s): {set(MDConcepts.base_columns) - set(df.columns)}.')
    check_time_column(df)
    placeholder_cols = get_placeholder_cols(df)
    to_be_cols = gen_feature_column_names(len(placeholder_cols))
    if any(a != b for a, b in zip(placeholder_cols, to_be_cols)):
        raise MalformedDataFileException('Placeholder feature columns have unexpected labels.')
    return True
