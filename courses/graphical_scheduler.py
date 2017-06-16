from courses import *
from Tkinter import *

class CourseFrame(Frame):
    """A frame to hold a single course. it will let you choose a subject, then a course, then a section.  
    It will sit as a section once those are chosen and the section 
    can be changed when clided on, but it can't change course"""
    def __init__(self, parent):
        Frame.__init__(self, parent)   

        #init course info fields to None
        self.subject = None
        self.course = None
        self.section = None
             
        #init this fram with a listbox of the subjects
        self.parent = parent
        
        self.button = Button(self, command=self.reselect_section)
        self.remove = Button(self, text="X", command=self.destroy)
        self.remove.pack(side=RIGHT, fill=Y)
        
        self.label = Label(self, text="Select Subject")
        self.label.pack(side=TOP, fill=X)

        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self, selectmode=SINGLE)
        self.listbox.pack(side=TOP) 


        for i in subject_list():
            self.listbox.insert(END, i)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
    
        #poll for subject
        self.get_selected_sub()

    def get_selected_sub(self):
        now = self.listbox.curselection()
        if len(now) != 1:
            self.after(250, self.get_selected_sub)
        else:
            #set subject, change listbox to contain courses
            self.subject = Subject(self.listbox.get(now[0]))
            self.label.config(text = "Select Course")
            self.listbox.delete(0, END)
            for i in self.subject.courses:
                self.listbox.insert(END, "%s%s: %s" %(i.subject, i.number, i.name))
            #poll for course 
            self.get_selected_course()

    def get_selected_course(self):
        now = self.listbox.curselection()
        if len(now) != 1:
            self.after(250, self.get_selected_course)
        else:
            #set subject, change listbox to contain courses
            self.course = self.subject.courses[now[0]] 
            self.label.config(text = "Select Section")
            self.listbox.delete(0, END)
            for i in self.course.sections:
                lecture_time_string = ""
                disc_time_string = ""
                
                for key, value in i.lecture.iteritems():
                    if value != None:
                        if len(lecture_time_string):
                            lecture_time_string = value[0] + "-" + value[1] + " " + key 
                        else:
                            lecture_time_string = lecture_time_string + key

                for key, value in i.disc.iteritems():
                    if value != None:
                        if len(disc_time_string):
                            disc_time_string = value[0] + "-" + value[1] + " " + key 
                        else:
                            disc_time_string = lecture_time_string + key
                        
                     
                self.listbox.insert(END, "Section: %d\t%s\nTeacher: %s\t%s" % (i.number, lecture_time_string, i.teacher, disc_time_string))

            #poll for section
            self.get_selected_section()

    def get_selected_section(self):
        now = self.listbox.curselection()
        if len(now) != 1:
            self.after(250, self.get_selected_section)
        else:
            #set subject
            self.section = self.course.sections[now[0]]
            #remove listbox, make button
            self.button.config(text = self.listbox.get(ACTIVE)) 
            self.listbox.pack_forget()
            self.label.pack_forget()
            self.scrollbar.pack_forget()
            self.button.pack(side=TOP)
            

    def reselect_section(self):
        self.label.config(text = "Select Section")
        self.button.pack_forget()
        self.label.pack(side=TOP, fill=X)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=TOP)
        self.listbox.delete(0, END)
        for i in self.course.sections:
            lecture_time_string = ""
            disc_time_string = ""
            
            for key, value in i.lecture.iteritems():
                if value != None:
                    if len(lecture_time_string):
                        lecture_time_string = value[0] + "-" + value[1] + " " + key 
                    else:
                        lecture_time_string = lecture_time_string + key

            for key, value in i.disc.iteritems():
                if value != None:
                    if len(disc_time_string):
                        disc_time_string = value[0] + "-" + value[1] + " " + key 
                    else:
                        disc_time_string = lecture_time_string + key
                    
                 
            self.listbox.insert(END, "Section: %d\t%s\nTeacher: %s\t%s" % (i.number, lecture_time_string, i.teacher, disc_time_string))

        #poll for section
        self.get_selected_section()

    def destroy(self):
        self.pack_forget()
        self.button.destroy()
        self.remove.destroy()
        self.listbox.destroy()
        self.label.destroy()
        self.scrollbar.destroy()
        self.parent.courseframelist.remove(self)
        Frame.destroy(self)

class CourseListFrame(Frame):
    """A fram to hold the add button and the multiple courses being displayed in the schedule"""
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
      
        self.add_button = Button(self, text="Add Course", command=self.add_course)
        self.add_button.pack(side=TOP)

        self.courseframelist = []

    def add_course(self):
        c = CourseFrame(self)
        c.pack(side=TOP)
        self.courseframelist.append(c)
         
class SectionFrame(Frame):
    """A frame to represent a section on the schedule, only on one day at one time"""
    def __init__(self, parent, start, end, building, room):
        Frame.__init__(self, parent)   

        self.parent = parent    
    
        self.starttime = start
        self.endtime = end
        self.building = building
        self.room = room

        self.time = Label(self, text=starttime + "-" + endtime)
        self.place = Label(self, text =building + " " + room)

        time.pack(side=TOP, fill=X)
        place.pack(side=TOP, fill=X)
    
    def destroy(self):
        self.grid_forget()
        self.time.destroy()
        self.place.destroy()
        Frame.destroy(self)

class WeekFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
    

def main():
    root = Tk()

    courselistframe = CourseListFrame(root)
    week = WeekFrame(root)
    week.pack(side=LEFT)
    courselistframe.pack(side=LEFT)
    root.mainloop()



main()
