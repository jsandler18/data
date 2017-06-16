from bs4 import BeautifulSoup
import urllib2
import sqlite3
from progressbar import ProgressBar
import re

pbar = ProgressBar()

response = urllib2.urlopen('https://ntst.umd.edu/soc/201608')
html = response.read()
response.close()

soup = BeautifulSoup(html, 'html.parser')

conn = sqlite3.connect("courses.db")
c = conn.cursor()

#c.execute("drop table subjects")
#c.execute("drop table courses")
#c.execute("drop table sections")

#has id, shortname and long name fields
c.execute("create table subjects (subjectid integer primary key, shortname text, longname text)")
#has id, course number (must be text for things like 100H), course name, credits, and subject fields
c.execute("create table courses (courseid integer primary key, number text, name text, credits integer, coursesubject integer, foreign key(coursesubject) references subjects(subjectid))")
#has id, section number, teacher, starttime, endtime, days of the week, building, room number, and course fields
c.execute("create table sections (sectionid integer primary key, number integer, teacher text, starttime text, endtime text, days text, building text, room integer, starttime2 text, endtime2 text, days2 text, building2 text, room2 text, sectioncourse integer, foreign key(sectioncourse) references courses(courseid))")

#keeps short subject names to make links out of
subjectlist = []

#populate subjects table
for i in soup.find_all('div', 'course-prefix row'):
    shortsub = i.find('span', 'prefix-abbrev push_one two columns').get_text()
    longsub = i.find('span', 'prefix-name nine columns').get_text()

    c.execute("insert into subjects(shortname, longname) values (?, ?)", (shortsub, longsub))

    subjectlist.append(shortsub)


    
#got to each subject page and read course info
for i in pbar(subjectlist):
    response = urllib2.urlopen('https://ntst.umd.edu/soc/201608/%s' % i)
    html = response.read()
    response.close()

    soup = BeautifulSoup(html, 'html.parser')

    #loop through the courses and add numbers to a list
    course_numbers = []

    for course in soup.find_all('div', 'course'):
        course_number = course['id'][4:]
        course_numbers.append(course_number)


    for co in course_numbers:
        response = urllib2.urlopen('https://ntst.umd.edu/soc/201608/%s/%s' % (i, i + str(co),))
        html = response.read()
        response.close()
        
        soup = BeautifulSoup(html, 'html.parser')

        course = soup.find('div', 'course')

        course_name = course.find('span', 'course-title').get_text()
        credits = course.find('span', 'course-min-credits').get_text() 
        c.execute("select subjectid from subjects where shortname=?", (i,))
        subject_id = c.fetchone()[0]
        
        c.execute("insert into courses(number, name, credits, coursesubject) values (?, ?, ?, ?)", (co, course_name, credits, subject_id,))

        #loop through the sections and extract their info
        for section in course.find_all('div', 'section'):
            section_number = section.find('span', 'section-id').get_text()
            section_teacher = section.find('span', 'section-instructors').get_text().strip()
            section_teacher = ", ".join(re.split("\W+ \W+", section_teacher))
            
            starts = section.find_all('span', 'class-start-time')
            ends = section.find_all('span', 'class-end-time')
            days = section.find_all('span', 'section-days')
            buildings = section.find_all('span', 'building-code')
            rooms = section.find_all('span', 'class-room')
            c.execute("select courseid from courses where number=? and coursesubject=?", (co, subject_id,))
            course_id = c.fetchone()[0]
            
            start1 = 'null' if len(starts) == 0 else starts[0].get_text()
            end1 = 'null' if len(ends) == 0 else ends[0].get_text()
            day1 = 'null' if len(days) == 0 else days[0].get_text()
            building1 = 'null' if len(buildings) == 0 else buildings[0].get_text()
            room1 = 'null' if len(rooms) == 0 else rooms[0].get_text()

            start2 = 'null' if len(starts) < 2 else starts[1].get_text()
            end2 = 'null' if len(ends) < 2 else ends[1].get_text()
            days2 = 'null' if len(days) < 2 else days[1].get_text()
            building2 = 'null' if len(buildings) < 2 else buildings[1].get_text()
            room2 = 'null' if len(rooms) < 2 else rooms[1].get_text()
            
            c.execute("insert into sections(number, teacher, starttime, endtime, days, building, room, starttime2, endtime2, days2, building2, room2, sectioncourse) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (section_number, section_teacher, start1, end1, day1, building1, room1, start2, end2, days2, building2, room2, course_id,))


conn.commit()
conn.close()
