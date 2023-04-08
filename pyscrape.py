# -*- coding: utf-8 -*-

import csv
import datetime
import os
import requests


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
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    print(response.text)
    jikai = response.text.count('次回')
    taiki = response.text.count('待機中')
    return jikai + taiki, taiki

if __name__ == '__main__':
    now_datetime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    date = now_datetime.strftime("%Y-%m-%d")
    time = now_datetime.strftime("%H:%M")
    list_of_name_url = read_from_csv('url.csv')
    for index, tenpo_url in enumerate(list_of_name_url):
        tenpo = tenpo_url[0]
        url = tenpo_url[1]
        shukkin, taiki = get_from_url(url)
        output_file = 'output' + str(index) + '.csv'
        output_row = [date, time, shukkin, taiki]
        write_to_csv(output_file, tenpo, output_row)
