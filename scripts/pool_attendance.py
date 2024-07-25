#%% 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from database import Database, Pool, Attendance

# Load the data
data = pd.read_csv(r"data/Outdoor_Swimming_Pool_Attendance_20240719.csv")
#%%
data.columns = data.columns.str.lower()
data = data.rename(columns={"date":"datetime"})
data["datetime"] = pd.to_datetime(data["datetime"])
data["pool"] = data["pool"].str.strip()

# %%
date = data.groupby("datetime").sum().reset_index()[["datetime","attendance"]]
date = date.groupby(date.datetime.dt.year)["attendance"].sum().reset_index()

lookup = {
    "Astoria Hts PS 10":"Astoria Pool",
    "David Fox/PS 251 Pool": "David Fox / PS 251 Mini Pool",
    "JHS 57/HS 26 Pool": "JHS 57 / HS 26 Mini Pool",
    "Mullaly Pool": "Mullaly Wading Pool"
}

# %%
db = Database("pools.db")

for i, group in data.groupby("pool"):
    name = group.iloc[0].pool

    if name in lookup.keys():
        name = lookup[name]

    pool = db.session.query(Pool).filter(Pool.name.contains(name)).first()

    if pool: 
        aa = []
        for d, row in group.iterrows(): 
            a = Attendance(
                pool=pool,
                datetime=row["datetime"],
                number=row["attendance"]
            )
            aa.append(a)
        db.session.add_all(aa)
    else:
        print(name)
    db.session.commit()
# %%
