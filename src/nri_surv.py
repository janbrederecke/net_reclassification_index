import pandas as pd
import numpy as np

from src.kmnri import kmnri
from src.process_nri import process_nri
from src.categ_nri_boot import categ_nri_boot


def nri_surv(preds, data, risklimits, ftime, censvar, Time, Nboot):
    def wrapper(pred):
        result = categ_nri_boot(
            risklimits=risklimits,
            pold=data[f"{preds[0]}"],
            pnew=data[f"{pred}"],
            ftime=data[ftime],
            censvar=data[censvar],
            Time=Time,
            Nboot=Nboot,
        )
        return result

    nri_matrix_ac = [wrapper(pred) for pred in preds[1:]]
    nri_matrix_ac = pd.DataFrame(nri_matrix_ac)
    nri_matrix_ac = process_nri(nri_matrix_ac)

    return nri_matrix_ac
