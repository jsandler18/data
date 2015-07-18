#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
name = sys.argv[1]
sex = sys.argv[2]

f = open('allProcessed.csv', 'r')
line = f.readline()

while line.find(name + ", " + sex) == -1:
    line = f.readline()

f.close()

data = line.split(",")

data.remove(name)
data.remove(" "+ sex)

a = 0
for i in data:
    data[a] = i.strip(" ")
    a = a + 1

data[len(data)-1] = data[len(data)-1].strip("\n")

a = 0
for i in data:
    data[a] = int(i)
    a = a + 1


years = []

for i in range(1880, 2015):
    years.append(i)

plt.plot(years, data)
plt.title(name)
plt.xlabel("Year")
plt.ylabel("Frequency of name: %s" % name)
plt.show()

