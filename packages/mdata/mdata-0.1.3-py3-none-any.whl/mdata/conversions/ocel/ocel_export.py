import pandas as pd

from mdata.core import MachineData, MDConcepts
from pm4py.objects.ocel.obj import OCEL, constants

import mdata.core.shared_defs


def create_ocel(md: MachineData):
    raise NotImplemented
    pd.DataFrame()
    os = md.index_frame[MDConcepts.Object].unique()
    for mt, tsc in md.measurement_series.items():
        i = 0
        m_obj = pd.DataFrame(tsc.df, columns=list(tsc.timeseries_spec.features))
        m_obj = m_obj.assign(**{constants.DEFAULT_OBJECT_TYPE: tsc.timeseries_spec.label, constants.DEFAULT_OBJECT_ID: i})
    for et, tsc in md.event_series.items():
        tsc.timeseries_spec.features

    ...