import fsspec
import pandas as pd
import xarray as xr
from tqdm import tqdm
import json
import os
from pathlib import Path
from datetime import datetime

here = Path(os.path.dirname(__file__))


def build_catalog(bucket='ncar-cesm-lens'):
    fs = fsspec.filesystem(protocol='s3', anon=True)
    dirs = fs.ls(bucket)
    frequencies = []
    components = ['ice_nh', 'ice_sh', 'lnd', 'ocn', 'atm']
    for d in dirs:
        if d.split('/')[-1] in components:
            f = fs.ls(d)
            frequencies.extend(f[1:])

    stores = []
    for freq in frequencies:
        s = fs.ls(freq)[1:]
        stores.extend(s)

    entries = []
    for store in tqdm(stores[:10]):
        try:
            path_components = store.split('/')
            component, frequency = path_components[1], path_components[2]
            if frequency != 'static':
                _, experiment, variable = path_components[-1].split('.')[0].split('-')
                path = f's3://{store}'
                ds = xr.open_zarr(
                    fs.get_mapper(path), consolidated=True, decode_cf=False
                )
                long_name = ds[variable].attrs.get('long_name', None)
                dim_per_tsep = ds[variable].data.ndim - 2

                start = str(
                    xr.coding.times.decode_cf_datetime(
                        ds.time[0],
                        ds.time.attrs['units'],
                        ds.time.attrs['calendar'],
                        use_cftime=True,
                    )
                )
                end = str(
                    xr.coding.times.decode_cf_datetime(
                        ds.time[-1],
                        ds.time.attrs['units'],
                        ds.time.attrs['calendar'],
                        use_cftime=True,
                    )
                )
                entry = {
                    'component': component,
                    'frequency': frequency,
                    'experiment': experiment,
                    'variable': variable,
                    'path': path,
                    'variable_long_name': long_name.lower(),
                    'dim_per_tstep': dim_per_tsep,
                    'start': start,
                    'end': end,
                }
                entries.append(entry)
            else:
                entry = {'component': component, 'frequency': frequency, 'path': path}

            entries.append(entry)
        except ValueError:
            print(store)

    df = pd.DataFrame(entries)
    return df


if __name__ == '__main__':
    df = build_catalog()
    df.to_csv(here / 'aws-cesm1-le.csv', index=False)

    with open(here / 'aws-cesm1-le.json') as fin:
        data = json.load(fin)
    last_updated = datetime.now().utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    data['last_updated'] = last_updated

    with open(here / 'aws-cesm1-le.json', 'w') as fout:
        json.dump(data, fout)
