#!/usr/bin/python

read = open('years/all.txt', 'r')

data = {}

line = read.readline()

year = -1
while line != '':
    items = line.split(",")
    nonYear = items[0] + ", " + items[1] 

    if nonYear == "Mary, F":
        year = year + 1
        print year

    if nonYear in data:
        #add data
        while len(data[nonYear]) < year:
            data[nonYear].append(0)

        data[nonYear].append(int(items[2].replace("\r\n", "")))
    else:
        #create data
        data[nonYear] = [int(items[2].replace("\r\n", ""))]
        while len(data[nonYear]) < year:
            data[nonYear].insert(0,0)

    line = read.readline()


read.close()

#write data
write = open('allProcessed.csv', 'w')

for name, years in data.iteritems():
    line = name + ", " + str(years).strip('[]').replace("\r\n", "") + "\n"
    write.write(line)
    write.flush()

write.close()

