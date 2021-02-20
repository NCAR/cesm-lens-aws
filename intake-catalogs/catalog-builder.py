import json
import os
from datetime import datetime
from pathlib import Path

import cf_xarray  # noqa
import fsspec
import pandas as pd
import xarray as xr
from tqdm import tqdm

here = Path(os.path.dirname(__file__))


def build_catalog(bucket='ncar-cesm-lens'):
    fs = fsspec.filesystem(protocol='s3', anon=True)
    dirs = fs.ls(bucket)
    frequencies = []
    components = ['ice_nh', 'ice_sh', 'lnd', 'ocn', 'atm']
    experiments = ['CTRL', 'HIST', 'RCP85', '20C']
    regions = {
        'atm': 'global',
        'ocn': 'global_ocean',
        'lnd': 'global_land',
        'ice_nh': 'artic_ocean',
        'ice_sh': 'antarctica',
    }
    for d in dirs:
        if d.split('/')[-1] in components:
            f = fs.ls(d)
            frequencies.extend(f[1:])

    stores = []
    for freq in frequencies:
        s = fs.ls(freq)[1:]
        stores.extend(s)

    entries = []
    for store in tqdm(sorted(stores)):
        try:
            path_components = store.split('/')
            component, frequency = path_components[1], path_components[2]
            path = f's3://{store}'
            if frequency != 'static':

                _, experiment, variable = path_components[-1].split('.')[0].split('-')
                ds = xr.open_zarr(fs.get_mapper(path), consolidated=True, use_cftime=True)

                start_time, end_time = str(ds.time[0].data), str(ds.time[-1].data)
                long_name = ds[variable].attrs.get('long_name', None)
                units = ds[variable].attrs.get('units', None)

                vertical_levels = 1
                try:
                    vertical_levels = ds[ds.cf['vertical'].name].size
                except KeyError:
                    pass

                entry = {
                    'component': component,
                    'frequency': frequency,
                    'experiment': experiment,
                    'variable': variable,
                    'path': path,
                    'long_name': long_name.lower(),
                    'vertical_levels': vertical_levels,
                    'start_time': start_time,
                    'end_time': end_time,
                    'spatial_domain': regions[component],
                    'units': units,
                }
                entries.append(entry)
            else:
                entry = {'component': component, 'frequency': frequency, 'path': path}
                static_entries = [
                    {
                        'component': component,
                        'frequency': frequency,
                        'path': path,
                        'experiment': exp,
                        'spatial_domain': regions[component],
                    }
                    for exp in experiments
                ]
                entries.extend(static_entries)
        except ValueError:
            print(store)
    df = pd.DataFrame(entries)
    columns = [
        'variable',
        'long_name',
        'component',
        'experiment',
        'frequency',
        'vertical_levels',
        'spatial_domain',
        'units',
        'start_time',
        'end_time',
        'path',
    ]
    return df[columns]


if __name__ == '__main__':
    df = build_catalog()
    df.to_csv(here / 'aws-cesm1-le.csv', index=False)

    with open(here / 'aws-cesm1-le.json') as fin:
        data = json.load(fin)
    last_updated = datetime.now().utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    data['last_updated'] = last_updated

    with open(here / 'aws-cesm1-le.json', 'w') as fout:
        json.dump(data, fout, indent=2)
