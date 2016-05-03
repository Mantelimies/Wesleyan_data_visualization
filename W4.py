'''
Python version 2.7.9
Author Joona R.
Date 2016/4/24
'''

import pandas as pd
import numpy as np
import seaborn
import matplotlib.pyplot as plt




data = pd.read_csv("gapminder.csv", low_memory = False, skipinitialspace = True)
print(len(data))
print(len(data.columns))
data2 = data.ix[:, ["country", "suicideper100th", "alcconsumption", "urbanrate", "incomeperperson"]] #subsetting the needed columns


#the composite variables "alcper1000dollar" and "suicideper100thper1000dollar" were left out from plotting on week4 
#data2["alcper1000dollar"] = data2["alcconsumption"] / (data2["incomeperperson"] / 1000) #adding the new composite variables
#data2["suicideper100thper1000dollar"] = data2["suicideper100th"] / (data2["incomeperperson"] / 1000)

### As the data is quite sparse and specific values would have been very few, I decided to divide the countries into ten bins starting from the smallest value and ending in the highest

# variables from my codebook
variables = ["suicideper100th", "alcconsumption", "urbanrate", "incomeperperson"] #the composite variables "alcper1000dollar" and "suicideper100thper1000dollar" were left out from plotting on week4 

# texts copied directly from the gapminder codebook
texts = {"suicideper100th" : "2005 Suicide, age adjusted, per 100 000. Mortality due to self-inflicted injury, per 100 000 standard population, age adjusted",
    "alcconsumption" : "2008 alcohol consumption per adult (age 15+), litres. Recorded and estimated average alcohol consumption, adult (15+) per capita consumption in litres pure alcohol",
    "urbanrate" : "2008 urban population (% of total) Urban population refers to people living in urban areas as defined by national statistical offices (calculated using World Bank population estimates and urban ratios from the United Nations World Urbanization Prospects)",
    "incomeperperson":"2010 Gross Domestic Product per capita in constant 2000 US$. The inflation but not the differences in the cost of living between countries has been taken into account.", "suicideper100thper1000dollar":"Ratio of suicides per income", "alcper1000dollar": "Ratio of alcohol consumption per income"}


shortTextsForPlots = {"suicideper100th" : "2005 Suicide per 100 000", "alcconsumption" : "2008 alcohol consumption per adult (age 15+), litres" ,
    "urbanrate" : "2008 urban population (% of total)", "incomeperperson":"2010 Gross Domestic Product per capita in constant 2000 US$", "suicideper100thper1000dollar":"Ratio of suicides per income", "alcper1000dollar": "Ratio of alcohol consumption per income"}


# creates a loop that goes through all the different variables
for i in variables:
    print "\n"
    # converts all the variables to numeric
    data2[i]=pd.to_numeric(data2[i])
    # make the binsize as 10 equally big parts based on the difference between the min and max values
    # my first attempt at dividing the binsize, easier to just use an integer: binSize = (data2[i].max()-data2[i].min())/10.0

    #prints the introtext for the variable
    print texts[i]

    # displays the range (min-max) of the single values and the countries they are from
    print "The values of", i, "range from", int(data2[i].min()), "in", data2.get_value(data2[i].argmin(), "country"), "to", int(data2[i].max()), "in", data2.get_value(data2[i].argmax(), "country")

    # creates the counts for each of the bins
    vals = data2[i].value_counts(sort = False, bins = 10, dropna = False) #here is my first attempt at the binsize-range, proved to be too silly: np.arange(data2[i].min(), data2[i].max()+binSize, binSize), binSize)
    print vals
    print "number of entries", sum(vals), "with", (len(data))-sum(vals), "values missing"

    # creates the normalized bin counts
    percentage = data2[i].value_counts(sort = False, bins = 10, normalize = True, dropna = False) #bins = np.arange(int(data2[i].min()), int(data2[i].max()+binSize), binSize)
    print percentage
    print "total percentage", sum(percentage)


#Week 4 tasks
shortTextsForPlots = {"suicideper100th" : "2005 Suicide per 100 000", "alcconsumption" : "2008 alcohol consumption per adult (age 15+), litres" ,
    "urbanrate" : "2008 urban population (% of total)", "incomeperperson":"2010 Gross Domestic Product per capita in constant 2000 US$"}

#describe the data
print data2.describe()



#W4 figure creation
plt.figure(1)

for i in variables:
    print "\n"
    #print median
    print "median for ", i, data2[i].median()
    #create the univariate graphs
    plt.subplot(len(variables)/2,2,variables.index(i)+1) 
    seaborn.distplot(data2[i].dropna(), kde=False)
    plt.xlabel(i)
    plt.title(shortTextsForPlots[i])


#creating the bivariate graphs
plt.figure(2)
plt.subplot(311)
seaborn.regplot(x="alcconsumption", y="suicideper100th", data = data2)
plt.xlabel(shortTextsForPlots["alcconsumption"])
plt.ylabel("2005 Suicide per 100 000")
plt.title("Scatterplot for the Association between Alcohol consumption and Suiciderate")

plt.subplot(312)
seaborn.regplot(x="urbanrate", y="suicideper100th", data = data2)
plt.xlabel(shortTextsForPlots["urbanrate"])
plt.ylabel("2005 Suicide per 100 000")
plt.title("Scatterplot for the Association between Alcohol consumption and Urban rate")

data2["logInc"] = np.log(data2["incomeperperson"])
plt.subplot(313)
seaborn.regplot(x=("logInc"), y=("suicideper100th"), data = data2)
plt.xlabel("log of 010 Gross Domestic Product per capita in constant 2000 US$")
plt.ylabel("2005 Suicide per 100 000")
plt.title("Scatterplot for the Association between Alcohol consumption and Income per person")




plt.show()
