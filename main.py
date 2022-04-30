import matplotlib.pyplot as mpl
import pandas as pd
import numpy as np
import math


def clean(data_set, replaced, column):
    data_set[str(column)] = data_set[str(column)].replace(replaced, math.nan)
    data_set.dropna(subset=[str(column)], inplace=True)


def get_column(data_set, filter_name, filter_value, column):
    return data_set[data_set[str(filter_name)] == filter_value][column]


def filter_by_manhattan(data_set, column):
    clean(data_set, " -  ", "GROSS SQUARE FEET")
    clean(data_set, " -  ", "SALE PRICE")
    clean(data_set, 0, "YEAR BUILT")
    return get_column(data_set, "BOROUGH", 1, str(column).upper())


data = pd.read_csv("nyc-rolling-sales.csv", header=0)
clean(data, " -  ", "GROSS SQUARE FEET")
clean(data, " -  ", "SALE PRICE")
clean(data, 0, "YEAR BUILT")

min_price = float(data['SALE PRICE'][0])
max_price = float(data['SALE PRICE'][0])
sum_price = 0.0
avg_price = 0.0

for num in data['SALE PRICE']:
    num = float(num)

    if num < min_price:
        min_price = num

    if num > max_price:
        max_price = num

    sum_price += num

print(max_price)

avg_price = sum_price / len(data['SALE PRICE'][0])

mpl.bar(filter_by_manhattan(data, "GROSS SQUARE FEET"),
        filter_by_manhattan(data, "SALE PRICE"), color='blue')

mpl.xlabel("Square ft")
mpl.ylabel("Price")
mpl.title("Price vs. Square footage in Manhattan")
mpl.xticks(visible=False)
mpl.yticks(ticks=np.arange(0, float(max_price), 100000), labels=np.arange(0, float(max_price), 100000))
mpl.show()