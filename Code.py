#***********************************************London Underground Station Routes********************************************************************
#
#                          The program finds the fastest route between any two London underground stations.
#                          It also handles any closed lines or out of service stations conditions
#
#Module imports.
import sys
import csv, operator
import copy

import heapq
from heapq import heapify,heappush,heappop

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#Initialization
#variables
station_file = 'londonstations.csv'
connections_file = 'londonconnections.csv'
lines_file = 'londonlines.csv'

#Lists
station_names=[]
station_ids_names=[]
station_id_list=[]
nodes_delete_list=[]

lines_id=[]
line_names=[]
lines_id_name=[]
edges_time=[]
lines_edges_time=[]
delete_lines=[]
edges_delete_list=[]

unvisited_stations=[]
visited_stations=[]
minheap=[]
Route_names=[]

#Dictionaries
graph_data={}

#Get input data from the database (CSV files)
try:
    
    with open(station_file,newline='') as stations:
         inp1 = csv.reader(stations, delimiter=',')
         header=next(inp1)
         SortedStations=sorted(inp1,key=operator.itemgetter(0))

         for row in SortedStations:
             station_id_list.append(row[0])
             station_names.append(row[3])
             station_ids_names.append([row[3],row[0]])
             
except (FileNotFoundError,IOError):
    if IOError:
        print('Error during the file open ' , station_file)
    if FileNotFoundError:
        print(station_file , ' No such file found in the directory')

try:
    
    with open(connections_file,newline='') as connections:
         inp2 = csv.reader(connections,delimiter=",")
         header=next(inp2)

         for data in inp2:
             edges_time.append([data[0],data[1],int(data[3])])
             lines_edges_time.append([data[2],data[0],data[1],int(data[3])])

except (FileNotFoundError,IOError):
    if IOError:
        print('Error during the file open ' , connections_file)
    if FileNotFoundError:
        print(connections_file , ' No such file found in the directory')

try:
    
    with open(lines_file,newline='') as lines:
         inp3 = csv.reader(lines,delimiter=",")
         header=next(inp3)

         for line in inp3:
             lines_id.append(line[0])
             lines_id_name.append([line[0],line[1]])
             line_names.append(line[1])

except (FileNotFoundError,IOError):
    if IOError:
        print('Error during the file open ' , lines_file)
    if FileNotFoundError:
        print(lines_file , ' No such file found in the directory')

station_names.sort()
line_names.sort()
graph_data=dict.fromkeys(station_id_list)
dict_connections=dict.fromkeys(lines_id)



#Data Structure:
#create graph and update for any unavailable stations/lines

class Graph_Construction:
    def __init__(self, graph_data):
        self.graph_data=graph_data
        self.edges_delete_list=edges_delete_list

        for node in self.graph_data:
            self.graph_data[node]=[]

    def add_connection(self,s1,s2,cost):
        templist1=[s2,cost]
        templist2=[s1,cost]
        if s1 in self.graph_data:
            self.graph_data[s1].append(templist1)
        if s2 in self.graph_data:
            self.graph_data[s2].append(templist2)

            
    def delete_station(self,st_delete):
        if st_delete not in self.graph_data:
            print("station id", st_delete, "does not exist in the graph")
        else:
            self.graph_data.pop(st_delete)
            for i in self.graph_data:
                templist3=self.graph_data[i]
                for j in templist3:
                    if j[0] == st_delete:
                        while j in templist3:
                            templist3.remove(j)

    def del_connection_list(self,closedline):
        for i in dict_connections[closedline]:
            if i not in self.edges_delete_list:
                self.edges_delete_list.append(i)

                      
    def delete_connection(self,st1,st2,cost):
        if st1 not in self.graph_data:
            print("station id ", st1, "does not exist")
        elif st2 not in self.graph_data:
            print("station id ", st2, "does not exist")
        else:
            templist4=[st1,cost]
            templist5=[st2,cost]
            if templist5 in self.graph_data[st1]:
                self.graph_data[st1].remove(templist5)
                self.graph_data[st2].remove(templist4)

    
    def print_graph_data(self):
        for node in self.graph_data:
            print(node, "->" ,self.graph_data[node])


graph=Graph_Construction(graph_data)

