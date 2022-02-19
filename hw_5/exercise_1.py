from datetime import datetime as dt
import csv
import functools
import os


def simple_logger(func):
    filename = "log.csv"
    fields = ("start_time", "start_date", "func_name", "result")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = dt.now().time()
        start_date = dt.now().date()
        result = func(*args, **kwargs)
        _check = check_if_file_exists()
        mode = 'a' if _check else 'w'
        with open(r'log.csv', mode, newline='', encoding="utf-8") as f:
            writer = csv.writer(f, quotechar='|')
            if mode == 'w':
                writer.writerow(fields)
            writer.writerow([start_time, start_date, func.__name__, f"{args=} {kwargs=}", result])

        return result

    def check_if_file_exists():
        return filename in os.listdir(".")

    return wrapper


@simple_logger
def odd_or_even(num):
    return "Even" if num % 2 == 0 else "Odd"


if __name__ == '__main__':
    print(odd_or_even(2))
    print(odd_or_even(4))
    print(odd_or_even(3))
