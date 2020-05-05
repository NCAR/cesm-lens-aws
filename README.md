# CESM LENS on AWS
- [CESM LENS on AWS](#cesm-lens-on-aws)
  - [Re-create notebooks with Pangeo Binder](#re-create-notebooks-with-pangeo-binder)
  - [ESM catalog](#esm-catalog)
  - [Requirements](#requirements)
  - [Examples](#examples)
  - [Reference Documentation](#reference-documentation)

Examples of analysis of [CESM LENS data](https://registry.opendata.aws/ncar-cesm-lens/) publicly available on Amazon S3 (us-west-2 region) using xarray and dask.

## Re-create notebooks with Pangeo Binder

Try these notebooks on Pangeo Binder. Note that
the session is ephemeral. **Your home directory will not persist, so remember to download your notebooks if you made changes that you need to use at a later time!**

[![badge](https://img.shields.io/badge/Launch%20Pangeo%20Binder-%20AWS%20us--west--2-F5A252.svg?logo=data:image/png;base64,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)](https://aws-uswest2-binder.pangeo.io/v2/gh/NCAR/cesm-lens-aws/master?urlpath=lab)


## ESM catalog

The master catalog URL is:

https://raw.githubusercontent.com/NCAR/cesm-lens-aws/master/intake-catalogs/aws-cesm1-le.json


This catalog is an [ESM collection](https://github.com/NCAR/esm-collection-spec) catalog. The data is stored in [Zarr](https://github.com/zarr-developers/zarr) format and meant to be opened with [Xarray](http://xarray.pydata.org/en/latest/).


## Requirements

Using this catalog requires the following package versions:

- [Intake-esm](https://github.com/NCAR/intake-esm) >= `v2020.5.1`

## Examples

To open the catalog and load a data set from Python, you can run the following code:

```python

In [1]: import intake

In [2]: col = intake.open_esm_datastore("https://raw.githubusercontent.com/NCAR/cesm-lens-aws/master/intake-catalogs/aws-cesm1-le.json")

In [3]: col
Out[3]:
aws-cesm1-le-ESM Collection with 302 entries:
        > 5 component(s)

        > 5 frequency(s)

        > 6 experiment(s)

        > 54 variable(s)

        > 302 path(s)

In [4]: col_subset = col.search(experiment="RCP85", frequency="monthly", variable=["hi", "aice"])

In [5]: col_subset
Out[5]:
aws-cesm1-le-ESM Collection with 4 entries:
        > 2 component(s)

        > 1 frequency(s)

        > 1 experiment(s)

        > 2 variable(s)

        > 4 path(s)

In [6]: dsets = col_subset.to_dataset_dict(zarr_kwargs={"consolidated": True}, storage_options={"anon": True})

--> The keys in the returned dictionary of datasets are constructed as follows:
        'component.experiment.frequency'

--> There is/are 2 group(s)
[########################################] | 100% Completed |  3.3s

In [7]: dsets.keys()
Out[7]: dict_keys(['ice_sh.RCP85.monthly', 'ice_nh.RCP85.monthly'])

In [8]: ds = dsets['ice_sh.RCP85.monthly']

In [9]: ds
Out[9]:
<xarray.Dataset>
Dimensions:      (d2: 2, member_id: 40, ni: 320, nj: 76, nvertices: 4, time: 1140)
Coordinates:
  * member_id    (member_id) int64 1 2 3 4 5 6 7 8 ... 34 35 101 102 103 104 105
  * time         (time) object 2006-02-01 00:00:00 ... 2101-01-01 00:00:00
Dimensions without coordinates: d2, ni, nj, nvertices
Data variables:
    ANGLE        (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    ANGLET       (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    HTE          (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    HTN          (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    TLAT         (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    TLON         (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    ULAT         (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    ULON         (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    aice         (member_id, time, nj, ni) float32 dask.array<chunksize=(40, 36, 76, 320), meta=np.ndarray>
    blkmask      (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    dxt          (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    dxu          (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    dyt          (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    dyu          (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    latt_bounds  (nj, ni, nvertices) float32 dask.array<chunksize=(76, 320, 4), meta=np.ndarray>
    latu_bounds  (nj, ni, nvertices) float32 dask.array<chunksize=(76, 320, 4), meta=np.ndarray>
    lont_bounds  (nj, ni, nvertices) float32 dask.array<chunksize=(76, 320, 4), meta=np.ndarray>
    lonu_bounds  (nj, ni, nvertices) float32 dask.array<chunksize=(76, 320, 4), meta=np.ndarray>
    tarea        (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    time_bounds  (time, d2) object dask.array<chunksize=(1140, 2), meta=np.ndarray>
    tmask        (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    uarea        (nj, ni) float32 dask.array<chunksize=(76, 320), meta=np.ndarray>
    hi           (member_id, time, nj, ni) float32 dask.array<chunksize=(40, 36, 76, 320), meta=np.ndarray>
Attributes:
    comment:                   All years have exactly 365 days
    contents:                  Diagnostic and Prognostic Variables
    conventions:               CF-1.0
    history:                   2019-07-19 13:44:43.986221 xarray.open_dataset...
    comment2:                  File written on model date 20060201
    comment3:                  seconds elapsed into model date:      0
    NCO:                       4.3.4
    nco_openmp_thread_number:  1
    source:                    sea ice model: Community Ice Code (CICE)
```

## Reference Documentation

For details about intake-esm API, see the [reference documentation](https://intake-esm.readthedocs.io/en/latest)
