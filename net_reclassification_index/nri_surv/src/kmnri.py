import numpy as np
from .kmnriw import kmnriw


def kmnri(risk_limits, p_old, p_new, fu_time, status, weight=None):
    n = len(status)
    risk_limits = np.sort(
        np.unique(np.concatenate(([0.0], np.setdiff1d(risk_limits, 1.0))))
    )

    if weight is None:
        weight = np.ones(n)

    match = lambda a, b: [b.index(x) if x in b else None for x in a]

    indices = np.where(status == 1)[0]
    unique_events = np.unique(fu_time[indices])
    sorted_unique_events = list(np.sort(unique_events))
    events = np.asarray(
        match(
            sorted_unique_events,
            list(fu_time),
        )
    )

    up = np.zeros(2)
    down = np.zeros(2)
    survival = np.zeros(1)

    kmnriw(
        up=up,
        down=down,
        survival=survival,
        cutpoints=np.append(risk_limits, 1 + 1e-05),
        pold=p_old,
        pnew=p_new,
        ftime=fu_time,
        weights=weight,
        evtimes=events,
        ntimes=len(events),
        casestatus=status,
        n=n,
    )

    return {
        "cases_up": up[1],
        "cases_down": down[1],
        "noncases_up": up[0],
        "noncases_down": down[0],
    }
