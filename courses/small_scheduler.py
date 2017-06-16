from courses import *
from sys import argv
import re
from math import ceil
"""This script expects valid courses as arguments and tries to form a schedule 
from those arguments"""

"""takes a string of time in the standard '12:30pm' standard way and coverts it 
to an index in an array representing time of day starting at 6am with 15 minute 
intervals"""
def time_to_index(time):
    (hour,minute,ampm) = re.match("(\d+):(\d+)(am|pm)", time).groups()
    if ampm == "pm":
        if hour != "12":
            hour = str(int(hour)+12)
    else:
        if hour == "12":
            hour = "00"

    return int(4*(int(hour) - 6) + (ceil(4*int(minute)/60.0)))
            
"""checks if the given list of sections has any conflicts"""
def no_conflicts(section_list):
    #init 2d array of 5 days with 16 hour days with 15 minute segments
    #if true, then time slot is filled
    schedule = [[false for x in range(16*15)] for x in range(5)]
    for section in section_list:
        for idx,timeframe in enumerate(section_list.lecture.itervalues()):
            if timeframe != None:
                starttime = time_to_int(timeframe[0])
                endtime = time_to_int(timeframe[1])
                for time in range(starttime, endtime):
                   if schedule[idx,time]:
                       return false
                   else:
                       schedule[idx,time] = True

    return True
                
"""returns a list of possible schedules, each of which is a list of sections"""
def get_schedules(course_list):
    current_schedule = [] #keeps track of which sections I am working with now
    schedules = []
    for course in course_list:

    

argv.pop(0)
courses = []

#read arguments into course objects
for course in argv:
    #match against patterns such as CMSC351 and math 246
    subj_num = re.match("([A-Za-z]+)\s*(\d+[A-Za-z]?)",course).groups()
    if subj_num == None:
        print "%s is invalid format" % course
        exit(1)

    subj = Subject(subj_num[0])
    
    course = subj.find(subj_num[1])
    if course != None:
        courses.append(course)



