# coding=gbk
# By Ϧ��
import time
import datetime

time_format = "%m-%d_%H-%M-%S"  # ��-��_Сʱ-����-��


# װ���� ��¼����ʱ��
def count_time(func):
    def inner():
        start = time.perf_counter()
        func()
        finish = time.perf_counter()
        use_time = round(finish - start, 3)
        print(f'��ʱ : {use_time}')

    return inner


def get_time():
    gmtime = time.gmtime()
    year = gmtime.tm_year  # ��
    mon = gmtime.tm_mon  # ��
    mday = gmtime.tm_mday  # ��
    hour = gmtime.tm_hour  # Сʱ
    min = gmtime.tm_min  # ����
    sec = gmtime.tm_sec  # ��
    wday = gmtime.tm_wday + 1  # ����
    yday = gmtime.tm_yday  # һ���еĵڼ���
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", gmtime)
    return year, mon, mday, hour, min, sec, wday, yday, format_time


# ��ʽ�������ǰ����
def get_date():
    return time.strftime(time_format, time.localtime())


# ʱ���ת��
def format_time(timestamp):
    formatted_time = datetime.datetime.fromtimestamp(timestamp).strftime(time_format)
    return formatted_time


if __name__ == '__main__':
    print(format_time(1624297865))
