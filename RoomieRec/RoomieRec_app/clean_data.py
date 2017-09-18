import csv
import re
import pandas as pd
from datetime import datetime

def clean(file):
    with open(file) as csvfile:
        data = []
        for row in csv.reader(csvfile):
            if row[0] == 'title':
                continue
            else:
                data.append([value for value in row])
    duplicate = []
    for row in data:
        if row[5] in duplicate:
            del row
            continue
        else:
            duplicate.append(row[5])
        if row[0] == '':
            row[0] = None
        if row[1] == '':
            row[1] = None
        else:
            row[1] = int(row[1].replace('$', ''))
        if row[2] == '':
            row[2] = None
        else:
            row[2] = row[2][1:-1].replace('(', '').replace(')', '')
        if row[3] == '':
            row[3] = None
        else:
            row[3] = datetime.strptime(row[3] , '%Y-%m-%d')
        if row[4] == '':
            row[4] = None
        else:
            row[4] = row[4].replace('<span>', '').replace('</span>', '').replace('[', '').replace(']', '').split(', ')
        if row[5] == '':
            row[5] = None
        else:
            row[5] = re.sub(r'QR Code Link to This Post', '', row[5])
            row[5] = re.sub(r'\\[ntr]', ' ', row[5])
            row[5] = re.sub('\\s+', ' ', row[5])
        if row[6] == '':
            row[6] = None
        else:
            row[6] = float(row[6])
        if row[7] == '':
            row[7] = None
        else:
            row[7] = float(row[7])
    df = pd.DataFrame(data)
    df.columns = ['title', 'price', 'neighborhood', 'movein', 'attributes', 'description', 'latitude', 'longitude']
    return df