time_to_reach=dict.fromkeys(graph_data)
Route_ids=dict.fromkeys(graph_data)
for station_id in Route_ids.keys():
    Route_ids[station_id]=[]
         

#Fastest Route

def algorithm(graph_data,source,dest):
    infinity=sys.maxsize
    for i in graph_data.keys():
        time_to_reach[i]=infinity
        time_to_reach[source]=0
        unvisited_stations.append(i)
        current=source

    while len(unvisited_stations) > 0:
        
        if current not in visited_stations:
                visited_stations.append(current)

        try:

            for neighbour in graph_data[current]:
                adjnode=neighbour[0]
                adjtime=neighbour[1]
                if adjnode not in visited_stations:
                    if adjtime + time_to_reach[current] < time_to_reach[adjnode]:
                        time_to_reach[adjnode] = adjtime + time_to_reach[current]
                        Route_ids[adjnode].append([current])
                        heappush(minheap,(time_to_reach[adjnode],adjnode))

                if current in unvisited_stations:
                    unvisited_stations.remove(current)
              
            heapify(minheap)
            current=minheap[0][1]
            heappop(minheap)
            
        except (KeyError,IndexError):
            if KeyError:
                print("Runtime KeyError: Error when trying to access the database with station id ", current)
            if IndexError:
                print("Runtime IndexError occurred")

#Calling the Data structure & algorithm portions for execution
            
def execute():

#graph creation - using station ids and the time
    for s1, s2, cost in edges_time:
        graph.add_connection(s1,s2,cost)

#get station ids for the unavailable station names
    for st_name in unavailable_stations:
        for i in station_ids_names:
            if st_name == i[0]:
                nodes_delete_list.append(i[1])
                
#perform delete stations        
    if len(nodes_delete_list) > 0:
        for st_del in nodes_delete_list:
            graph.delete_station(st_del)

#get connections/time for the unavailable line names
    for i in dict_connections:
        dict_connections[i]=[]
        for j in lines_edges_time:
            if i == j[0]:
                dict_connections[i].append([j[1],j[2],j[3]])

    for line_name in unavailable_lines:
        for id in lines_id_name:
            if line_name == id[1]:
                delete_lines.append(id[0])

#prepare connections list for deletion    
    for closedline in delete_lines:
        graph.del_connection_list(closedline)

#perform delete connections    
    if len(edges_delete_list) > 0:
        for st1, st2, cost in edges_delete_list:
            graph.delete_connection(st1,st2,cost)
            
#find the fastest route
    algorithm(graph_data,source,dest)

    

#GUI
#get/validate input, print output
    
def print_output():
    output_page=Toplevel(bg='white')
    
    commute = str(st_from)+"--->"+str(st_to)
    quickest = "Quickest time to reach the destination : " + str(time_to_reach[dest])+ " minute(s)"

    Commute=Label(output_page, text=commute, font=('arial',16),fg="green")
    Commute.grid(row=4,column=0)

    Time=Label(output_page, text=quickest, font=('arial',10),fg="green")
    Time.grid(row=5,column=0)


    for path_list in Route_ids[dest]:
        for path_id in path_list:
            for i in station_ids_names:
                if i[1] == path_id:
                    Route_names.append(i[0])
    path = "The Route is: "+ str(Route_names)



    Route=Label(output_page, text=path, font=('arial',10),fg="green")
    Route.grid(row=6,column=0)
    
def get_station_id():
    global source
    global dest

    
    if error == False:
        templist=station_ids_names
        for i in templist:
            if st_from == i[0]:
                source = i[1]
            if st_to == i[0]:
                dest = i[1]
    
        execute()

        print_output()
    
def verify_input():
    global error
    error = False


    if len(st_from) == 0:
        messagebox.showinfo("Station not selected", 'Select a From station')
        error = True
    if len(st_to) == 0:
        messagebox.showinfo("Station not selected", 'Select a To Station')
        error = True

    if len(st_from) > 0:
        if len(st_to) > 0:
            if st_from == st_to:
                messagebox.showinfo("Same Stations Error", 'From and To Stations cannot be the same')
                error = True

    if st_from in unavailable_stations:
        messagebox.showinfo("Same Stations Error", 'From Station cannot be the out of service station')
        error = True
    if st_to in unavailable_stations:
        messagebox.showinfo("Same Stations Error", 'To Station cannot be the out of service station')
        error = True

    get_station_id()
    
    return error

        
