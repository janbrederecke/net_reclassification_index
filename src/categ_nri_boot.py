import numpy as np
from scipy.stats import norm
from src.kmnri import kmnri


def categ_nri_boot(risklimits, pold, pnew, ftime, censvar, Time, Nboot):
    v = np.where(ftime > Time)[0]
    if len(v) > 0:
        censvar[v] = 0
        ftime[v] = Time

    Data = np.column_stack((pold, pnew, ftime, censvar))
    Data = Data[~np.isnan(Data).any(axis=1)]

    def kmnri_boot(data, indices):
        data = data[indices]
        a = kmnri(
            risklimits=risklimits,
            pold=data[:, 0],
            pnew=data[:, 1],
            ftime=data[:, 2],
            censvar=data[:, 3],
            weight=None,
        )
        nri_ev = a["casesup"] - a["casesdown"]
        nri_nev = a["noncasesdown"] - a["noncasesup"]
        nri = nri_ev + nri_nev
        return np.array([nri_ev, nri_nev, nri])

    # Calculate SE and CIs by bootstrapping
    Nboot = int(Nboot)
    results = []
    for _ in range(Nboot):
        indices = np.random.choice(Data.shape[0], size=Data.shape[0], replace=True)
        boot_result = kmnri_boot(Data, indices)
        results.append(boot_result)
    results_boot = np.array(results)
    SE = np.std(results_boot, axis=0)

    # Calculate NRI and NRI
    nri_result = kmnri(
        risklimits=risklimits,
        pold=Data[:, 0],
        pnew=Data[:, 1],
        ftime=Data[:, 2],
        censvar=Data[:, 3],
        weight=None,
    )
    nri_ev = nri_result["casesup"] - nri_result["casesdown"]
    nri_nev = nri_result["noncasesdown"] - nri_result["noncasesup"]
    nri = nri = nri_ev + nri_nev

    out = {
        "nri": nri,
        "nri.SE": SE[2],
        "nri.p": 2 * norm.cdf(-np.abs(nri) / SE[2]),
        "nri.ev": nri_ev,
        "nri.ev.SE": SE[0],
        "nri.ev.p": 2 * norm.cdf(-np.abs(nri_ev) / SE[0]),
        "nri.nev": nri_nev,
        "nri.nev.SE": SE[1],
        "nri.nev.p": 2 * norm.cdf(-np.abs(nri_nev) / SE[1]),
        "N": Data.shape[0],
        "Nevent": np.sum(Data[:, 3] == 1),
    }

    return out
