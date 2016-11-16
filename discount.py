#The program will calculate the discount factor using in the related evaluations
import math
import time
from datetime import date
from datetime import datetime

#past is a string, and present is a date object, the result is in terms of days
def time_diff(past,present):
    temp = time.strptime(past, '%Y-%m-%d')
    dt   = datetime.fromtimestamp(time.mktime(temp))
    diff = present - dt.date()
    return diff.days

#The function requires a input that specify how long it takes to discount to half
#of initial value, in terms of year. The second input determine how long it will
#be used as discounting process
def discount(rate, time):
     r = math.log(2)/float(rate)
     #Suppose there are 365 days in a year
     return math.exp(-r*time/365)
