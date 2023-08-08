import os

import pandas as pd

from mdata.core import MDConcepts, MachineData
from mdata.core.extensions import Extension
from mdata.file_formats import io_utils


def write_machine_data_h5(filename, md: MachineData, complevel: int = 0, **kwargs) -> None:
    if 'format' not in kwargs:
        kwargs['format'] = 't'
    if isinstance(filename, str | os.PathLike):
        io_utils.ensure_directory_exists(filename)
        filename = io_utils.ensure_ext(filename, '.h5')
    with pd.HDFStore(filename, mode='w', complib='blosc', complevel=complevel) as store:
        store.put('index', md.index_frame, index=True, data_columns=MDConcepts.base_columns,
                  dropna=False, **kwargs)
        store.create_table_index('index', columns=['index', MDConcepts.Time, MDConcepts.Label], kind='full')

        def put_series(key, df):
            store.put(key, df, index=True, data_columns=MDConcepts.base_columns, dropna=False,
                      **kwargs)
            store.create_table_index(key, columns=['index', MDConcepts.Time, MDConcepts.Label], kind='full')

        for label, ess in md.event_series.items():
            put_series(f'events/{label}', ess.df)
        for label, mss in md.measurement_series.items():
            put_series(f'measurements/{label}', mss.df)

        if len(md.meta.extensions) > 0:
            store.put('meta/extensions', list(md.meta.extensions), format='table', index=False)
        if Extension.Metadata in md.meta.extensions:
            keys, values = map(list, zip(*((k, v) for k, v in md.meta.metadata.items())))
            metadata_df = pd.DataFrame(data=values, index=pd.Index(keys, name='key'), columns=['value'])
            store.put('meta/metadata', metadata_df)

            specs_extra_metadata = []
            for tsc in md.series_containers:
                tt = tsc.timeseries_spec
                t, label = tt.identifier
                for fspec in tt.base.features:
                    row = [t, label, fspec.name, fspec.print_name if fspec.name != fspec.print_name else [],
                           fspec.data_type if fspec.data_type is not None else []]
                specs_extra_metadata.append(row)
            store.put('meta/specs', pd.DataFrame(specs_extra_metadata,
                                                 columns=[MDConcepts.Type, MDConcepts.Label, 'feature',
                                                          'print_name', 'data_type']))
