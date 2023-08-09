import pandas as pd
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import io

# file_path = "/elwood/MERRA2_400.inst3_3d_asm_Np.20220101.nc4"

# ds = xr.open_dataset(file_path, engine="netcdf4", decode_coords="all")

# print("FULL SET")
# print(ds)

# cut_dataset = ds.sel(lev=500)

# # Drop the "lev" dimension from the dataset
# cut_dataset = cut_dataset.drop("lev")

# cut_dataset = cut_dataset.sel(lat=slice(10, 40), lon=slice(-120, -90))

# # Save the new dataset to a netCDF file
# cut_dataset.to_netcdf("cut_MERRA2_3D.20220101.nc4")

# post_cut = xr.open_dataset(
#     "cut_MERRA2_3D.20220101.nc4", engine="netcdf4", decode_coords="all"
# )

# print("POST CUT")
# print(post_cut)


# file_path = "/elwood/tests/inputs_transformations/cut_MERRA2_3D.20220101.nc4"

# ds = xr.open_dataset(file_path, engine="netcdf4", decode_coords="all")

# print(ds)

# df = ds.to_dataframe()

# df = df.reset_index()

# print(df)

# df_string = """
# date,lat,lon,temperature
# 2023-01-02,35.0,-95.0,83.0
# 2023-01-02,15.0,-95.0,73.0
# 2023-01-02,35.0,-115.0,93.0
# 2023-01-02,15.0,-115.0,83.0
# """

# df = pd.read_csv(io.StringIO(df_string))
# df = pd.read_csv("/elwood/merra_multi_output.csv")
df = pd.read_csv("/elwood/more_dates_pandas.csv")
# df_regrid = pd.read_csv("/elwood/merra_multi_output.csv")

# print(df)

# print(df.columns)

# print(df["PHIS"].values)

#####

# cut_dataset = ds.sel(lev=1)

# # Drop the "lev" dimension from the dataset
# cut_dataset = cut_dataset.drop("lev")

# # Save the new dataset to a netCDF file
# cut_dataset.to_netcdf("cut_MERRA2_3D.20220101.nc4")

# post_cut = xr.open_dataset(
#     "cut_MERRA2_3D.20220101.nc4", engine="netcdf4", decode_coords="all"
# )

# print(post_cut)

# ##
# # Create the plot
# fig = plt.figure(figsize=(12, 6))
# ax = plt.axes(projection=ccrs.PlateCarree())  # Create a geographic projection
# ax.coastlines()  # Add coastlines
# ax.add_feature(cfeature.BORDERS)  # Add country borders

# # Plot the temperature data
# img = ax.pcolormesh(
#     ds["lon"], ds["lat"], ds, cmap="RdBu_r", transform=ccrs.PlateCarree()
# )
# fig.colorbar(img, ax=ax, label="Temperature")
# plt.title("Temperature Distribution")
# plt.show()
# #####


lat_scale = 20.0
lon_scale = 20.0

# Create a grid of lat and lon values
lat = np.arange(
    df["latitude"].min(), df["latitude"].max() + lat_scale, 20.0
)  # 10 degree steps
lon = np.arange(
    df["longitude"].min(), df["longitude"].max() + lon_scale, 20.0
)  # 10 degree steps
print(lat)
print(lon)
grid_lon, grid_lat = np.meshgrid(lon, lat)

# Interpolate the temperature values to the grid
grid_temp = griddata(
    df[["latitude", "longitude"]].values,
    df["temperature"].values,
    (grid_lat, grid_lon),
    method="cubic",
)

# Create a figure and draw the map:
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.PlateCarree())  # Change the projection as needed
ax.coastlines()  # Draw coastlines
gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=True,
    linewidth=1,
    color="gray",
    alpha=0.5,
    linestyle="--",
    xlocs=range(-180, 180, 10),
    ylocs=range(-90, 90, 10),
)  # Gridlines
gl.xlabels_top = False
gl.ylabels_right = False

# Add the temperature as a filled contour plot:
mesh = plt.pcolormesh(
    grid_lon,
    grid_lat,
    grid_temp,
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    shading="auto",
)

# Add a colorbar
cbar = plt.colorbar(mesh, orientation="horizontal")
cbar.set_label("Temperature")

# Show the plot
plt.show()

plt.savefig("more_dates_actual_temp_pandas.png")


#### Total sum code
# columns = ["T", "PHIS", "V", "SLP"]
# # timestamp = "2022-01-01 00:00:00"

# # Set the DataFrame index to the 'timestamp' column
# df.set_index("time", inplace=True)

# # Use .loc[] to select rows with the specific timestamp

# results = {}
# for column in columns:
#     # selected_rows = df.loc[timestamp]

#     results[column] = df[column].sum()

# print(results)


### Comparing squares

# onetwenty_square = df[df["lon"] == -120.0]

# print(onetwenty_square[onetwenty_square["lat"] <= 10.0])

# # 14 regrid
# print("INTERMEDIATE POINT 14 ---")

# subset = onetwenty_square[
#     (onetwenty_square["lat"] >= 13.5) & (onetwenty_square["lat"] <= 14.4)
# ]

# total_sum = subset["T"].sum()
# print(f"Original total 120, 13.5-14.4: {total_sum}")


# grid_120 = df_regrid[df_regrid["lon"] == -120.0]
# onetwenty_14_points = grid_120[(grid_120["lat"] >= 13.5) & (grid_120["lat"] <= 14.4)]

# # print(onetwenty_14_points)

# total_sum = onetwenty_14_points["T"].sum()
# print(f"Regridded total 120, 13.5-14.4: {total_sum}")

# # Lower end
# print("LOWER END ---")

# subset = onetwenty_square[
#     (onetwenty_square["lat"] >= 10.0) & (onetwenty_square["lat"] <= 10.4)
# ]

# total_sum = subset["T"].sum()
# print(f"Original total 120, 10.0-10.4: {total_sum}")

# onetwenty_14_points = grid_120[(grid_120["lat"] >= 10.0) & (grid_120["lat"] <= 10.4)]

# # print(onetwenty_14_points)

# total_sum = onetwenty_14_points["T"].sum()
# print(f"Regridded total 120, 10.0-10.4: {total_sum}")


# # Upper end
# print("UPPER END ---")

# subset = onetwenty_square[
#     (onetwenty_square["lat"] >= 39.0) & (onetwenty_square["lat"] <= 40.0)
# ]

# total_sum = subset["T"].sum()
# print(f"Original total 120, 39.0-40.0: {total_sum}")

# onetwenty_14_points = grid_120[(grid_120["lat"] >= 40.0) & (grid_120["lat"] <= 41.0)]

# # print(onetwenty_14_points)

# total_sum = onetwenty_14_points["T"].sum()
# print(f"Regridded total 120, 39.5-40.0: {total_sum}")


# # Dropping over values

# filtered_df = df_regrid[df_regrid["lat"] <= 40.0]
# filtered_df = filtered_df[filtered_df["lon"] <= -90.0]
# grid_120 = filtered_df[filtered_df["lon"] == -120.0]

# onetwenty_14_points = grid_120[(grid_120["lat"] >= 40.0) & (grid_120["lat"] <= 41.0)]

# # print(onetwenty_14_points)

# total_sum = onetwenty_14_points["T"].sum()
# print(f"Regridded total 120, 39.5-40.0: {total_sum}")
