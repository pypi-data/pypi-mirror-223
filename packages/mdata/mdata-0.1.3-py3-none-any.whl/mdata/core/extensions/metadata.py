from __future__ import annotations

from enum import Enum

import numpy as np
import pandas as pd

CSV_KEY = 'META'


class FeatureDataTypeConversionException(Exception):
    pass


class FeatureDataType(Enum):
    Infer = 'infer'
    String = 'string'
    Int = 'int'
    Float = 'float'
    Boolean = 'boolean'
    Categorical = 'categorical'
    Datetime = 'datetime'
    Duration = 'duration'


target_numeric_types = {FeatureDataType.Int: int, FeatureDataType.Float: float}


def infer_type(series: pd.Series):
    converted = series.convert_dtypes()
    return get_type(converted)


# noinspection PyProtectedMember
def get_type(series: pd.Series) -> FeatureDataType:
    from pandas.api.types import is_bool_dtype, is_float_dtype, is_integer_dtype, is_categorical_dtype, \
        is_datetime64_any_dtype, is_timedelta64_dtype, is_string_dtype

    dtype = series.dtype
    if is_string_dtype(dtype):
        return FeatureDataType.String
    elif is_integer_dtype(dtype):
        return FeatureDataType.Int
    elif is_float_dtype(dtype):
        return FeatureDataType.Float
    elif is_bool_dtype(dtype):
        return FeatureDataType.Boolean
    elif is_categorical_dtype(dtype):
        return FeatureDataType.Categorical
    elif is_datetime64_any_dtype(dtype):
        return FeatureDataType.Datetime
    elif is_timedelta64_dtype(dtype):
        return FeatureDataType.Duration
    else:
        return FeatureDataType.Infer


def infer_types(df: pd.DataFrame):
    return {c: infer_type(df.loc[:, c]) for c in df.columns}


def get_types(df: pd.DataFrame) -> dict[str, FeatureDataType]:
    return {c: get_type(df.loc[:, c]) for c in df.columns}


def is_series_convertible(series: pd.Series, data_type: FeatureDataType):
    if (data_type == FeatureDataType.Int) or (data_type == FeatureDataType.Float):
        try:
            conv = series.astype(target_numeric_types[data_type], errors='raise')
        except Exception:
            return False
        return np.array_equal(series, conv)
    elif data_type == FeatureDataType.Boolean:
        try:
            conv = series.astype(bool, errors='raise')
        except Exception:
            return False
        return np.array_equal(series, conv)
    elif data_type == FeatureDataType.Datetime:
        try:
            pd.to_datetime(series, errors='raise', format='ISO8601')
        except Exception:
            return False
        return True
    elif data_type == FeatureDataType.Duration:
        try:
            pd.to_timedelta(series, errors='raise')
        except Exception:
            return False
        return True
    return False


def convert_df(df: pd.DataFrame, data_types: dict[str, FeatureDataType], inplace=False):
    res = pd.DataFrame(index=df.index) if not inplace else df

    for f, dt in data_types.items():
        try:
            if inplace:
                convert_series(df.loc[:, [f]], dt, inplace=True)
            else:
                res[f] = convert_series(df.loc[:, [f]], dt, inplace=False)
        except Exception as e:
            raise FeatureDataTypeConversionException(f'Conversion of feature {f} to {dt} failed:\n' + str(e))

    return res


def convert_series(arg: pd.Series | pd.DataFrame, data_type: FeatureDataType, inplace=True):
    copy = not inplace

    def upd_inplace(arg, conv):
        if isinstance(arg, pd.Series):
            arg.loc[:] = conv
        elif isinstance(arg, pd.DataFrame):
            arg.loc[:, :] = conv

    if data_type is FeatureDataType.Int or data_type is FeatureDataType.Float:
        return arg.astype(target_numeric_types[data_type], copy=copy)
    elif data_type is FeatureDataType.Boolean:
        return arg.astype(bool, copy=copy)
    elif data_type is FeatureDataType.Datetime:
        datetime = pd.to_datetime(arg, errors='raise', format='ISO8601')
        if inplace:
            upd_inplace(arg, datetime)
            return arg
        else:
            return datetime
    elif data_type is FeatureDataType.Duration:
        timedelta = pd.to_timedelta(arg, errors='raise')
        if inplace:
            upd_inplace(arg, timedelta)
            return arg
        else:
            return timedelta
    elif data_type is FeatureDataType.String:
        return arg.astype(str, copy=copy)
    elif data_type is FeatureDataType.Categorical:
        if isinstance(arg, pd.DataFrame):
            cdt = {c: pd.CategoricalDtype(arg.loc[:, c].dropna().unique()) for c in arg.columns}
        elif isinstance(arg, pd.Series):
            cdt = pd.CategoricalDtype(arg.dropna().unique())
        return arg.astype(cdt, copy=copy)
    elif data_type is FeatureDataType.Infer:
        conv = arg.convert_dtypes()
        if inplace:
            upd_inplace(arg, conv)
            return arg
        else:
            return conv
