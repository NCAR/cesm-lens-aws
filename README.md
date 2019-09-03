# CESM LENS on AWS
- [CESM LENS on AWS](#cesm-lens-on-aws)
  - [Intake Catalogs](#intake-catalogs)
    - [Requirements](#requirements)
    - [Examples](#examples)

Examples of analysis of CESM LENS data publicly available on Amazon S3 (us-west-2 region) using xarray and dask


## Intake Catalogs

The master intake catalog URL is:

https://raw.githubusercontent.com/NCAR/cesm-lens-aws/master/intake-catalogs/master.yaml


This catalog is an [Intake](https://github.com/ContinuumIO/intake) catalog. The data is stored in [Zarr](https://github.com/zarr-developers/zarr) format and meant to be opened with [Xarray](http://xarray.pydata.org/en/latest/).


### Requirements

Using this catalog requires the following package versions:

- [Intake-xarray](https://github.com/intake/intake-xarray) >= 0.3.1
- [Dask](https://github.com/dask/dask) >= 2.2.0

### Examples

To open the catalog and load a dataset from Python, you can run the following code

```python
import intake
cat_url = "https://raw.githubusercontent.com/NCAR/cesm-lens-aws/master/intake-catalogs/master.yaml"
cat = intake.Catalog(cat_url)
ds = cat.ice_northern_hemisphere_monthly.grid_cellmean_ice_thickness_RCP85.to_dask()
```


To explore the whole catalog, you can try:

```python
cat.walk(depth=5)
```
