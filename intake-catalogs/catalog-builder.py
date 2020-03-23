import fsspec
import pandas as pd


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

    for store in stores:
        path_components = store.split('/')
        component, frequency = path_components[1], path_components[2]
        _, experiment, variable = path_components[-1].split('.')[0].split('-')
        entry = {
            'component': component,
            'frequency': frequency,
            'experiment': experiment,
            'variable': variable,
            'path': f's3://{store}',
        }
        entries.append(entry)

    df = pd.DataFrame(entries)
    df.to_csv('aws-cesm1-le.csv', index=False)


if __name__ == '__main__':
    build_catalog()
