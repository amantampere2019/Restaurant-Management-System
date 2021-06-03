# TIE-02106 Introduction to Programming
# Md Aman Khan, md.khan@student.tut.fi, student no :272541
# Md Shohidur Rahman, md.s.rahman@student.tut.fi, student no: 245141
# Task: Program for restaurant management(Space and Billing)

"""
This project has been implemented  keeping the space management of any
restaurant in mind. In the beginning of the program it asks user to enter the
size of the floor and size of the table that will be placed throughout the
space.

We assumed the floor is square shaped and so the tables.We consumed additional
2 square feet space to keep gap between tables.So total number of tables for
the space have been calculated using following formula:

Number of maximum table = Size of the floor space/( Size of the table + TABLE_INTER_SPACE )

After initial input it will display maximum possible table when the user click
confirm button. The new interface with table layout will be loaded on screen
when user click the continue button.

User can book any table from the layout by clicking the reserve button. When
the user click reserve button it will turn in red to denote that table has been
reserved. For every table there is also a Bill button. This Bill button will
help to generate bill for that table with table number and a randomly generated
reference number.

In “Bill  interface”, user can select the item from the check button and place
the price in the text field.

TOTAL button will generate the total bill based on value placed by the user.
If anything goes wrong, user can reset all values by clicking RESET button and
corresponding error will be shown on the same interface.

How this program is Scalable:
To prove this program as a scalable solution we implemented following features:

Table Layout:
The table layout will be created dynamically based on user input. It can
generate layout for 0 to any number(since we used a picture, it might take long
time, so its better to use reasonable large number to test the scalability.)
For a test run you can use floor size as 100 and table size 4. Our program also
capable of handing  situation like 0 table to infinitely large number ( e.g
maximum  size of the integer)

Check Button and Price Entry Fields:
We implanted check buttons and Price Entry fields  in a such a way that,
whenever a new food item is added to the  global constant named MANU_LIST,
corresponding check button and price entry fields will be generated accordingly
for the newly added food item.


"""
from tkinter import *
import tkinter
import random
import math

# MENU_LIST contains the existing food items, more food items can be added here
MENU_LIST = ["Fries","Burger","Filet" , "Drinks", "Chicken_Burger", "Cheese_Burger"]
# 24% is considered
Tax = 24
# Space between two tables
TABLE_INTER_SPACE = 2


