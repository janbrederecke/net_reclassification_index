import numpy as np
from src.kmnriw import kmnriw


def kmnri(risklimits, pold, pnew, ftime, censvar, weight=None):
    n = len(censvar)
    risklimits = np.sort(
        np.unique(np.concatenate(([0.0], np.setdiff1d(risklimits, 1.0))))
    )
    ngroup = len(risklimits)
    if weight is None:
        weight = np.ones(n)

    match = lambda a, b: [b.index(x) if x in b else None for x in a]

    indices = np.where(censvar == 1)[0]
    unique_events = np.unique(ftime[indices])
    sorted_unique_events = list(np.sort(unique_events))
    events = np.asarray(
        match(
            sorted_unique_events,
            list(ftime),
        )
    )

    up = np.zeros(2)
    down = np.zeros(2)
    survival = np.zeros(1)

    kmnriw(
        up,
        down,
        survival,
        np.append(risklimits, 1 + 1e-05),
        pold,
        pnew,
        ftime,
        weight,
        events,
        len(events),
        censvar,
        n,
    )

    return {
        "casesup": up[1],
        "casesdown": down[1],
        "noncasesup": up[0],
        "noncasesdown": down[0],
    }
