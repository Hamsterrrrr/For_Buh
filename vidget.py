# from autobuh import Pars_fsgs
import tkinter as tk
from tkinter import messagebox
from autobuh import *
import csv
import threading

class App:
    def __init__(self, master):
        self.master = master
        self.pars = Pars_fsgs()
        self.master.title("CRUD and Pars_fsgs program")
        self.master.config(bg="black")
        
        # Create label and entry for INN
        self.inn_label = tk.Label(self.master, text="INN:")
        self.inn_label.grid(row=0, column=0)
        
        self.inn_entry = tk.Entry(self.master)
        self.inn_entry.grid(row=1, column=0)
        self.inn_entry.config(bg="grey")
        
        self.add_button = tk.Button(self.master, text="Add data to database", command=self.add_db)
        self.add_button.grid(row=2, column=0)
        self.add_button.config(bg="grey")

        self.delete_button = tk.Button(self.master, text="Delete data from database by inn", command=self.delete_db)
        self.delete_button.grid(row=3, column=0)
        self.delete_button.config(bg="grey")


        # Create buttons for Pars_fsgs options
        self.scrape_button = tk.Button(self.master, text="Scrape data from website", command=self.scrape_data)
        self.scrape_button.grid(row=8, column=1)
        self.scrape_button.config(bg="grey")

        self.data_inn_button = tk.Button(self.master, text="all inn in db", command=self.send_inn)
        self.data_inn_button.grid(row=7, column=1)
        self.data_inn_button.config(bg="grey")

        self.csv_label = tk.Label(self.master, text="Insert name file's")
        self.csv_label.grid(row=0, column=1)

        self.csv_entry = tk.Entry(self.master)
        self.csv_entry.grid(row=1, column=1)
        self.csv_entry.config(bg="grey")

        self.csv_button = tk.Button(self.master, text="start", command = self.import_from_csv)
        self.csv_button.grid(row=2, column=1)
        self.csv_button.config(bg="grey")

        # Create label and entry for ID
        self.id_label = tk.Label(self.master, text="ID")
        self.id_label.grid(row=0, column=2)

        self.id_entry = tk.Entry(self.master)
        self.id_entry.grid(row=1, column=2)
        self.id_entry.config(bg="grey")

        

        self.delete_by_id_button = tk.Button(self.master, text="Delete data from database by ID", command=self.delete_by_id)
        self.delete_by_id_button.grid(row=2, column=2)
        self.delete_by_id_button.config(bg="grey")

        self.delete_all_button = tk.Button(self.master, text="Delete all", command=self.delete_all)
        self.delete_all_button.grid(row=3, column=2)
        self.delete_all_button.config(bg="grey")

        


        
    def scrape_data(self):
        thread = threading.Thread(target=self.pars.insert_db)
        thread.start()
        
    def add_db(self):
        try:
            inn_value = (self.inn_entry.get())
            inn_alike = session.query(Inns).filter_by(inn=str(inn_value)).first()
            if 9 <= len(inn_value) <= 12 and not inn_alike:                
                print(f"Adding INN: {inn_value}")
                session.add(Inns(inn=inn_value))
                session.commit()
                session.close()
            else:
                print("incorrect inn")
                messagebox.showerror("Error", "Incorrect INN")
        except Exception as _ex:
            print(_ex)
            
            # Use inn_value in your add_db method
            
        print(inn_value)
    
    def add_db(self):
        try:
            inn_value = (self.inn_entry.get())
            inn_alike = session.query(Inns).filter_by(inn=str(inn_value)).first()
            if 9 <= len(inn_value) <= 12 and not inn_alike:                
                print(f"Adding INN: {inn_value}")
                session.add(Inns(inn=inn_value))
                session.commit()
                session.close()
            else:
                print("incorrect inn")
                messagebox.showerror("Error", "Incorrect INN")
        except Exception as _ex:
            print(_ex)
            messagebox.showerror("Error", str(_ex))
            
    def delete_db(self):
        try:
            inn_value = (self.inn_entry.get())
            print(f"Deleting INN: {inn_value}")
            session.query(Codes_data).filter(Codes_data == inn_value).delete()
            session.query(Formes_data).filter(Formes_data == inn_value).delete()
            session.query(Inns).filter(Inns.inn == inn_value).delete()
            session.commit()
            session.close()
        except Exception as _ex:
            print(_ex)
            messagebox.showerror("Error", str(_ex))
        
    
    def delete_by_id(self):
        try:
            id_value = self.id_entry.get()
            if id_value:
                id_value = int(id_value)
                print(f"Deleting row with ID: {id_value}")
                session.query(Codes_data).filter(Codes_data == id_value).delete()
                session.query(Formes_data).filter(Formes_data == id_value).delete()
                session.query(Inns).filter(Inns.ID == id_value).delete()
                session.commit()
                session.close()
            else:
                print("Please enter an ID value")
                messagebox.showerror("Error", "Please enter an ID value")
        except Exception as _ex:
            print(_ex)
            messagebox.showerror("Error", str(_ex))
       

    def delete_all(self):
        try:
            print(f"Deleting all")
            session.query(Codes_data).delete()
            session.query(Formes_data).delete()
            session.query(Inns).delete()
            session.commit()
            session.close()
        except Exception as _ex:
            print(_ex)
            messagebox.showerror("Error", str(_ex))
       

    def send_inn(self):
        all_inn = session.query(Inns.ID, Inns.inn).all()
        display_window = tk.Toplevel(self.master)
        display_window.title("All INN values")
        for row in all_inn:
            id_value = row[0]
            inn_value = row[1]
            label_text = f"ID: {id_value}, INN: {inn_value}"
            label = tk.Label(display_window, text=label_text, anchor="w")
            label.pack(fill="x")


    def import_from_csv(self):
        try:
            file_name = self.csv_entry.get()
            if file_name:
                with open(f"{file_name}.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        row_int = list(map(int, row))
                        for value in row_int:
                            inn = Inns(inn=value)
                            if session.query(Inns).filter_by(inn=str(value)).first():
                                continue
                            else:
                                session.add(inn)
                session.commit()
                session.close()
                messagebox.showinfo("Success", "Data imported from CSV file")
            else:
                print("Please enter a file name")
                messagebox.showerror("Error", "Please enter a file name")
        except Exception as _ex:
            print(_ex)
            messagebox.showerror("Error", str(_ex))


root = tk.Tk()
app = App(root)
root.mainloop()