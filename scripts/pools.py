#%% 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# import dankpy 

# plt.style.use("dankpy.styles.latex")

# Load the data
data = pd.read_csv(r"data/NYC_Parks_Pools_20240719.csv")
data.columns = data.columns.str.lower()
#%% 
borough = {
    "M": "Manhattan",
    "B": "Brooklyn",
    "X": "The Bronx",
    "Q": "Queens",
    "R": "Staten Island"
}

data.borough = data.borough.apply(lambda x: borough[x])
# %%
import shapely.wkt

data.polygon = data.polygon.apply(lambda x: shapely.wkt.loads(x))

#%%
data["latitude"] = data.polygon.apply(lambda x: x.centroid.y)
data["longitude"] = data.polygon.apply(lambda x: x.centroid.x)
# %%

boro = data.groupby(["borough"]).count().reset_index()

#%% 
from database import Database, Pool, Attendance

db = Database("pools.db")

for d, row in data.iterrows():
    pool = Pool(
        name=row["name"], 
        borough=row["borough"],
        location=row["location"],
        pooltype=row["pooltype"], 
        latitude = row["latitude"],
        longitude = row["longitude"]
    )
    db.session.add(pool)
db.session.commit()

#%%

# fig, ax = plt.subplots()
# ax.bar(boro.borough, boro.name)
# ax.set_ylabel("Number of Pools")
# ax.tick_params(
# axis='x', # changes apply to the x-axis
# which='both', # both major and minor ticks are affected
# bottom=False, # ticks along the bottom edge are off
# top=False, # ticks along the top edge are off
# )
# # %%
# from dankpy import mapping, mymaptiles
# from matplotlib.ticker import FormatStrFormatter

# extents = mapping.find_extents(latitudes=data.latitude, longitudes=data.longitude)

# fig, ax = plt.subplots()
# extents = mapping.axes_aspect_expander(extents, sz=ax.figure.get_size_inches(), pad_meters=100)

# mapurl = next(iter(mapping.sources.values()))

# (ax0, axi) = mymaptiles.draw_map(ax=ax, bounds=extents, tile=mapurl, z=16)

# axi.set_interpolation("lanczos")
# ax.xaxis.set_major_formatter(FormatStrFormatter("%.4f"))
# ax.yaxis.set_major_formatter(FormatStrFormatter("%.4f"))
# ax.set_ylim(extents[1], extents[3])
# ax.set_xlim(extents[0], extents[2])
# ax.set_xticks([extents[0], extents[2]])
# ax.set_yticks([extents[1], extents[3]])

# fig
# # %%