class Management:
    """
    This class has implemented the table layout, Reservation and take to Billing
    option
    """
    def __init__(self, tables_per_side):
        """
        this constructor creates GUI and create instance variables
        :param tables_per_side: number of tables per row / column
        """
        self.__window = Tk()
        self.__window.title("Space Management System")

        # picture for the available table
        self.__tablepics = PhotoImage(file="1.png")
        # picture for the booked / reserved table
        self.__tablepics_reserved = PhotoImage(file="2.png")
        self.__tables_per_side = tables_per_side

        # Creating empty list where pictures for table will be stored
        self.__tablepiclabels = []
        # Creating empty list for Labeling tables, such as table1, table2 etc.
        self.tablenamelabel = []
        #A boolean list for tracking table status(i.e booked or available)
        self.__book = []
        # list for Bill buttons used for every table
        self.__button2 = []

        # Creating scalable GUI based on previously calculated number of tables,
        # each of them containing a 'Bill' button, a 'Available / Resurve' button
        # and table label with their own number
        for i in range(tables_per_side):
            for j in range(0, tables_per_side * tables_per_side, tables_per_side):

                # Adding table picture
                new_label = Label(self.__window)
                new_label.grid(row=j+1, column=i + 1, sticky=S)
                self.__tablepiclabels.append(new_label)

                # Adding  name label for table
                table_name = Label(self.__window)
                table_name.grid(row=j+1, column=i + 1, sticky=S)
                self.tablenamelabel.append(table_name)

                # Adding 'Available' button
                new_button = Button(self.__window)
                new_button.grid(row=j+2, column=i + 1, sticky=E+N)
                self.__book.append(new_button)

                # Adding 'Bill' button
                new_button_2 = Button(self.__window)
                new_button_2.grid(row=j+2, column=i + 1, sticky=W+N)
                self.__button2.append(new_button_2)

        # Adding 'Exit' button for exiting from the program
        Button(self.__window, text="Exit", command=self.__window.destroy, font=('arial', 10, 'bold'), bg = 'pink')\
            .grid(row=tables_per_side * tables_per_side + 4, column=int(tables_per_side * tables_per_side), sticky=W+E+N+S)

        self.initialize_table()

    def initialize_table(self):
        """
        This list contains information on whether the table is free or in use.
        :return: None
        """
        self.__table_is_free = [True] *(self.__tables_per_side * self.__tables_per_side)

        # Setting a picture of to every table
        for label in self.__tablepiclabels:
            label.configure(image=self.__tablepics)
        # Setting default values
        self.reset_buttons_labels()

    def reset_buttons_labels(self):
        """
        Setting all buttons and labels to their initial state.
        :return: None
        """
        for ind_num in range(len(self.__book)):
            self.__book[ind_num].configure(text="Available")
            self.__book[ind_num].configure(background="green")
            self.__book[ind_num].configure(state=NORMAL)
            # used to retrieve index of the table for clicked 'Available' button
            self.__book[ind_num].configure(command=lambda s=ind_num: self.change_in_table_status(s))

        for ind_num in range(len(self.tablenamelabel)):
            self.tablenamelabel[ind_num].configure(text="Table No: "+ str(ind_num+1))

        for ind_num in range(len(self.__button2)):
            self.__button2[ind_num].configure(text="Bill")
            self.__button2[ind_num].configure(background="Yellow")
            self.__button2[ind_num].configure(state=NORMAL)
            # used to retrieve index of the table for clicked 'Bill' button
            self.__button2[ind_num].configure(command = lambda s=ind_num: self.table_bill_fun(s))

    def table_bill_fun(self, table_num_of_bill):
        """
        initiate the bill window for particular table
        :param table_num_of_bill: number of table per row / column
        :return: None
        """
        table_bill = Bill(table_num_of_bill)
        table_bill.start()

    def change_in_table_status(self, index):
        """
        Change table status(Available / Resurve)
        :param index: index of the particular table
        :return: None
        """
        if self.__table_is_free[index]:
            self.__book[index].configure(text="Resurve")
            self.__book[index].configure(background="red")
            self.__book[index].configure(state=NORMAL)
            self.__table_is_free[index] = False
            self.__tablepiclabels[index].configure(image=self.__tablepics_reserved)
        else:
            self.__book[index].configure(text="Available")
            self.__book[index].configure(background="green")
            self.__book[index].configure(state=NORMAL)
            self.__table_is_free[index] = True
            self.__tablepiclabels[index].configure(image=self.__tablepics)

    def start(self):
        self.__window.mainloop()


