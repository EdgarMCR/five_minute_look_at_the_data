import re
import os
import time
import json
from pathlib import Path

import pandas as pd
import matplotlib.pylab as plt


class Col:
    indicator = 'Indicator'
    value = 'Indicator Value'
    value_type = "Indicator Value Units"
    sample_size = 'Sample Size'
    yr_from = 'Collection Year From'
    yr_to = 'Collection Year To'
    age_range = 'Age Range'
    gender = 'Gender'
    percent = 'percent'


def load_spreadsheet(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name='values', engine='openpyxl')
    df = df.rename(columns=lambda x: x.replace(' \n ', ' '))
    return df


def main():
    path = Path(r'C:\Users\Developer\Downloads\hace_pilot_db_spreadsheet_20210307_1655.xlsx')
    df = load_spreadsheet(path)
    print(df.columns)
    print(df.head())

    print('len(df) = {}'.format(len(df)))
    df = df[df[Col.indicator] == 'Children in employment']
    print('len(df) = {}'.format(len(df)))
    df = df[df[Col.gender] == 'All']
    print('len(df) = {}'.format(len(df)))

    df = df[df[Col.value] <= df[Col.sample_size]]
    print('len(df) = {}'.format(len(df)))

    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print(df[[Col.indicator, Col.value, Col.value_type, Col.sample_size, Col.yr_from, Col.yr_to]])

    condition = df[Col.value_type] == 'Count'
    p1 = df[condition][Col.value] / df[condition][Col.sample_size]

    condition = df[Col.value_type] == 'Percentage'
    p2 = df[condition][Col.value] / 100

    df[Col.percent] = pd.concat([p1, p2])

    plt.figure()
    plt.scatter(df[Col.yr_from], df[Col.percent] * 100)
    plt.ylabel('Child labour %')
    plt.xlabel('Year')
    plt.savefig(r'C:\Users\Developer\Downloads\child_labour.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    start_time = time.time()   # pylint: disable=C0103
    main()
    print("Ran %s in %.3f seconds" % (os.path.basename(__file__), time.time() - start_time))
