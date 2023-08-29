import pandas as pd
import numpy as np
from kmnri import kmnri

data = pd.read_csv("./data/data.csv")
preds = ["base", "big"]
event_time = "time"
event = "status"
Time = time_span = 600
r_boot_nri = 50
risklimits = [0.9]
pold = np.asarray(data.pred_base)
pnew = np.asarray(data.pred_big)
ftime = np.asarray(data.time)
censvar = np.asarray(data.status)

v = np.where(ftime > Time)[0]
if len(v) > 0:
    censvar[v] = 0
    ftime[v] = Time

data = np.column_stack((pold, pnew, ftime, censvar))
data = data[~np.isnan(data).any(axis=1)]

a = kmnri(
    risklimits=risklimits,
    pold=data[:, 0],
    pnew=data[:, 1],
    ftime=data[:, 2],
    censvar=data[:, 3],
    weight=None,
)

print(a)
