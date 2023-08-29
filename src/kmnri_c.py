import numpy as np
from ctypes import *
import ctypes
from math import pow


def kmnri(risklimits, pold, pnew, ftime, censvar, weight=None):
    n = len(censvar)
    risklimits = np.sort(
        np.unique(np.concatenate(([0.0], np.setdiff1d(risklimits, 1.0))))
    )
    risklimits = np.append(risklimits, [1 + pow(10, (-5))])
    ngroup = len(risklimits) - 1
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
    print(np.sort(events))
    print(len(events))

    up = np.zeros(2).ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    down = np.zeros(2).ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    survival = np.zeros(1).ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    risklimits = risklimits.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    pold = pold.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    pnew = pnew.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    ftime = ftime.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    weight = weight.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    len_events = len(events)
    events = events.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    len_events = ctypes.pointer(ctypes.c_int(len_events))
    censvar = censvar.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    n = ctypes.pointer(ctypes.c_int(n))
    ngroup_sq = int(pow(ngroup, 2))
    ngroup = ctypes.pointer(ctypes.c_int(ngroup))
    ngroup_sq = ctypes.pointer(ctypes.c_int(ngroup_sq))

    so_file = "validstats.so"
    my_functions = CDLL(so_file)

    my_functions.kmnriw(
        up,
        down,
        survival,
        risklimits,
        pold,
        pnew,
        ftime,
        weight,
        events,
        len_events,
        censvar,
        n,
        ngroup,
        ngroup_sq,
    )

    return {
        "casesup": up[1],
        "casesdown": down[1],
        "noncasesup": up[0],
        "noncasesdown": down[0],
    }
