import calendar
import concurrent.futures
import datetime
import os
import platform

from tqdm import tqdm
from win32_setctime import setctime

import helpers.constants as constants


class Date:
    @staticmethod
    def numericize(string):
        months = {m: c for c, m in enumerate(calendar.month_abbr) if c}
        try:
            return months[string]
        except KeyError:
            print('Month does not exist.')
            return 0

    def __iter__(self):
        return iter([self._year, self._month, self._day])

    def __init__(self, day, month, year):
        self._day = int(day)
        self._month = self.numericize(month)
        self._year = int(year)

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, day):
        self._day = day

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, month):
        self._month = month

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        self._year = year


class Time:
    def __iter__(self):
        return iter([self._hour, self._minute, self._second])

    def __init__(self, hour, minute, second):
        self._hour = int(hour)
        self._minute = int(minute)
        self._second = int(second)

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, hour):
        self._hour = hour

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, minute):
        self._minute = minute

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, second):
        self._second = second


class Timestamp:
    def __init__(self, date: list, time: list):
        self.date = Date(*date)
        self.time = Time(*time)
        self._count = 0

    def get_timestamp(self):
        try:
            date = datetime.datetime(*iter(self.date), *iter(self.time))
            timestamp = date.timestamp()
            return timestamp
        except ValueError:
            if not self._count:
                print(
                    'Value for month is invalid. Please file an issue at https://github.com/Amenly/pocketstars-dl')
            self._count += 1
        return 0


def create_main_dir(username):
    os.makedirs(os.path.join(os.getcwd(), username), exist_ok=True)
    return


def prepare_download(media, s, username):
    if media:
        with tqdm(total=len(media), desc='Downloading images/videos', colour='red') as bar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(download, *t, s, username): t for t in media}
                for future in concurrent.futures.as_completed(futures):
                    future.result
                    bar.update(1)


def download(url, date, s, username):
    filename = url.split('?')[0].rsplit('/')[-1]
    path = os.path.join(os.getcwd(), username, filename)
    with s.get(url) as r:
        if r.ok:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
        else:
            print(
                f'Received {r.status_code} STATUS CODE -- Unable to download {url}')
    if date:
        set_time(path, date)


def set_time(path, date):
    timestamp = get_timestamp(date)
    if not timestamp:
        return
    if platform.system() == 'Windows':
        setctime(path, timestamp)
    os.utime(path, (timestamp, timestamp))


def get_timestamp(date):
    date_split = date.split()
    length = len(date_split)
    filtered_date = [
        info for c, info in enumerate(date_split) if c and c < length - 1]
    time = filtered_date.pop().split(':')
    ts = Timestamp(filtered_date, time)
    timestamp = ts.get_timestamp()
    return timestamp
