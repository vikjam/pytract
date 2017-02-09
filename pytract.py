import requests
import pandas as pd
import numpy as np
import os
import glob
from random import randint
from time import sleep

load_df       = pd.read_csv('us500.csv', header = None)
# load_df       = load_df.columns.str.strip()
load_df[3] = load_df[3].apply(lambda x: str(x).zfill(5))
for g, df in load_df.groupby(np.arange(len(load_df)) // 1000):
    submit_path = os.path.join('acs_submit' + str(g) + '.csv')
    df.to_csv(submit_path, header = False)

for g, fname in enumerate(glob.glob('acs_submit*.csv')):
    url     = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch'
    payload = {'benchmark': 'Public_AR_Current',
               'vintage':   'Current_Current'}
    files   = {'addressFile': (fname, open(fname, 'rb'), 'text/csv')}
    r       = requests.post(url, files = files, data = payload)
    print(r.text, file = open('acs_result' + str(g) + '.csv', 'w'))
    sleep(randint(10, 60))

# curl --form addressFile=@us500.csv --form benchmark=Public_AR_Current vintage=ACS2013_Current vintage= http://geocoding.geo.census.gov/geocoder/locations/addressbatch --output geocoderesult.csv
