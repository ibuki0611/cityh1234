# -*- coding: utf-8 -*-

import csv
import datetime
import os
import requests
import time

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def write_to_csv(file_path, tenpo, row):
    if not os.path.isfile(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['店舗:', tenpo])
            writer.writerow(['日付', '時間', '出勤数', '待機'])
    with open(file_path, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def read_from_csv(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        ret = [row for row in reader]
    return ret


def get_from_url(url):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=10,
                    status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    try:
        response = session.request('GET', url, timeout=10)
    except Exception as e:
        print(f'connection to {url} failed')
        print(e)
        return 0, 0
    response.encoding = response.apparent_encoding
    jikai = response.text.count('次回')
    taiki = response.text.count('待機中')
    return jikai + taiki, taiki

if __name__ == '__main__':
    now_datetime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    now_date = now_datetime.strftime("%Y-%m-%d")
    now_time = now_datetime.strftime("%H:%M")
    list_of_name_url = read_from_csv('url.csv')
    for index, tenpo_url in enumerate(list_of_name_url):
        tenpo = tenpo_url[0]
        url = tenpo_url[1]
        shukkin, taiki = get_from_url(url)
        output_file = 'output' + str(index) + '.csv'
        output_row = [date, now_time, shukkin, taiki]
        write_to_csv(output_file, tenpo, output_row)
        time.sleep(5)
