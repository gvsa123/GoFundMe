#! /usr/bin/env python3
fin = open('urllist.txt', 'r') #'data_campaign_links.txt'
fin_lst = fin.readlines()
seen = set()
uniq = []
for x in fin_lst:
    if x not in seen:
        uniq.append(x)
        seen.add(x)
print(len(uniq), len(seen))
# with open('urllist_master.txt', 'w') as fout:
#     for url in uniq:
#         fout.write(url)
