import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
import collections

# Read the registration data
data = pd.read_csv('Registration Data Sem I 19-20(14.10.19).csv')

# Taking the required course as input
stream  = input('Enter the Stream of the course: (eg: BITS,HSS,CS,EEE,GS,etc) : ')
course_code = input('Enter the course code: (eg: F372,F464,F112,etc) : ')
target_course = stream+'    '+course_code

# Remove the columns which are not required
to_be_dropped = ['Semester','Descr','Lecture Section No','Practical Section No','Tutorial Section No','Project Section No','Thesis section','Graded Component','Grade In']
data = data.drop(to_be_dropped,axis=1)

# Combine Subject and Catalog column into one and remove both
data['cname'] = data['Subject'] + data['Catalog']
data = data.drop(['Subject','Catalog'],axis=1)

# Make a Dataframe of the class which you want to reschedule
os = data[data['cname']==(target_course)]

# Remove duplicate entries of same student for the same course
data = data.drop_duplicates(subset = ['ID','cname'],keep='first')
os = os.drop_duplicates(subset = ['ID','cname'],keep='first')

# Dictionary which stores the courses in which students 
# from the target class are registered apart from it
# along with the counts of no. of students in the intersection
course_counts_ID = {}

# Populating the course_counts_ID dictionary
for student in os['ID']:
    for courses in data[data['ID']==student]['Course ID']:
        if(courses in course_counts_ID):
            course_counts_ID[courses]+=1
        else:
            course_counts_ID[courses]=1

# Sort the dictionary in decreasing order
sorted_course_counts_ID = sorted(course_counts_ID.items(), key=operator.itemgetter(1),reverse=True)
sorted_course_counts_ID = collections.OrderedDict(sorted_course_counts_ID)

# Read the timetable csv
tt = pd.read_csv('Time Table Semester I 2019-20-29 July 19_5.csv')

# Create an empty numpy array to store our required answer table
slots = np.zeros((6, 13))

# Few dictionaries and lists made to simplify/prettify printing output
days={'M':0,'T':1,'W':2,'TH':3,'F':4,'S':5}
dayss = ['Mon','Tue','Wed','Thurs','Fri','Sat']
timeslices=['   ','8-9','9-10','10-11','11-12','12-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9']

# Function which checks whether the given input is a number or a string
def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

# Iterating over all the intersecting courses and 
# filling the number of students in them in appropriate 
# location in the timetable
for course in sorted_course_counts_ID.items():
    for i in tt[tt['COM CODE']==course[0]]['time'].index:
        stack = []
        for inp in tt['time'][i].split():
            if(check_int(inp)!=True):
                stack.append(inp)
            else:
                while(len(stack)!=0):
                    val = stack.pop()
                    slots[days[str(val)]][int(inp)-1]+=course[1]

# Printing the resulting timetable containing
# the number of students engaged in other courses
# in the given time slots. 

# We would want very less number of students to be engaged
# in other classes in the time slot in which we want to 
# reschedule our class.
for i in range(len(timeslices)):
    if(i==0):
        print("\t")
    print(timeslices[i],end="\t")
print("\n")
for i in range(len(slots)):
    print(dayss[i],end="\t")
    for j in range(len(slots[i])):
        print(int(slots[i][j]),end="\t")
    print("\n")