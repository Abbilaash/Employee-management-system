########################################################
#              THIS IS AN OASIS CREATION               #
# DEVELOPER: ABBILAASH A T                             #
# LANGUAGE OF CREATION: PYTHON, SQL                    #
# FRAMEWORK: Tkinter, CustomTkinter, MySQL             #
########################################################


#importing the needed modules
import tkinter as tk
from tkinter import *
import customtkinter
from PIL import ImageTk, Image
from tkinter import messagebox
import mysql.connector 
from tkinter import filedialog
import os
from tkinter import ttk
import smtplib
import pickle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


#Entering my MySQL access data (localhost - XAMPP)
# server: Apache
# database: MySQL
USER = "root"
PASSWD = ""
DB = "employee_management"
HOSTNAME = "localhost"

window = tk.Tk()
window.geometry('1250x718')
window.resizable(0, 0)
window.state('zoomed')
window.title("OASIS Employee Management")

def data_extract():
    #create a connection
    myconn = mysql.connector.connect(host=HOSTNAME,user=USER,password=PASSWD,database=DB)
    cursor = myconn.cursor()
    cursor.execute("SELECT * FROM employees;")
    #create the lists to store the fetched data
    global EMPL_DATA
    EMPL_DATA = {}
    #split and store the data in appropriate list
    data_collection = cursor.fetchall()
    #create the employee name list for future purpose
    global empl_name_list
    empl_name_list = []
    for data in data_collection:
        EMPL_DATA['EMPL_ID'] = data[0]
        EMPL_DATA['EMPL_NAME'] = data[1]
        EMPL_DATA['EMPL_AGE'] = data[2]
        EMPL_DATA['EMPL_BLOODGRP'] = data[3]
        EMPL_DATA['EMPL_ADDRESS'] = data[4]
        EMPL_DATA['EMPL_GENDER'] = data[5]
        EMPL_DATA['EMPL_DOB'] = data[6]
        EMPL_DATA['EMPL_JOINDATE'] = data[7]
        EMPL_DATA['EMPL_EMAIL'] = data[8]
        EMPL_DATA['EMPL_PHONE'] = data[9]
        EMPL_DATA['EMPL_DEPT'] = data[10]
        EMPL_DATA['EMPL_SALARY'] = data[11]
        EMPL_DATA['EMPL_PICTURE'] = data[12]

        empl_name_list.append(data[1])
    
    #return the final data
    myconn.close()
    return EMPL_DATA


#################################################################################

def app():

    global side_options_frame, top_navbar, file_path

    side_options_frame = Frame(window, bg="gray13",width=200)
    side_options_frame.place(x=0,relheight=1)
    side_options_frame.pack_propagate(False)
    top_line = Canvas(side_options_frame, height=1, bg="gray4", highlightthickness=0)
    top_line.place(x=0,y=49,relwidth=1)

    top_navbar = Frame(window, bg="gray4",height=50)
    top_navbar.place(x=200,y=0,relwidth=1)

    text_var = tk.StringVar(value="💲O-Travail")
    logo_label = customtkinter.CTkLabel(master=side_options_frame,
                               textvariable=text_var,
                               fg_color=("gray13", "gray13"),
                               font=("Abbyssinica SIL",30),
                               corner_radius=8)
    logo_label.place(x=0,y=5,relwidth=0.9)

    global file_path
    file_path = os.path.dirname(os.path.realpath(__file__))

    dashboard_btn_img = customtkinter.CTkImage(Image.open(file_path + "/assets/dashboard_icon.png"),size=(20,20))
    workers_btn_img = customtkinter.CTkImage(Image.open(file_path + "/assets/members_icon.png"),size=(20,20))
    email_btn_img = customtkinter.CTkImage(Image.open(file_path + "/assets/email_icon.png"),size=(22,22))

    dashboard_btn = customtkinter.CTkButton(master=side_options_frame,command=dashboard_func,anchor="sw",hover_color="gray20",image=dashboard_btn_img,fg_color="gray13",compound="left",height=40,text_color="white",font=("yu gothic ui", 19,"bold"),text="  Dashboard",corner_radius=8)
    dashboard_btn.place(x=5,y=70,relwidth=0.99)

    workers_btn = customtkinter.CTkButton(master=side_options_frame,command=workers_func,anchor="sw",hover_color="gray20",image=workers_btn_img,fg_color="gray13",text_color="white",compound="left",height=40,font=("yu gothic ui", 19,"bold"),text="  Employees",corner_radius=8)
    workers_btn.place(x=5,y=130,relwidth=0.99)

    email_btn = customtkinter.CTkButton(master=side_options_frame,command=email_func,anchor="sw",hover_color="gray20",image=email_btn_img,fg_color="gray13",text_color="white",compound="left",height=40,font=("yu gothic ui", 19,"bold"),text="  Email",corner_radius=8)
    email_btn.place(x=5,y=190,relwidth=0.99)



    dashboard_func()