class Bill:
    """
    This class has implemented functionalities of billing
    """
    def __init__(self, table__number_of_bill):
        """
        constructor of the class
        :param table__number_of_bill: Index of a particular table for which 'Bill'
        button has been clicked
        """
        self.__window = Toplevel()
        self.__window.title("Restaurent Management System")

        self.__table__number_of_bill=table__number_of_bill

        Tops = Frame(self.__window)
        Tops.pack(side=TOP)
        # Displaying label with table number for which bill is being prepared
        label_info = Label(Tops, font=('arial', 25, 'italic'),text="Bill for Table No:"+str(self.__table__number_of_bill+1), fg='Blue', bd=10, anchor='w')
        label_info.grid(row=0, column=0)

        self.initialize_manu()

    def initialize_manu(self):
        """
        Setting initial values for variables and GUI
        :return: None
        """
        self.__menu_list = MENU_LIST
        self.__menu_price = [0]*len(self.__menu_list)
        self.__checkbutton_var = [0]*len(self.__menu_list)
        self.__total_price = 0

        frame1 = Frame(self.__window, width=600, height=600, relief=SUNKEN)
        frame1.pack(side=LEFT)

        label_Reference = Label(frame1, font=('arial', 16, 'bold'), text="Reference", bd=16, anchor='w')
        label_Reference.grid(row=0, column=0)

        self.__rand_number = StringVar()
        txt_Reference = Entry(frame1, font=('arial', 12, 'bold'), textvariable=self.__rand_number, bd=10, insertwidth=4, bg='pink', justify='right')
        txt_Reference.grid(row=0, column=1)

        # Creating check buttons and entry fields based on MANU_LIST
        for i in range(len(self.__menu_list)):
            self.__checkbutton_var[i] = IntVar()
            self.__checkbutton = Checkbutton(frame1, font=('arial', 12, 'bold'), text=self.__menu_list[i],variable = self.__checkbutton_var[i] ,bd=16, anchor='w')
            self.__checkbutton.grid(row=i+2, column=0)
            self.__menu_price[i] = StringVar()
            txt_Reference = Entry(frame1, font=('arial', 12, 'bold'), textvariable=self.__menu_price[i], bd=10, insertwidth=4,bg='pink', justify='right')
            txt_Reference.grid(row=i+2, column=1)

        # for Tax Label and value
        label_Tax = Label(frame1, font=('arial', 12, 'bold'), text="Tax", bd=16, anchor='w')
        label_Tax.grid(row=len(self.__menu_list)+2, column=0)
        label_Tax_Value = Label(frame1, font=('arial', 12, 'bold'), text=str(Tax)+"%", bd=16, anchor='w')
        label_Tax_Value.grid(row=len(self.__menu_list)+2, column=1)

        # Creating Error info Label
        self.label_error_info = Label(frame1, font=('arial', 16, 'bold'), text="", bd=16, anchor='w')
        self.label_error_info.grid(row=len(self.__menu_list)+1, column=3)

        # Creating Total Label and Button
        label_Total = Label(frame1, font=('arial', 16, 'bold'), text="Total", bd=16, anchor='w')
        label_Total.grid(row=len(self.__menu_list)+3, column=3)
        self.__total_price_var = StringVar()
        txt_Total = Entry(frame1, font=('arial', 16, 'bold'),textvariable=self.__total_price_var , bd=10, insertwidth=4, bg='pink',
                          justify='right')
        txt_Total.grid(row=len(self.__menu_list)+3, column=4)
        btnTotal = Button(frame1, padx=16, pady=8, bd=16, fg='black',
                          font=('arial', 16, 'bold'),
                          width=10, text="Total", bg='powder blue', command=self.total).grid(row=len(self.__menu_list)+4, column=1)

        # Creating Reset Button
        btnReset = Button(frame1, padx=16, pady=8, bd=16, fg='black',
                          font=('arial', 16, 'bold'),
                          width=10, text="Reset", bg='powder blue',
                          command=self.reset_buttons_labels).grid(row=len(self.__menu_list)+4, column=2)

        # Creating Paid Button
        btnPaid = Button(frame1, padx=16, pady=8, bd=16, fg='black',
                          font=('arial', 16, 'bold'),
                          width=10, text="Paid", bg='powder blue',
                          command=self.__window.destroy).grid(row=len(self.__menu_list)+4, column=3)

        self.reset_buttons_labels()

    def reset_buttons_labels(self):
        """
        Setting all value to their initial state.
        :return: None
        """
        # Creating a random number for reference
        self.__rand_number.set(random.randint(10000, 999999))
        self.__total_price = 0
        self.__total_price_var.set(0)
        self.label_error_info["text"] = ""

        for item_price in self.__menu_price:
            item_price.set(0)

        for chk_button in self.__checkbutton_var:
            chk_button.set(0)

    def total(self):
        """
        Calculate bill for a table based food selected from check button
        :return: None
        """
        self.__total_price = 0
        for i in range(len(self.__menu_price)):
            try:
                if float(self.__menu_price[i].get())>= 0:
                    self.__total_price = self.__total_price + float(self.__menu_price[i].get()) * float(self.__checkbutton_var[i].get())
                else:
                    self.label_error_info["text"] = "Error: Price must be a positive number"
            except:
                self.label_error_info["text"] = "Error: Price must be a positive number"
        self.__total_price_var.set(format (self.__total_price+self.__total_price*Tax*.01,'.2f'))

    def start(self):
        self.__window.mainloop()


