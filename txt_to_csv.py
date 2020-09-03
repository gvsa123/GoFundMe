import csv
from itertools import islice

with open('./Data/sample_campaign_info.txt') as fin, open('output.csv', 'w') as fout:
    pipe_out = csv.writer(fout, delimiter=',')
    rows = iter(lambda: list(islice(fin, 6)), [])
    pipe_out.writerows(rows)
