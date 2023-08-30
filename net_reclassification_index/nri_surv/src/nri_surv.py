import pandas as pd
from .process_nri import process_nri
from .categorical_nri_boot import (
    categorical_nri_boot,
)


def nri_surv(predictors, data, risk_limits, fu_time, status, time, n_boot):
    def wrapper(predictor):
        result = categorical_nri_boot(
            risk_limits=risk_limits,
            p_old=data[f"{predictors[0]}"],
            p_new=data[f"{predictor}"],
            fu_time=data[fu_time],
            status=data[status],
            time=time,
            n_boot=n_boot,
        )
        return result

    nri_matrix_ac = [wrapper(predictor) for predictor in predictors[1:]]
    nri_matrix_ac = pd.DataFrame(nri_matrix_ac)
    nri_matrix_ac = process_nri(nri_matrix_ac)

    return nri_matrix_ac