class Userinterface:
    """
    This class implement the user interface for taking user input such as floor
    size(in square feet) and table size(square feet). Also calculate number of
    maximum tables can be fitted in given floor space.
    """

    def __init__(self):
        """
        this constructor creates GUI
        """
        self.__tables_per_side = 0
        self.__mainwindow = tkinter.Tk()
        self.__mainwindow.geometry("600x200+0+0")

        # Change the title of the main window
        self.__mainwindow.title("Restaurant Managemet System")

        # Adding GUI components
        self.__floor_label = tkinter.Label(self.__mainwindow,
                                           text="Enter area of the floor in Square feet", font=('arial', 12))
        self.__table_label = tkinter.Label(self.__mainwindow,
                                           text="Enter space required for every table in Square feet", font=('arial', 12))

        # Create an Entry-component for the floor size and table size.
        self.__floor_value = tkinter.Entry(self.__mainwindow, width=20, font=('arial', 12, 'bold'))
        self.__floor_value.focus()
        self.__mainwindow.bind('<Return>', lambda a=0: self.calculate_table())
        self.__table_value = tkinter.Entry(self.__mainwindow, width=20, font=('arial', 12, 'bold'))
        self.__calculate_button = tkinter.Button(self.__mainwindow,text="Confirm", background="pink", command=self.calculate_table, font=('arial', 12))
        self.__explanation_text = tkinter.Label(self.__mainwindow , font=('arial', 12, 'bold'))
        self.__continue_button = tkinter.Button(self.__mainwindow, text="Continue", command=self.stop, font=('arial', 12))

        # Placing the components in the GUI
        self.__floor_label.grid(row=3, column=1, sticky=W+E+N)
        self.__floor_value.grid(row=3, column=2, sticky=E)
        self.__table_label.grid(row=5, column=1, sticky=W+E+N)
        self.__table_value.grid(row=5, column=2, sticky=E)
        self.__calculate_button.grid(row=7, column=2, sticky=W+E+N)
        self.__continue_button.grid(row=9, column=2, sticky=W + E + N)
        self.__explanation_text.grid(row=7, column=1, sticky=W+E+N+S)

    def calculate_table(self):
        """
        This function calculate maximum number of table for the floor
        :return: None
        """
        if not (
                self.__floor_value.get().isalpha() or self.__table_value.get().isalpha()):
            try:
                if float(self.__floor_value.get()) <= 0 or float(
                        self.__table_value.get()) <= 0:
                    self.__explanation_text["text"] = "Error: Floor space and Table size must be positive."
                    self.reset_fields()
                else:
                    floor = float(self.__floor_value.get())
                    table = float(self.__table_value.get())

                    # Calculating maximum possible tables in the floor space
                    number_of_total_table = int(floor / (table + TABLE_INTER_SPACE))
                    # Calculate number of rows or column of the layout for the given space
                    self.__tables_per_side = int(math.sqrt(number_of_total_table))
                    maximum_possible_table = self.__tables_per_side * self.__tables_per_side

                    text = "2 feet free space has been added with every tables \n so, maximum possible Table: " + str(maximum_possible_table)
                    self.__explanation_text["text"] = text
            except ValueError:
                self.__explanation_text["text"] = "Error: Floor space and Table size must be a positive numbers."
                # if error occurs all fields in the GUI will be reset
                self.reset_fields()
        else:
            self.__explanation_text["text"] = "Error: Floor space and Table size must be a psotive numbers."
            # if error occurs all fields in the GUI will be reset
            self.reset_fields()

    def get_tables_per_side(self):
        """
        :return: number of tables per row / column
        """
        return self.__tables_per_side

    def reset_fields(self):
        """
        Reset fields
        :return: None
        """
        self.__floor_value["textvariable"] = ''
        self.__table_value["textvariable"] = ''

    def stop(self):
        """
        Ends the execution of the program.
        """
        self.__mainwindow.destroy()

    def start(self):
        """
        Starts the mainloop.
        """
        self.__mainwindow.mainloop()


def main():
    """
    :return: None
    """
    # Creating object of class User Userinterface
    ui = Userinterface()
    ui.start()

    # Taking the number of tables per row or column
    tables_per_side =int(ui.get_tables_per_side())

    # Creating object of class Management
    ui2 = Management(tables_per_side)
    ui2.start()


main()
