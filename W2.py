'''
Python version 2.7.9
Author Joona R.
Date 2016/4/12
'''

import pandas as pd
import numpy as np


data = pd.read_csv("gapminder.csv", low_memory = False, skipinitialspace = True)
print(len(data))
print(len(data.columns))
data2 = data.ix[:, ["country", "suicideper100th", "alcconsumption", "urbanrate", "incomeperperson"]] #subsetting the needed columns

### As the data is quite sparse and specific values would have been very few, I decided to divide the countries into ten bins starting from the smallest value and ending in the highest

# variables from my codebook
variables = ["suicideper100th", "alcconsumption", "urbanrate", "incomeperperson"]

# texts copied directly from the gapminder codebook
texts = {"suicideper100th" : "2005 Suicide, age adjusted, per 100 000. Mortality due to self-inflicted injury, per 100 000 standard population, age adjusted", 
    "alcconsumption" : "2008 alcohol consumption per adult (age 15+), litres. Recorded and estimated average alcohol consumption, adult (15+) per capita consumption in litres pure alcohol", 
    "urbanrate" : "2008 urban population (% of total) Urban population refers to people living in urban areas as defined by national statistical offices (calculated using World Bank population estimates and urban ratios from the United Nations World Urbanization Prospects)", 
    "incomeperperson":"2010 Gross Domestic Product per capita in constant 2000 US$. The inflation but not the differences in the cost of living between countries has been taken into account."}

# creates a loop that goes through all the different variables
for i in variables:
    print "\n"
    # converts all the variables to numeric
    data2[i]=pd.to_numeric(data2[i])
    # make the binsize as 10 equally big parts based on the difference between the min and max values
    binSize = int(round((int(data2[i].max())-int(data2[i].min()))/10.0))
    
    #prints the introtext for the variable
    print texts[i]
    
    # displays the range (min-max) of the single values and the countries they are from
    print "The values of", i, "range from", int(data2[i].min()), "in", data2.get_value(data2[i].argmin(), "country"), "to", int(data2[i].max()), "in", data2.get_value(data2[i].argmax(), "country")
    
    # creates the counts for each of the bins
    vals = data2[i].value_counts(sort = False, bins = range(int(data2[i].min()), int(data2[i].max()+binSize), binSize), dropna = False)
    print vals
    print "number of entries", sum(vals), "with", (len(data))-sum(vals), "values missing"
    
    # creates the normalized bin counts
    percentage = data2[i].value_counts(sort = False, bins = range(int(data2[i].min()), int(data2[i].max()+binSize), binSize), normalize = True, dropna = False)
    print percentage
    print "total percentage", sum(percentage)
    

