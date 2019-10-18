import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
import collections

data = pd.read_csv('Registration Data Sem I 19-20(14.10.19).csv')

to_be_dropped = ['Semester','Descr','Lecture Section No','Practical Section No','Tutorial Section No','Project Section No','Thesis section','Graded Component','Grade In']
data = data.drop(to_be_dropped,axis=1)

data['cname'] = data['Subject'] + data['Catalog']
data = data.drop(['Subject','Catalog'],axis=1)

os = data[data['cname']=='CS    F372']

data = data.drop_duplicates(subset = ['ID','cname'],keep='first')
os = os.drop_duplicates(subset = ['ID','cname'],keep='first')

course_counts_ID = {}

for student in os['ID']:
    for courses in data[data['ID']==student]['Course ID']:
        if(courses in course_counts_ID):
            course_counts_ID[courses]+=1
        else:
            course_counts_ID[courses]=1

sorted_course_counts_ID = sorted(course_counts_ID.items(), key=operator.itemgetter(1),reverse=True)
sorted_course_counts_ID = collections.OrderedDict(sorted_course_counts_ID)

tt = pd.read_csv('Time Table Semester I 2019-20-29 July 19_5.csv')

days={'M':0,'T':1,'W':2,'TH':3,'F':4,'S':5}
slots = np.zeros((6, 13))
dayss = ['Mon','Tue','Wed','Thurs','Fri','Sat']
timeslices=['   ','8-9','9-10','10-11','11-12','12-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9']

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

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

