import numpy as np
import pandas as pd

import mdata.core.shared_defs
from mdata.core.shared_defs import MeasurementSpecLabel
from mdata.core import MachineData, MDConcepts


def estimate_measurement_frequencies(md: MachineData) -> dict[MeasurementSpecLabel, float]:
    res = {}
    for m, tsc in md.measurement_series.items():
        diffs = tsc.df[MDConcepts.Time].diff()
        med = diffs.median()
        values = diffs.sort_values()
        n = len(values)
        inner_values = values.iloc[int(0.05 * n):int(0.95 * n)]
        f_mean = inner_values.mean()
        f_med = inner_values.median()
        std = inner_values.std()
        if abs(f_med - f_mean) > std:
            print('mean and median differ significantly', med, f_mean, f_med, std)
        s = pd.Timedelta.total_seconds(f_mean)
        res[m] = 1 / s if s > 0 else np.inf
    return res
