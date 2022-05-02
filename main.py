import matplotlib.pyplot as mpl
import pandas as pd
import math

def print_data(obj, data):
    min = data["min"]
    max = data["max"]
    avg = data["avg"]
    sum = data["sum"]
    
    print(f"-----------{obj.upper()}-----------")
    print(f"The minimum {obj} is {min}")
    print(f"The maximum {obj} is {max}")
    print(f"The average {obj} is {avg}")
    print(f"The sum of the {obj}s is {sum}")
    print("----------------------" + ('-'*len(obj)))
    print()

def get_column(data_set, filter_name, filter_value, column):
    return data_set[data_set[str(filter_name)] == filter_value][column]


def filter_by_manhattan(data_set, column):
    return get_column(data_set, "BOROUGH", 1, str(column).upper())

# Cleans the data set provided by dropping all rows containing the "replaced" parameter in the column provided.
# Replaces all instances of the "replaced" parameter in the column with NaN, before dropping all rows containing NaN.
def clean(data_set, replaced, column):
    data_set[str(column)] = data_set[str(column)].replace(replaced, math.nan) # Replace "replaced" with NaN
    data_set.dropna(subset=[str(column)], inplace=True) # Drop rows with NaN (previously "replaced")

# Read the csv, and remove incomplete rows.
# No row should have blank prices or square footage, and the year built and ZIP Code cannot be 0
data = pd.read_csv("nyc-rolling-sales.csv", header=0)
clean(data, " -  ", "GROSS SQUARE FEET")
clean(data, " -  ", "SALE PRICE")
clean(data, 0, "YEAR BUILT")
clean(data, 0, "ZIP CODE")

price = {
    "sum": 0,
    "max": 0,
    "min": 0,
    "avg": 0
}
sqft = {
    "sum": 0,
    "max": 0,
    "min": 0,
    "avg": 0
}
zip_code = {
    "sum": 0,
    "max": 0,
    "min": 0,
    "avg": 0
}
year_built = {
    "sum": 0,
    "max": 0,
    "min": 0,
    "avg": 0
}

def gen_points(dictionary, series):
    dictionary["min"] = float(series[0])
    dictionary["max"] = float(series[0])
    
    for num in series:
        num = float(num)

        if num < dictionary["min"]:
            dictionary["min"] = num

        if num > dictionary["max"]:
            dictionary["max"] = num
        
        dictionary["sum"] += num

    dictionary["avg"] = dictionary["sum"] / len(series)
    
gen_points(price, filter_by_manhattan(data, "SALE PRICE"))
gen_points(sqft, filter_by_manhattan(data, "GROSS SQUARE FEET"))
gen_points(zip_code, filter_by_manhattan(data, "ZIP CODE"))
gen_points(year_built, filter_by_manhattan(data, "YEAR BUILT"))
print_data("price", price)
print_data("sqft", sqft)
print_data("zip code", zip_code)
print_data("year built", year_built)

def square_footage():
    mpl.subplot(3, 1, 1)
    mpl.bar(filter_by_manhattan(data, "GROSS SQUARE FEET"),
            filter_by_manhattan(data, "SALE PRICE"), color='blue')

    mpl.xlabel("Square ft")
    mpl.ylabel("Price")
    mpl.title("Price vs. Square footage in Manhattan")
    mpl.xticks(visible=False)
    mpl.yticks(visible=False)

def zip_code():
    mpl.subplot(3, 1, 2)
    
    mpl.scatter(filter_by_manhattan(data, "ZIP CODE"), 
                filter_by_manhattan(data, "SALE PRICE"), color='green')

    mpl.xlabel("Zip Code")
    mpl.ylabel("Price")
    mpl.title("Price vs. ZIP Code in Manhattan")
    mpl.yticks(visible=False)
    
def year():
    mpl.subplot(3, 1, 3)
    
    mpl.bar(filter_by_manhattan(data, "YEAR BUILT"), 
                filter_by_manhattan(data, "SALE PRICE"), color='red')

    mpl.xlabel("Zip Code")
    mpl.ylabel("Price")
    mpl.title("Price vs. Year Built in Manhattan")
    mpl.yticks(visible=False)
        
mpl.suptitle("Price vs. Square Footage, Zip Code, and Year Built in Manhattan")        

square_footage()
zip_code()
year()
mpl.tight_layout()
mpl.show()