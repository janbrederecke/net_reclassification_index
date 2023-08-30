import numpy as np
from scipy.stats import norm
from .kmnri import kmnri


def categorical_nri_boot(risk_limits, p_old, p_new, fu_time, status, time, n_boot):
    v = np.where(fu_time > time)[0]
    if len(v) > 0:
        np.asarray(status)[v] = 0
        np.asarray(fu_time)[v] = time

    data = np.column_stack((p_old, p_new, fu_time, status))
    data = data[~np.isnan(data).any(axis=1)]

    def kmnri_boot(data, indices):
        data = data[indices]
        a = kmnri(
            risk_limits=risk_limits,
            p_old=data[:, 0],
            p_new=data[:, 1],
            fu_time=data[:, 2],
            status=data[:, 3],
            weight=None,
        )
        nri_ev = a["cases_up"] - a["cases_down"]
        nri_nev = a["noncases_down"] - a["noncases_up"]
        nri = nri_ev + nri_nev
        return np.array([nri_ev, nri_nev, nri])

    # Calculate se and CIs by bootstrapping
    n_boot = int(n_boot)
    results = []
    for _ in range(n_boot):
        indices = np.random.choice(data.shape[0], size=data.shape[0], replace=True)
        boot_result = kmnri_boot(data, indices)
        results.append(boot_result)
    results_boot = np.array(results)
    se = np.std(results_boot, axis=0)

    # Calculate NRI and NRI
    nri_result = kmnri(
        risk_limits=risk_limits,
        p_old=data[:, 0],
        p_new=data[:, 1],
        fu_time=data[:, 2],
        status=data[:, 3],
        weight=None,
    )
    nri_ev = nri_result["cases_up"] - nri_result["cases_down"]
    nri_nev = nri_result["noncases_down"] - nri_result["noncases_up"]
    nri = nri = nri_ev + nri_nev

    out = {
        "nri": nri,
        "nri_se": se[2],
        "nri_p": 2 * norm.cdf(-np.abs(nri) / se[2]),
        "nri_ev": nri_ev,
        "nri_ev_se": se[0],
        "nri_ev_p": 2 * norm.cdf(-np.abs(nri_ev) / se[0]),
        "nri_nev": nri_nev,
        "nri_nev_se": se[1],
        "nri_nev_p": 2 * norm.cdf(-np.abs(nri_nev) / se[1]),
        "n": data.shape[0],
        "n_event": np.sum(data[:, 3] == 1),
    }

    return out
