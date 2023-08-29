import numpy as np
import pandas as pd
from scipy.stats import norm


def process_nri(x):
    qqq = norm.ppf(0.975)

    out = {
        "nri": x["nri"],
        "nri.left": x["nri"] - qqq * x["nri.SE"],
        "nri.right": x["nri"] + qqq * x["nri.SE"],
        "nri.ev": x["nri.ev"],
        "nri.ev.left": x["nri.ev"] - qqq * x["nri.ev.SE"],
        "nri.ev.right": x["nri.ev"] + qqq * x["nri.ev.SE"],
        "nri.nev": x["nri.nev"],
        "nri.nev.left": x["nri.nev"] - qqq * x["nri.nev.SE"],
        "nri.nev.right": x["nri.nev"] + qqq * x["nri.nev.SE"],
        "N": x["N"],
        "Nevent": x["Nevent"],
    }

    return pd.DataFrame(out)