def get_input():
    global st_from
    global st_to
    global unavailable_lines
    global unavailable_stations
    
    st_from=start_station.get()
    st_to=end_station.get()
    

    closed_lines=lbox.get(0,tk.END)
    unavailable_lines=[closed_lines[i] for i in lbox.curselection()]

    
    closed_stations=sbox.get(0,tk.END)
    unavailable_stations=[closed_stations[i] for i in sbox.curselection()]


    verify_input()
 
    return st_from,st_to,unavailable_lines,unavailable_stations


#GUI - Tkinter Design

def submit_window():
    global start_station
    global end_station
    
    Submit_page=Tk()
    Submit_page.geometry("500x500")
    Submit_page.title("Submit Page")
    Submit_page.config(bg="white")


    Title = Label(Submit_page, text='Please select your source and destination',font=('arial',12),fg="white",bg="dark blue")
    Title.grid(row=1,column=1)

    From_Station=Label(Submit_page, text='From Station',font=('arial',12),fg="white",bg="dark blue")
    From_Station.grid(row=3,column=0)

    To_Station=Label(Submit_page, text='To Station', font=('arial',12),fg="white",bg="dark blue")
    To_Station.grid(row=4,column=0)

    options=station_names
    start_station=ttk.Combobox(Submit_page,value=options,width=20)
    start_station.grid(row=3,column=1)

    options=station_names
    end_station=ttk.Combobox(Submit_page,value=options,width=20)
    end_station.grid(row=4,column=1)

    submit=Button(Submit_page,text="Submit",bg="dark blue",fg="white",command=get_input)
    submit.grid(row=5,column=1)


    
#Home Page    
Home_Page=Tk()
Home_Page.geometry("500x500")
Home_Page.title("London Underground Route Finder")
Home_Page.config(bg="White")

Title = Label(Home_Page, text='Welcome to London Underground Station Routes', font=('arial',16),fg="white",bg="dark blue")
Title.pack(pady=7)

Text = Label(Home_Page, text='Please select unavailable stations / lines if any', font=('arial',12),fg="white",bg="dark blue")
Text.pack(pady=7)

Stations_Text = Label(Home_Page, text='Unavailable stations', font=('arial',10),fg="white",bg="dark blue")
Stations_Text.pack(padx=10)
    
Stations_frame=Frame(Home_Page)
Stations_frame.pack()

vscroll=Scrollbar(Stations_frame,orient=VERTICAL)
hscroll=Scrollbar(Stations_frame,orient=HORIZONTAL)

options=station_names
sbox=Listbox(Stations_frame,width=25,height=10,selectmode=MULTIPLE,yscrollcommand=vscroll.set,xscrollcommand=hscroll.set,exportselection=False)
sbox.pack(pady=5)

for data in station_names:
    sbox.insert(END,data)

vscroll.config(command=sbox.yview)
vscroll.pack(side=RIGHT,fill=Y)
   
hscroll.config(command=sbox.xview)
hscroll.pack(side=BOTTOM,fill=X)

Lines_Text = Label(Home_Page, text='Unavailable Lines', font=('arial',10),fg="white",bg="dark blue")
Lines_Text.pack()

Lines_frame=Frame(Home_Page)
Lines_frame.pack()

yscroll=Scrollbar(Lines_frame,orient=VERTICAL)
xscroll=Scrollbar(Lines_frame,orient=HORIZONTAL)

options=line_names
lbox=Listbox(Lines_frame,width=25,height=10,selectmode=MULTIPLE,yscrollcommand=yscroll.set,xscrollcommand=xscroll.set,wrap=None,exportselection=False)
lbox.pack(pady=5)

for data in line_names:
    lbox.insert(END,data)

yscroll.config(command=lbox.yview)
xscroll.pack(side=RIGHT,fill=Y)
   
yscroll.config(command=lbox.xview)
xscroll.pack(side=BOTTOM,fill=X)


submit=Button(Home_Page,text="Next",bg="darkblue",fg="white",command=submit_window)
submit.pack()


Home_Page.mainloop()
