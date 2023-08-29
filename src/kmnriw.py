import numpy as np


def kmnriw(
    up,
    down,
    survival,
    cutpoints,
    pold,
    pnew,
    ftime,
    weights,
    evtimes,
    ntimes,
    casestatus,
    n,
):
    skmup = 1.0
    skmdown = 1.0
    counterup = 0.0
    counterdown = 0.0
    total = 0.0

    indold = np.zeros(n, dtype=int)
    indnew = np.zeros(n, dtype=int)

    survival = 1.0

    for l in range(n):
        indold[l] = np.sum(pold[l] > cutpoints[1:])
        indnew[l] = np.sum(pnew[l] > cutpoints[1:])
        if indold[l] < indnew[l]:
            counterup += weights[l]
        if indold[l] > indnew[l]:
            counterdown += weights[l]
        total += weights[l]

    for k in range(ntimes):
        cases = 0.0
        casesup = 0.0
        casesdown = 0.0
        riskset = 0.0
        risksetup = 0.0
        risksetdown = 0.0
        for l in range(n):
            if ftime[l] == ftime[evtimes[k]]:
                if casestatus[l]:
                    cases += weights[l]
                    if indold[l] < indnew[l]:
                        casesup += weights[l]
                    if indold[l] > indnew[l]:
                        casesdown += weights[l]
            if ftime[l] >= ftime[evtimes[k]]:
                riskset += weights[l]
                if indold[l] < indnew[l]:
                    risksetup += weights[l]
                if indold[l] > indnew[l]:
                    risksetdown += weights[l]

        if riskset > 0.0:
            survival *= 1.0 - cases / riskset
        if risksetup > 0.0:
            skmup *= 1.0 - casesup / risksetup
        if risksetdown > 0.0:
            skmdown *= 1.0 - casesdown / risksetdown

    up[1] = (1.0 - skmup) * (counterup / total) / (1.0 - survival)
    up[0] = skmup * (counterup / total) / survival
    down[1] = (1.0 - skmdown) * (counterdown / total) / (1.0 - survival)
    down[0] = skmdown * (counterdown / total) / survival

    return up[0], up[1], down[0], down[1]
