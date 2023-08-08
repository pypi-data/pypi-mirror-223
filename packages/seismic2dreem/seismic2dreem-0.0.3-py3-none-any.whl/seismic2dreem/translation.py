import numpy as np
import pandas as pd
import os
import gzip
import shutil
import os

translation_arrays = {
    "Called": 'cov',
    "Covered" : 'cov',
    "Informed": 'info',
    "Subbed": 'sub_N',
    "Subbed-A": 'sub_A',
    "Subbed-C": 'sub_C',
    "Subbed-G": 'sub_G',
    "Subbed-T": 'sub_T',
    "Deleted": 'del',
    "Inserted": 'ins',
}

def seismic_csv_to_dreem_json(csv_path:str):
    # load csv
    i = pd.read_csv(csv_path)
    sequence = ''.join(i['Base'].tolist())
    
    # convert to json
    d = {}
    for k, v in translation_arrays.items():
        if k in i.columns:
            d[v] = np.array(i[k], dtype=np.int64).tolist()
    d['min_cov'] = min(d['cov'])
    if 'info' not in d.keys():
        d['info'] = (i['Mutated'] + i['Matched']).tolist()
    d['sub_rate'] = np.divide(np.array(d['sub_N']).astype(float), np.array(d['info']).astype(float), out=np.zeros_like(np.array(d['sub_N']).astype(float)), where= np.array(d['info'])!=0).tolist()
    
    # add sub_hist from relate-per-read.csv.gz
    d['sub_hist'] = read_num_of_mutations(csv_path.replace('relate-per-pos.csv', 'relate-per-read.csv.gz'))
    
    return {'sequence': sequence, 'pop_avg': d}

def read_num_of_mutations(csv_gz_path:str):
    csv_path = untar_csv_gz(csv_gz_path)
    mut_per_read = pd.read_csv(csv_path)['Mutated']
    out = np.histogram(mut_per_read, bins=range(0, max(mut_per_read)+1))[0].tolist()
    os.remove(csv_path)
    return out

def untar_csv_gz(csv_gz_path):
    with gzip.open(csv_gz_path, 'rb') as f_in:
        with open(os.path.splitext(csv_gz_path)[0], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return f_out.name