def dashboard_func():
    dashboard_main_frame = customtkinter.CTkFrame(master=window, fg_color="gray63")
    dashboard_main_frame.place(x=200,y=50,relheight=1,relwidth=1)

    empl_dashboard_lbl = customtkinter.CTkLabel(master=dashboard_main_frame,
                                                text="Dashboard",
                                                font=("yu gothic ui", 24,"bold"),
                                                fg_color="gray63",
                                                height=50,
                                                width=200,
                                                text_color="black")
    empl_dashboard_lbl.place(x=30,y=20)

    employee_count_frame = customtkinter.CTkFrame(master=dashboard_main_frame,
                                                  fg_color="gray74",
                                                  width=300,
                                                  height=90)
    employee_count_frame.place(x=30,y=90)

    global empl_count_icon_photo
    empl_count_icon = Image.open('assets/employee_count_icon.png').resize((45,45))
    empl_count_icon_photo = ImageTk.PhotoImage(empl_count_icon)
    empl_count_img_lbl = Label(employee_count_frame, image=empl_count_icon_photo, bg='gray74')
    empl_count_img_lbl.place(x=220,y=20)

    empl_count_head_lbl = customtkinter.CTkLabel(master=employee_count_frame,
                                                 text="Employee Count",
                                                 fg_color="gray74",
                                                 text_color="gray25",
                                                 font=("yu gothic ui", 18,"bold"))
    empl_count_head_lbl.place(x=10,y=5)

    global total_employees
    total_employees = len(empl_name_list)

    empl_count_lbl = customtkinter.CTkLabel(master=employee_count_frame,
                                                 text=total_employees,
                                                 fg_color="gray74",
                                                 text_color="black",
                                                 font=("yu gothic ui", 23,"bold"))
    empl_count_lbl.place(x=20,y=40)

    # Creating a employee gender chart
    gender_get_connect = mysql.connector.connect(host=HOSTNAME,user=USER,password=PASSWD,database=DB)
    gender_get_cursor = gender_get_connect.cursor()
    gender_get_cursor.execute("SELECT empl_gender FROM employees;")
    genderData = gender_get_cursor.fetchall()
    MaleCount = FemaleCount = CustomGenCount = 0
    for G_ in genderData:
        if G_[0] == "Male":
            MaleCount += 1
        elif G_[0] == "Female":
            FemaleCount += 1
        else:
            CustomGenCount += 1
    gender_get_connect.close()
    def GenderChart():
        gender_labels = ["Male","Female","Custom"]
        GCount = [2,1,0]
        fig = Figure() # create a figure object
        fig.set_facecolor("#A1A1A1")
        ax = fig.add_subplot(111)
        ax.pie(GCount, radius=1, labels=gender_labels,autopct='%0.2f%%', shadow=False,startangle=90)
        chart1 = FigureCanvasTkAgg(fig,dashboard_main_frame)
        chart1.get_tk_widget().place(x=-140,y=200)
    GenderChart()

    # Creating the Project summary frame
    ProjectSummary_main_frame = customtkinter.CTkFrame(master=dashboard_main_frame, fg_color="gray74",border_color="gray74",
                                                       border_width=1,
                                                       width=650,
                                                       height=280)
    ProjectSummary_main_frame.place(x=410,y=90)
    ProjectSummary_lbl = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="Project Summary",
                                                font=("yu gothic ui", 18,"bold"),
                                                fg_color="gray74",
                                                height=50,
                                                width=200,
                                                text_color="gray25")
    ProjectSummary_lbl.place(x=10,y=10)
    ProjectSummary_head_frame = customtkinter.CTkFrame(master=ProjectSummary_main_frame, fg_color="gray63",border_color="gray74",
                                                       border_width=1,
                                                       width=650,
                                                       height=50)
    ProjectSummary_head_frame.place(x=0,y=50)
    ProjectSummary_code_lbl = customtkinter.CTkLabel(master=ProjectSummary_head_frame,
                                                text="Code",
                                                font=("yu gothic ui", 17,"bold"),
                                                fg_color="gray63",
                                                text_color="gray25")
    ProjectSummary_code_lbl.place(x=10,y=16)
    ProjectSummary_name_lbl = customtkinter.CTkLabel(master=ProjectSummary_head_frame,
                                                text="Project Name",
                                                font=("yu gothic ui", 17,"bold"),
                                                fg_color="gray63",
                                                text_color="gray25")
    ProjectSummary_name_lbl.place(x=140,y=16)
    ProjectSummary_cost_lbl = customtkinter.CTkLabel(master=ProjectSummary_head_frame,
                                                text="Project Cost",
                                                font=("yu gothic ui", 17,"bold"),
                                                fg_color="gray63",
                                                text_color="gray25")
    ProjectSummary_cost_lbl.place(x=350,y=16)
    ProjectSummary_status_lbl = customtkinter.CTkLabel(master=ProjectSummary_head_frame,
                                                text="Status",
                                                font=("yu gothic ui", 17,"bold"),
                                                fg_color="gray63",
                                                text_color="gray25")
    ProjectSummary_status_lbl.place(x=530,y=16)

    # Project 1
    ProjectSummary_code_lbl1 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="#A010",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_code_lbl1.place(x=10,y=110)
    ProjectSummary_name_lbl1 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="Bank Payroll Sys",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_name_lbl1.place(x=140,y=110)
    ProjectSummary_cost_lbl1 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="💲50,200",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_cost_lbl1.place(x=350,y=110)
    ProjectSummary_status_lbl1 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="In Progress",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_status_lbl1.place(x=530,y=110)

    # Project 2
    ProjectSummary_code_lbl2 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="#A011",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_code_lbl2.place(x=10,y=160)
    ProjectSummary_name_lbl2 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="Cyber Dashboard",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_name_lbl2.place(x=140,y=160)
    ProjectSummary_cost_lbl2 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="💲62,650",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_cost_lbl2.place(x=350,y=160)
    ProjectSummary_status_lbl2 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="In Progress",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_status_lbl2.place(x=530,y=160)

    # Project 3
    ProjectSummary_code_lbl3 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="#A015",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_code_lbl3.place(x=10,y=210)
    ProjectSummary_name_lbl3 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="VideoCon System",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_name_lbl3.place(x=140,y=210)
    ProjectSummary_cost_lbl3 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="💲34,220",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_cost_lbl3.place(x=350,y=210)
    ProjectSummary_status_lbl3 = customtkinter.CTkLabel(master=ProjectSummary_main_frame,
                                                text="Completed",
                                                font=("yu gothic ui", 15,"bold"),
                                                fg_color="gray74",
                                                text_color="black")
    ProjectSummary_status_lbl3.place(x=530,y=210)
    







