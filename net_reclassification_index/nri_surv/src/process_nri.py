import numpy as np
import pandas as pd
from scipy.stats import norm


def process_nri(results):
    qqq = norm.ppf(0.975)

    output = {
        "nri": results["nri"],
        "nri_left": results["nri"] - qqq * results["nri_se"],
        "nri_right": results["nri"] + qqq * results["nri_se"],
        "nri_ev": results["nri_ev"],
        "nri_ev_left": results["nri_ev"] - qqq * results["nri_ev_se"],
        "nri_ev_right": results["nri_ev"] + qqq * results["nri_ev_se"],
        "nri_nev": results["nri_nev"],
        "nri_nev_left": results["nri_nev"] - qqq * results["nri_nev_se"],
        "nri_nev_right": results["nri_nev"] + qqq * results["nri_nev_se"],
        "n": results["n"],
        "n_event": results["n_event"],
    }

    return pd.DataFrame(output)
