#! /usr/bin/env python3

import pandas as pd
import glob

path = r'./gofund_data'
files = glob.glob(path + "/*.csv")
file_list = []

for f in files:
    df = pd.read_csv(f, index_col=0, header=0)
    file_list.append(df)

df_all = pd.concat(file_list, axis=0, ignore_index=True)

# Save to new csv
with open('gofund_data_master.csv', 'w+') as f:
    df_all.to_csv('gofund_data_master.csv', encoding="utf-8", index=True)
print('Success.')