def workers_func():

    workers_main_frame = customtkinter.CTkFrame(master=window, fg_color="gray63")
    workers_main_frame.place(x=200,y=50,relheight=1,relwidth=1)


    def new_empl_add_func():
        empl_add_frame = customtkinter.CTkFrame(master=workers_main_frame, fg_color="gray63")
        empl_add_frame.place(x=0,y=0,relheight=1,relwidth=1)

        add_new_lbl = customtkinter.CTkLabel(master=workers_main_frame,
                                                text="Add New Employee",
                                                font=("yu gothic ui", 24,"bold"),
                                                fg_color="gray63",
                                                height=50,
                                                width=200,
                                                text_color="black")
        add_new_lbl.place(x=30,y=20)

        top_line = Canvas(empl_add_frame, height=1, bg="gray36", highlightthickness=0)
        top_line.place(x=0,y=80,relwidth=1)

        name_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="NAME: ",font=("yu gothic ui", 15),
                                        fg_color="gray63",text_color="black")
        name_lbl.place(x=30,y=90)
        global name_entry
        name_entry = Entry(empl_add_frame,highlightthickness=0, relief=FLAT,
                                            font=("yu gothic ui ", 14),width=300,bg="gray63",fg="black")
        name_entry.place(x=90,y=90)
        name_line = Canvas(empl_add_frame, width=310, height=2.0, bg="gray26", highlightthickness=0)
        name_line.place(x=60, y=115)

        age_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="AGE: ",font=("yu gothic ui", 15),
                                        fg_color="gray63",text_color="black")
        age_lbl.place(x=30,y=135)
        global age_entry
        age_entry = Entry(empl_add_frame,highlightthickness=0, relief=FLAT,
                                            font=("yu gothic ui ", 14),width=300,bg="gray63",fg="black")
        age_entry.place(x=70,y=135)
        age_line = Canvas(empl_add_frame, width=310, height=2.0, bg="gray26", highlightthickness=0)
        age_line.place(x=60, y=160)

        def bloodgrp_callback(choice):
            global SELECTED_BLOOD
            SELECTED_BLOOD = choice

        bloodgrp_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="BLOOD GROUP: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        bloodgrp_lbl.place(x=30,y=175)
        bloodgrp_entry = customtkinter.CTkComboBox(master=workers_main_frame,
                                     values=["A+", "A-","B+","B-","O+","O-","AB+","AB-","CUSTOM"],
                                     variable=customtkinter.StringVar(value="---"),
                                     fg_color="gray63",
                                     text_color="gray22",
                                     width=150,
                                     font=("yu gothic ui", 15),
                                     command=bloodgrp_callback)
        bloodgrp_entry.place(x=150,y=175)

        empladdr_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="ADDRESS: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        empladdr_lbl.place(x=30,y=220)
        global empladdr_entry
        empladdr_entry = customtkinter.CTkTextbox(master=workers_main_frame,fg_color="gray63",corner_radius=7,
                                                text_color="black",width=310,height=200,border_width=1,
                                                border_color="gray22",font=("yu gothic ui", 15))
        empladdr_entry.place(x=120,y=220)

        #taking the gender input
        emplgender_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="GENDER: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        emplgender_lbl.place(x=30,y=450)
        def gender_callback(choice1):
            global SELECTED_GENDER
            SELECTED_GENDER = choice1
        emplgender_entry = customtkinter.CTkComboBox(master=workers_main_frame,
                                     values=["Male","Female","Custom"],
                                     variable=customtkinter.StringVar(value="---"),
                                     fg_color="gray63",
                                     text_color="gray22",
                                     width=150,
                                     font=("yu gothic ui", 15),
                                     command=gender_callback)
        emplgender_entry.place(x=120,y=450)

        #taking the input DOB of the employee
        empldob_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="DOB: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        empldob_lbl.place(x=30,y=495)
        global empldob_entry
        empldob_entry = Entry(empl_add_frame,highlightthickness=0, relief=FLAT,
                                            font=("yu gothic ui ", 14),width=300,bg="gray63",fg="black")
        empldob_entry.place(x=90,y=495)
        empldob_line = Canvas(empl_add_frame, width=310, height=2.0, bg="gray26", highlightthickness=0)
        empldob_line.place(x=80, y=520)

        #getting the join date of the employee
        empljoindate_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="JOIN DATE: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        empljoindate_lbl.place(x=30,y=540)
        global empljoindate_entry
        empljoindate_entry = Entry(empl_add_frame,highlightthickness=0, relief=FLAT,
                                            font=("yu gothic ui ", 14),width=300,bg="gray63",fg="black")
        empljoindate_entry.place(x=130,y=540)
        empljoindate_line = Canvas(empl_add_frame, width=310, height=2.0, bg="gray26", highlightthickness=0)
        empljoindate_line.place(x=120, y=565)

        #getting the EmailID input
        emplemailid_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="EMAIL ID: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        emplemailid_lbl.place(x=30,y=585)
        global emplemail_entry
        emplemail_entry = Entry(empl_add_frame,highlightthickness=0, relief=FLAT,
                                            font=("yu gothic ui ", 14),width=300,bg="gray63",fg="black")
        emplemail_entry.place(x=110,y=585)
        emplemail_line = Canvas(empl_add_frame, width=310, height=2.0, bg="gray26", highlightthickness=0)
        emplemail_line.place(x=100,y=610)

        #getting employee phone number
        emplphone_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="PHONE NUMBER: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        emplphone_lbl.place(x=30,y=630)
        global emplphone_entry
        emplphone_entry = Entry(empl_add_frame,highlightthickness=0, relief=FLAT,
                                            font=("yu gothic ui ", 14),width=300,bg="gray63",fg="black")
        emplphone_entry.place(x=170,y=630)
        emplphone_line = Canvas(empl_add_frame, width=310, height=2.0, bg="gray26", highlightthickness=0)
        emplphone_line.place(x=160,y=655)

        #drawing a vertical page seperator line
        vertical_line = Canvas(empl_add_frame, width=1, bg="gray36", highlightthickness=0)
        vertical_line.place(x=550,y=80,relheight=1)

        #getting the employee department
        empldept_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="DEPARTMENT: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        empldept_lbl.place(x=570,y=90)
        global empldept_entry
        empldept_entry = Entry(empl_add_frame,highlightthickness=0, relief=FLAT,
                                            font=("yu gothic ui ", 14),width=300,bg="gray63",fg="black")
        empldept_entry.place(x=680,y=90)
        empldept_line = Canvas(empl_add_frame, width=310, height=2.0, bg="gray26", highlightthickness=0)
        empldept_line.place(x=670,y=115)

        #getting employee salary 
        emplsalary_lbl = customtkinter.CTkLabel(master=workers_main_frame,text="SALARY: ",font=("yu gothic ui", 16),
                                        fg_color="gray63",text_color="black")
        emplsalary_lbl.place(x=570,y=135)
        global emplsalary_entry
        emplsalary_entry = Entry(empl_add_frame,highlightthickness=0, relief=FLAT,
                                            font=("yu gothic ui ", 14),width=300,bg="gray63",fg="black")
        emplsalary_entry.place(x=630,y=135)
        emplsalary_line = Canvas(empl_add_frame, width=310, height=2.0, bg="gray26", highlightthickness=0)
        emplsalary_line.place(x=620,y=160)

        #getting employee profile picture
        image_input_frame = customtkinter.CTkFrame(master=empl_add_frame,
                                                   width=400,
                                                   height=400,
                                                   fg_color="gray63",
                                                   border_color="gray26",
                                                   border_width=1)
        image_input_frame.place(x=620,y=210)
        def select_pic():
            filename = filedialog.askopenfilename(initialdir="/images", title="Select Profile Pic",
                                filetypes=(("png images","*.png"),("jpg images","*.jpg")))
            global SELECTED_IMAGE
            with open(filename,"rb") as convertToBinary:
                SELECTED_IMAGE = convertToBinary.read()

            if type(filename) == "<class 'str'>":
                pass
            else:
                global img
                img1 = Image.open(filename)
                img = img1.resize((200,200), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                lbl_show_pic['image'] = img
                
        lbl_show_pic = tk.Label(image_input_frame, bg='gray63')
        lbl_show_pic.place(x=80,y=80)
        btn_browse = customtkinter.CTkButton(master=image_input_frame,text='Select Profile Pic',
                                             width=23,
                                             fg_color="black",
                                             text_color="white",
                                             font=("yu gothic ui", 15, "bold"),
                                             command=select_pic)
        btn_browse.place(x=170,y=350)

        #creating the cancel and submit button
        def cancel_func():
            workers_main_frame.destroy()

        def submit_func():
            ENTERED_NAME = name_entry.get()
            ENTERED_AGE = age_entry.get()
            SELECTED_EMPLADDR = empladdr_entry.get("0.0", "end")
            SELECTED_DOB = empldob_entry.get()
            SELECTED_JOINDATE = empljoindate_entry.get()
            SELECTED_EMAILID = emplemail_entry.get()
            SELECTED_PHONE = emplphone_entry.get()
            SELECTED_DEPARTMENT = empldept_entry.get()
            SELECTED_SALARY = emplsalary_entry.get()

            database_add_connection = mysql.connector.connect(host=HOSTNAME,
                                                              user=USER,
                                                              password=PASSWD,
                                                              database=DB)
            add_cursor = database_add_connection.cursor()
            query = """ 
                INSERT INTO employees (employee_id,empl_name,empl_age,empl_bloodgrp,empl_Addr,empl_gender,empl_dob,empl_joindate,empl_mail,empl_phone,empl_department,empl_salary,empl_picture)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            vals = (len(empl_name_list)+1,ENTERED_NAME,ENTERED_AGE,SELECTED_BLOOD,SELECTED_EMPLADDR,SELECTED_GENDER,SELECTED_DOB,SELECTED_JOINDATE,SELECTED_EMAILID,SELECTED_PHONE,SELECTED_DEPARTMENT,SELECTED_SALARY,SELECTED_IMAGE) 
            add_cursor.execute(query,vals)
            database_add_connection.commit()
            database_add_connection.close()

            TreeView.insert("","end",text=len(empl_name_list)+1,values=(ENTERED_NAME,SELECTED_EMAILID,SELECTED_PHONE,
                                                                        SELECTED_DEPARTMENT,SELECTED_JOINDATE))
            empl_add_frame.destroy()



        
        cancel_btn = customtkinter.CTkButton(master=empl_add_frame,
                                             font=("yu gothic ui", 15, "bold"),
                                             fg_color="red",
                                             text="CLOSE",
                                             text_color="white",command=cancel_func)
        cancel_btn.place(x=570,y=680)

        submit_btn = customtkinter.CTkButton(master=empl_add_frame,
                                             font=("yu gothic ui", 15, "bold"),
                                             fg_color="red",
                                             text="SUBMIT",
                                             text_color="white",command=submit_func)
        submit_btn.place(x=900,y=680)


    workers_lbl = customtkinter.CTkLabel(master=workers_main_frame,
                                                text="Employee Portal",
                                                font=("yu gothic ui", 24,"bold"),
                                                fg_color="gray63",
                                                height=50,
                                                width=200,
                                                text_color="black")
    workers_lbl.place(x=30,y=20)

    new_empl_add_btn = customtkinter.CTkButton(master=workers_main_frame, text="Add", command=new_empl_add_func,
                                               width=80,
                                               height=35,
                                               font=("yu gothic ui", 18,"bold"),
                                               corner_radius=7,
                                               fg_color="gray26",
                                               text_color="white",
                                               hover_color="gray20")
    new_empl_add_btn.place(x=950,y=30)

    #creating the table view
    global TreeView
    TreeView = ttk.Treeview(workers_main_frame,
                            columns=('ID','NAME','EMAIL','PHONE','DEPARTMENT','HIRE DATE'))
    TreeView.place(x=20,y=120,relwidth=0.8,relheight=0.75)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    fieldbackground="white",
                    rowheight=50,
                    background="white")
    style.configure("Treeview.Heading", font=("Kerning",11))
    style.map("Treeview",
        background=[("selected", "gray25")],
        foreground=[("selected","white")])


    #creating the headings for the table
    TreeView.heading('#0', text="ID",anchor="w")
    TreeView.column("#0", width=50, anchor='w')
    TreeView.heading('#1', text="NAME",anchor="w")
    TreeView.column("#1", minwidth=180, anchor='w')
    TreeView.heading('#2', text="EMAIL",anchor="w")
    TreeView.column("#2", minwidth=180, anchor='w')
    TreeView.heading('#3', text="PHONE",anchor="w")
    TreeView.column("#3", width=180, anchor='w')
    TreeView.heading('#4', text="DEPARTMENT",anchor="w")
    TreeView.column("#4", width=180, anchor='w')
    TreeView.heading('#5', text="HIRE DATE",anchor="w")
    TreeView.column("#5", width=100, anchor='w')


    extract_data_conn = mysql.connector.connect(host=HOSTNAME,
                                                user=USER,
                                                password=PASSWD,
                                                database=DB)
    extract_cursor = extract_data_conn.cursor()
    extract_cursor.execute("SELECT * FROM employees;")
    extracted_data = extract_cursor.fetchall()
    for dat in extracted_data:
        TreeView.insert("","end",text=dat[0],values=(dat[1],
                                                    dat[8],
                                                    dat[9],
                                                    dat[10],
                                                    dat[7]))
    extract_data_conn.close()

    #creating the double click response function
    def OnDoubleClick(event):
        #getting the selected item
        global item
        item = TreeView.selection()[0]

        #creating a database connection
        #fetch the needed data with the employee_id similarity
        new_conn = mysql.connector.connect(host=HOSTNAME,user=USER,password=PASSWD,database=DB)
        new_conn_cursor = new_conn.cursor()
        new_conn_cursor.execute("SELECT * FROM employees WHERE employee_id='%s'",(TreeView.item(item,"text"),))
        fetch_Data = new_conn_cursor.fetchall()
        for k in fetch_Data:
            EMPLID = k[0]
            NAME = k[1]
            AGE = k[2]
            BLOOD_GRP = k[3]
            ADDRESS = k[4]
            GENDER = k[5]
            DOB = k[6]
            JOINDATE = k[7]
            EMAILID = k[8]
            PHONENUMBER = k[9]
            DEPARTMENT = k[10]
            SALARY = k[11]
            PICTURE = k[12]
        new_conn.close()

        #defining the frame for the display window
        detail_display_window = customtkinter.CTkFrame(master=workers_main_frame,
                                                       fg_color="gray63")
        detail_display_window.place(x=0,y=0,relheight=1,relwidth=1)

        gen_spec = ""
        if GENDER == "Male":
            gen_spec = "Mr."
        elif GENDER == "Female":
            gen_spec = 'Mrs.'
        else:
            gen_spec = "Mr/Mrs."
        lbl = "The details of "+gen_spec+" "+NAME
        empl_det_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                              fg_color="gray63",
                                              font=("yu gothic ui", 21,"bold"),
                                              text_color="black",
                                              text=lbl)
        empl_det_lbl.place(x=30,y=30)

        name = "NAME: "+NAME
        empl_name_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=name)
        empl_name_lbl.place(x=30,y=100)

        department = "DEPARTMENT: "+DEPARTMENT
        empl_dept_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=department)
        empl_dept_lbl.place(x=30,y=140)

        age = "AGE: "+AGE
        empl_age_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=age)
        empl_age_lbl.place(x=30,y=180)

        dob = "DOB: "+DOB
        empl_dob_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=dob)
        empl_dob_lbl.place(x=30,y=220)

        joindate = "HIRE DATE: "+JOINDATE
        empl_joindate_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=joindate)
        empl_joindate_lbl.place(x=30,y=260)

        email = "EMAIL ID: "+EMAILID
        empl_email_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=email)
        empl_email_lbl.place(x=30,y=300)

        phone = "PHONE NUMBER: "+PHONENUMBER
        empl_phone_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=phone)
        empl_phone_lbl.place(x=30,y=340)

        gender = "GENDER: "+GENDER
        empl_gender_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=gender)
        empl_gender_lbl.place(x=30,y=380)

        salary = "SALARY: "+SALARY
        empl_salary_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=salary)
        empl_salary_lbl.place(x=30,y=420)

        bloodgrp = "BLOOD GROUP: "+BLOOD_GRP
        empl_bloodgrp_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=bloodgrp)
        empl_bloodgrp_lbl.place(x=30,y=460)

        addr = "ADDRESS: "+ADDRESS
        empl_addr_lbl = customtkinter.CTkLabel(master=detail_display_window,
                                               fg_color="gray63",
                                               font=("yu gothic ui", 17),
                                               text_color="black",
                                               text=addr)
        empl_addr_lbl.place(x=30,y=500)














        #defining a button for firing the employee
        def fire_func():
            firing_conn = mysql.connector.connect(host=HOSTNAME,password=PASSWD,user=USER,database=DB)
            firing_cursor = firing_conn.cursor()
            firing_cursor.execute("DELETE FROM employees WHERE employee_id='%s'",(TreeView.item(item,"text"),))
            firing_conn.commit()
            firing_conn.close()
            detail_display_window.destroy()
            TreeView.delete(item)
        firing_btn = customtkinter.CTkButton(master=detail_display_window,
                                             font=("yu gothic ui", 18, "bold"),
                                             fg_color="red",
                                             text_color="white",
                                             command=fire_func,
                                             text="FIRE HIM")
        firing_btn.place(x=900,y=30)

        #defining the close button
        def close_func():
            detail_display_window.destroy()
        close_btn = customtkinter.CTkButton(master=detail_display_window,
                                             font=("yu gothic ui", 18, "bold"),
                                             fg_color="red",
                                             text="CLOSE",
                                             text_color="white",
                                             command=close_func)
        
        close_btn.place(x=900,y=680)

    TreeView.bind("<Double-1>",OnDoubleClick)



def email_func():

    email_frame = Frame(window, bg="gray63")
    email_frame.place(x=200,y=50,relwidth=1,relheight=1)

    email_notsetup_warn = customtkinter.CTkFrame(master=email_frame, width=850, height=500,fg_color="#F8F8F8")
    email_notsetup_warn.place(x=50,y=50)

    noacc_lbl = customtkinter.CTkLabel(master=email_notsetup_warn, 
                                                        text="""Oops! You have not merged your email account with O-Travail! Please follow the following steps to \n merge your gmail account.
                                                        \n STEP 1: Turn on two step verification for the particular Gmail ID.
                                                        \n STEP 2: Enter into 'Manage your Google account' > Security > App passwords
                                                        \n STEP 3: Give a custom name under 'Select app' > Generate
                                                        \n STEP 4: Note down the generated app password
                                                        \n STEP 5: click the below button and fill in the Gmail ID and the generated app password
                                                        \n Congrats You have successfully logged in to your Gmail account!!!
                                                        \n\n IF YOU ARE ALREADY LOGGED IN, CLICK BELOW BUTTON TO MOVE TO CONSOLE!""",
                                                        font=("yu gothic ui",16,"bold"),
                                                        text_color="black")
    noacc_lbl.place(x=10,y=10)

    #coding the after log frame
    def gmail_direct_login():
        email_console_frame = Frame(window, bg="gray63")
        email_console_frame.place(x=200,y=50,relheight=1,relwidth=1)
        gmail_lbl = customtkinter.CTkLabel(master=email_console_frame,
                                                text="Gmail",
                                                font=("yu gothic ui", 24,"bold"),
                                                fg_color="gray63",
                                                height=50,
                                                width=200,
                                                text_color="black")
        gmail_lbl.place(x=30,y=30)

        #defining a function to send mails
        def email_compose():
            email_composing_frame = customtkinter.CTkFrame(master=email_console_frame,
                                                   fg_color="gray50",
                                                   height=600,
                                                   width=600)
            email_composing_frame.place(x=200,y=100)
            #gmail ID entry field
            senders_addr_lbl = customtkinter.CTkLabel(master=email_composing_frame,
                                          text="Sender's Address",
                                          text_color="gray21",
                                          fg_color="gray50",
                                          font=("yu gothic ui",18,"bold"))
            senders_addr_lbl.place(x=30,y=40)
            senders_addr_entry = customtkinter.CTkEntry(master=email_composing_frame,
                                            height=35,
                                            width=550,
                                            fg_color="gray50",
                                            text_color="gray21",
                                            border_color="gray25",
                                            corner_radius=8,
                                            font=("yu gothic ui",15,"bold"),
                                            border_width=2)
            senders_addr_entry.place(x=30,y=75)
            #getting the subkect of the mail
            mail_subject_lbl = customtkinter.CTkLabel(master=email_composing_frame,
                                          text="Subject",
                                          text_color="gray21",
                                          fg_color="gray50",
                                          font=("yu gothic ui",18,"bold"))
            mail_subject_lbl.place(x=30,y=130)
            mail_subject_entry = customtkinter.CTkTextbox(master=email_composing_frame,
                                            height=70,
                                            width=550,
                                            fg_color="gray50",
                                            text_color="gray21",
                                            border_color="gray25",
                                            corner_radius=8,
                                            font=("yu gothic ui",15,"bold"),
                                            border_width=2)
            mail_subject_entry.place(x=30,y=165)
            #getting the mail body input
            mail_body_lbl = customtkinter.CTkLabel(master=email_composing_frame,
                                          text="Body",
                                          text_color="gray21",
                                          fg_color="gray50",
                                          font=("yu gothic ui",18,"bold"))
            mail_body_lbl.place(x=30,y=250)
            mail_body_entry = customtkinter.CTkTextbox(master=email_composing_frame,
                                            height=200,
                                            width=550,
                                            fg_color="gray50",
                                            text_color="gray21",
                                            border_color="gray25",
                                            corner_radius=8,
                                            font=("yu gothic ui",15,"bold"),
                                            border_width=2)
            mail_body_entry.place(x=30,y=285)

            def close_fxn():
                email_composing_frame.destroy()

            #creating the close button
            close_btn_img = customtkinter.CTkImage(Image.open(file_path + "/assets/close_icon.png"),size=(23,23))
            close_btn = customtkinter.CTkButton(master=email_composing_frame,command=close_fxn,width=22,hover_color="gray20",image=close_btn_img,fg_color="gray35",compound="left",height=22,text_color="white",font=("yu gothic ui", 19,"bold"),text="")
            close_btn.place(x=550,y=10) 
            
            global msg 
            msg = MIMEMultipart()

            def SEND_MAIL():
                msg["Subject"] = mail_subject_entry.get("0.0","end")
                msg.attach(MIMEText(mail_body_entry.get("0.0","end"), 'plain'))
                HOST = "smtp.gmail.com"
                PORT = 587
                smtp = smtplib.SMTP(HOST,PORT)
                send_detail = {}
                try:
                    send_detail = pickle.load(open("gdat.dat","rb"))
                except:
                    pass
                FROM_EMAIL = send_detail['EMAIL_ID']
                PASSWORD = send_detail['EMAIL_PASSWORD']
                smtp.ehlo()
                smtp.starttls()
                smtp.login(FROM_EMAIL, PASSWORD)
                TO_EMAIL = senders_addr_entry.get()
                smtp.sendmail(FROM_EMAIL,TO_EMAIL,msg.as_string())
                smtp.quit()
            

            #creating a set attachment button 
            def set_attachment_fileopen():
                selected_file = filedialog.askopenfile(mode='r', filetypes=[('Python Files','*.py'), ("all files","*.*")])
                selected_file_path = selected_file.name
                attachment = open(selected_file_path,'rb') # r for read and b for binary
                attachment_package = MIMEBase('application', 'octet-stream')
                attachment_package.set_payload((attachment).read())
                encoders.encode_base64(attachment_package)
                attachment_package.add_header('Content-Disposition', "attachment; filename= " + selected_file_path)
                msg.attach(attachment_package)
                # mail_body_entry.insert("0.0",selected_file_path) --> insert the file name at the last of the textbox (mail_body_entry)


            setattachment_btn_img = customtkinter.CTkImage(Image.open(file_path + "/assets/attachment_icon.png"),size=(22,22))
            set_attachment_btn = customtkinter.CTkButton(master=email_composing_frame,command=set_attachment_fileopen,anchor="sw",hover_color="gray20",image=setattachment_btn_img,fg_color="gray50",compound="left",height=40,text_color="white",font=("yu gothic ui", 19,"bold"),text=" Attachment",corner_radius=8)
            set_attachment_btn.place(x=40,y=530)    


            #creating a send button
            sendmail_btn_img = customtkinter.CTkImage(Image.open(file_path + "/assets/send_icon.png"),size=(22,22))
            sendmail_btn = customtkinter.CTkButton(master=email_composing_frame,command=SEND_MAIL,anchor="sw",hover_color="gray20",image=sendmail_btn_img,fg_color="gray35",compound="left",height=40,text_color="white",font=("yu gothic ui", 19,"bold"),text="  SEND",corner_radius=5)
            sendmail_btn.place(x=450,y=530) 


        #creating the mail composing button
        compose_btn = customtkinter.CTkButton(master=email_console_frame, text="Compose", command=email_compose,
                                               width=110,
                                               height=35,
                                               font=("yu gothic ui", 18,"bold"),
                                               corner_radius=7,
                                               fg_color="gray26",
                                               text_color="white",
                                               hover_color="gray20")
        compose_btn.place(x=880,y=30)

        # Displaying the mail <from addrs> and <subject>
        email_display_mainFrame = customtkinter.CTkScrollableFrame(master=email_console_frame,
                                                                   fg_color="gray55",
                                                                   corner_radius=8)
        email_display_mainFrame.place(x=20,y=100,relwidth=0.80,relheight=0.8)

        # Create a fucntion which retrieves the sender's addrs and subject from gmail and insert insert into a list
        
        MailSubject = []
        SendersAddrs = []
        def getGmailSenderSubject():
            # Importing the needed modules
            import smtplib
            import time
            import imaplib
            import email
            import traceback 
            import base64

            send_detail = {}
            try:
                send_detail = pickle.load(open("gdat.dat","rb"))
            except:
                pass
            EMAIL_ID = send_detail['EMAIL_ID']
            PASSWORD = send_detail['EMAIL_PASSWORD']
            HOST = "imap.gmail.com"
            SMTP_PORT = 993
            try:
                mail = imaplib.IMAP4_SSL(HOST)
                mail.login(EMAIL_ID,PASSWORD)
                mail.select('inbox')

                data = mail.search(None, 'ALL')
                mail_ids = data[1]
                id_list = mail_ids[0].split()   
                first_email_id = int(id_list[0])
                latest_email_id = int(id_list[-1])

                for i in range(latest_email_id,first_email_id, -1):
                    data = mail.fetch(str(i), '(RFC822)' )
                    for response_part in data:
                        arr = response_part[0]
                        if isinstance(arr, tuple):
                            msg = email.message_from_string(str(arr[1],'utf-8'))
                            email_subject = msg['subject'] # Getting the subject of the mail
                            email_from = msg['from'] # getting the from addr of the mail
                            
                            SendersAddrs.append(email_from)
                            MailSubject.append(email_subject)
                    if len(SendersAddrs) == 10:
                        break
                    else:
                        pass
            except Exception as e:
                traceback.print_exc() 
                print("The Error is: ",str(e))
        getGmailSenderSubject()

        for g in range(0,len(SendersAddrs)):
            ind_mail = customtkinter.CTkFrame(master=email_display_mainFrame,
                                       fg_color="gray35", height=80,width=800,border_width=3,border_color="gray55")
            ind_mail.pack(anchor="nw")
            senderText = "From: "+SendersAddrs[g]
            ind_email_SendersAddr = customtkinter.CTkLabel(ind_mail, fg_color="gray35",text=senderText,
                                                           font=("Helvetica", 14),
                                                           text_color="black")
            ind_email_SendersAddr.place(x=10,y=10)
            SubjectText = "Subject: "+MailSubject[g]
            ind_email_Subject = customtkinter.CTkLabel(ind_mail, fg_color="gray35",text=SubjectText,
                                                           font=("Helvetica", 12),
                                                           text_color="black")
            ind_email_Subject.place(x=10,y=45)

    
    def loginorregister_setup():
        email_notsetup_warn.destroy()
        #creating the login screen first
        email_setup_frame = customtkinter.CTkFrame(master=email_frame,
                                                   fg_color="gray50",
                                                   height=500,
                                                   width=600)
        email_setup_frame.place(x=200,y=100)

        gmailicon_img = Image.open("assets\gmail_icon.png")
        gmailicon_img = gmailicon_img.resize((230,120))
        gmailicon_img = ImageTk.PhotoImage(gmailicon_img)
        gmailicon_lbl = customtkinter.CTkLabel(master=email_setup_frame,
                                               image=gmailicon_img,
                                               text="")
        gmailicon_lbl.place(x=180,y=0)

        signin_lbl = customtkinter.CTkLabel(master=email_setup_frame,
                                            text="Sign In",
                                            text_color="gray21",
                                            fg_color="gray50",
                                            font=("yu gothic ui",23,"bold"))
        signin_lbl.place(x=270,y=100)
        
        mail_lbl = customtkinter.CTkLabel(master=email_setup_frame,
                                          text="Email Address",
                                          text_color="gray21",
                                          fg_color="gray50",
                                          font=("yu gothic ui",18,"bold"))
        mail_lbl.place(x=30,y=160)
        mail_entry = customtkinter.CTkEntry(master=email_setup_frame,
                                            height=35,
                                            width=350,
                                            fg_color="gray50",
                                            text_color="gray21",
                                            border_color="gray25",
                                            corner_radius=8,
                                            font=("yu gothic ui",15,"bold"),
                                            border_width=2)
        mail_entry.place(x=30,y=195)

        pass_lbl = customtkinter.CTkLabel(master=email_setup_frame,
                                          text="Password",
                                          text_color="gray21",
                                          fg_color="gray50",
                                          font=("yu gothic ui",18,"bold"))
        pass_lbl.place(x=30,y=250)
        pass_entry = customtkinter.CTkEntry(master=email_setup_frame,
                                            height=35,
                                            width=350,
                                            fg_color="gray50",
                                            text_color="gray21",
                                            border_color="gray25",
                                            corner_radius=8,
                                            font=("yu gothic ui",15,"bold"),
                                            border_width=2,show="*")
        pass_entry.place(x=30,y=285)

        def login_func():
            global EMAIL_PASSWORD,EMAIL_ID
            EMAIL_PASSWORD = pass_entry.get()
            EMAIL_ID = mail_entry.get()
            l = [EMAIL_ID,EMAIL_PASSWORD]
            gmail_dat_file = open("gdat.dat","wb")
            gmail_log_det = {}
            gmail_log_det["EMAIL_ID"] = EMAIL_ID
            gmail_log_det["EMAIL_PASSWORD"] = EMAIL_PASSWORD
            pickle.dump(gmail_log_det,gmail_dat_file)
            gmail_dat_file.close()
            gmail_direct_login()
        
        login_btn = customtkinter.CTkButton(master=email_setup_frame,
                                            height=30,
                                            text="LOGIN",
                                            fg_color="gray15",
                                            text_color="white",
                                            font=("yu gothic ui",20,"bold"),
                                            hover_color="gray20",
                                            width=540,
                                            command=login_func)
        login_btn.place(x=30,y=350)


    #function to check weather the gmail data file is empty or not and act according to it
    def check_gmail_data():
        gmail_data_file = "gdat.dat"
        if os.stat(gmail_data_file).st_size == 0:
            loginorregister_setup()
        else:
            gmail_direct_login()




    noacc_btn = customtkinter.CTkButton(master=email_notsetup_warn, text="LOGIN", command=check_gmail_data,
                                                        width=120,
                                                        height=32,
                                                        border_width=0,
                                                        corner_radius=10,
                                                        fg_color="turquoise",
                                                        hover_color="cyan",
                                                        font=("yu gothic ui",14,"bold"),
                                                        text_color="black")
    noacc_btn.place(x=350,y=400)
    




data_extract()
app()


window.mainloop()