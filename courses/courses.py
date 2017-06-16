import sqlite3

class Section:
    """A class to represent a specific section of a course."""
    def __init__(self, course, number, teacher, lecturestarttime, lectureendtime, lecturedays, lecturebuilding, lectureroom, discstarttime=None, discendtime=None, discdays=None, discbuilding=None, discroom=None):
        self.number = number
        self.course = course
        self.teacher = teacher.strip()
        #initialize a dictionary that keeps section start/endtimes associated with days
        self.lecture = {'M':None, 'Tu':None, 'W':None,'Th':None,'F':None}
        self.lecture['M'] = (lecturestarttime, lectureendtime) if lecturedays.find('M') != -1 else None
        self.lecture['Tu'] = (lecturestarttime, lectureendtime) if lecturedays.find('Tu') != -1 else None
        self.lecture['W'] = (lecturestarttime, lectureendtime) if lecturedays.find('W') != -1 else None
        self.lecture['Th'] = (lecturestarttime, lectureendtime) if lecturedays.find('Th') != -1 else None
        self.lecture['F'] = (lecturestarttime, lectureendtime) if lecturedays.find('F') != -1 else None
        self.lecturebuilding = lecturebuilding
        self.lectureroom = lectureroom
        #init a dictionary like the one above, but for the discussion section
        self.disc = {'M':None, 'Tu':None, 'W':None,'Th':None,'F':None}
        self.disc['M'] = (discstarttime, discendtime) if discdays.find('M') != -1 else None
        self.disc['Tu'] = (discstarttime, discendtime) if discdays.find('Tu') != -1 else None
        self.disc['W'] = (discstarttime, discendtime) if discdays.find('W') != -1 else None
        self.disc['Th'] = (discstarttime, discendtime) if discdays.find('Th') != -1 else None
        self.disc['F'] = (discstarttime, discendtime) if discdays.find('F') != -1 else None
        self.discbuilding = discbuilding if discbuilding != 'null' else None        
        self.discroom = discroom if discroom != 'null' else None

    def __str__(self):
        string = "%s\t%s\t%s\t%s %s\t" % (self.course,str(self.number), self.teacher.strip(), self.lecturebuilding, str(self.lectureroom))

        for key, value in self.lecture.iteritems():
            string = string + ("" if value == None else (key + ": " +  value[0] 
                + " - " + value[1] + ", "))
        
        if self.discbuilding != None and self.discroom != None:
            string = string + "\t%s %s\t" % (self.discbuilding, str(self.discroom))

        for key, value in self.disc.iteritems():
            string = string + ("" if value == None else (key + ": " + value[0] + 
                " - " + value[1] + ", "))

        return string

class Course:
    """A class to represent a course of a specific subject"""
    def __init__(self, subject, number):
        self.number = number
        self.subject = subject
        
        #connect to the database and get a list of sections for this course
        conn = sqlite3.connect("courses.db")
        c = conn.cursor()
        c.execute("select subjectid from subjects where shortname=?", (subject,))
        c.execute("select courseid, name, credits from courses where coursesubject=? and number=?", (c.fetchone()[0],number,))
        out = c.fetchone()
        c.execute("select * from sections where sectioncourse=?", (out[0],))

        self.name = out[1]
        self.credits = out[2]

        dbsections = c.fetchall()
        c.close()

        self.sections = []
        for dbsec in dbsections:
            self.sections.append(Section("%s%s" %(self.subject,self.number),dbsec[1], dbsec[2], dbsec[3], dbsec[4], dbsec[5], dbsec[6], dbsec[7], dbsec[8], dbsec[9], dbsec[10], dbsec[11], dbsec[12]))

    def __str__(self):
        string = "%s%s: %s\n%d credits\n\n" % (self.subject, self.number, self.name ,self.credits)
    
        for i in self.sections:
            string = string + str(i.number) + " "

        return string


class Subject:
    """A calss representing a subject, which has courses"""
    def __init__(self, shortname):
        self.shortname = shortname
        
        #connect to database to fill out courses
        conn = sqlite3.connect("courses.db")
        c = conn.cursor()
    
        c.execute("select longname, subjectid from subjects where shortname=?", (shortname,))
        out = c.fetchone()
        
        #raise a value error if the shortname is not found in the database
        if out == None:
            raise ValueError

        self.longname = out[0]
        subjectid = out[1]

        c.execute("select number from courses where coursesubject=?", (subjectid,))
        
        dbcourses = c.fetchall()

        c.close() 

        self.courses = []
        for i in dbcourses:
            self.courses.append(Course(shortname, i[0]))

    def __str__(self):
        string = "%s: %s\n" % (self.shortname, self.longname)
        for i in self.courses:
            string = string + i.number + " "
        return string
        
    """finds a course by the given number in this subject.  Returns a course object of the course if it is present, None if it is not"""
    def find(self, number):
    
        if type(number) is int:
            number = str(number)        

        for i in self.courses:
            if i.number == number:
                return i

        return None    

"""returns a list of strings that are the availible subjects to make subject objects from"""        
def subject_list():
    conn = sqlite3.connect("courses.db")
    c = conn.cursor()

    c.execute("select shortname from subjects");
    
    out = c.fetchall()

    subjects = []

    for i in out:
        subjects.append(i[0])
    
    c.close()

    return subjects

