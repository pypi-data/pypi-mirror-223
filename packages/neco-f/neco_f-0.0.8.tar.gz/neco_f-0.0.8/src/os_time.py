# coding=gbk
# By 夕攘
import time
import datetime

time_format = "%m-%d_%H-%M-%S"  # 月-日_小时-分钟-秒


# 装饰器 记录运行时长
def count_time(func):
    def inner():
        start = time.perf_counter()
        func()
        finish = time.perf_counter()
        use_time = round(finish - start, 3)
        print(f'耗时 : {use_time}')

    return inner


def get_time():
    gmtime = time.gmtime()
    year = gmtime.tm_year  # 年
    mon = gmtime.tm_mon  # 月
    mday = gmtime.tm_mday  # 日
    hour = gmtime.tm_hour  # 小时
    min = gmtime.tm_min  # 分钟
    sec = gmtime.tm_sec  # 秒
    wday = gmtime.tm_wday + 1  # 星期
    yday = gmtime.tm_yday  # 一年中的第几天
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", gmtime)
    return year, mon, mday, hour, min, sec, wday, yday, format_time


# 格式化输出当前日期
def get_date():
    return time.strftime(time_format, time.localtime())


def how_many_days_ago(year: int, month: int, day: int):
    # 计算一个日期距今多少天
    past_date = datetime.datetime(year, month, day)
    today = datetime.datetime.today()
    days_diff = (today - past_date).days

    # print(f"{days_diff} days have passed since {past_date}")
    return days_diff
    # 268 days have passed since 2020-01-01 00:00:00


# 时间戳转换
def format_time(timestamp):
    formatted_time = datetime.datetime.fromtimestamp(timestamp).strftime(time_format)
    return formatted_time


if __name__ == '__main__':
    # print(format_time(1624297865))
    how_many_days_ago(2023, 8, 1)
