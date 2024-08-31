import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime

class ExpenseTracker:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1000x800")
        
        #Define categories
        self.categories = ['Groceries', 'Rent', 'Entertainment', 'Utilities', 'Other']
        self.file_name = os.path.join(os.path.dirname(__file__),"expenses_tracker.csv")
        
        #List to hold expenses
        self.expenses = []
        self.load_expenses()
        
        self.root.configure(bg = "#ADD8E6")
        self.setup_ui()
        
        
    def setup_ui(self):
        self.form_frame = tk.Frame(self.root, bg="#ADD8E6")
        self.form_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.date_label = tk.Label(self.form_frame, text="Date (YYYY-MM-DD):", bg="#ADD8E6")
        self.date_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")

        self.date_entry = tk.Entry(self.form_frame)
        self.date_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")

        self.amount_label = tk.Label(self.form_frame, text="Amount:", bg="#ADD8E6")
        self.amount_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="w")

        self.amount_entry = tk.Entry(self.form_frame)
        self.amount_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="w")

        self.categories_label = tk.Label(self.form_frame, text="Category:", bg="#ADD8E6")
        self.categories_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="w")

        self.category_combobox = ttk.Combobox(self.form_frame, values=self.categories)
        self.category_combobox.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="w")

        self.description_label = tk.Label(self.form_frame, text="Description:", bg="#ADD8E6")
        self.description_label.grid(row=3, column=0, padx=(10, 0), pady=10, sticky="w")

        self.description_entry = tk.Entry(self.form_frame)
        self.description_entry.grid(row=3, column=1, padx=(0, 10), pady=10, sticky="w")
        
        self.add_button = tk.Button(self.form_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.frame_container = tk.Frame(self.root, bg="#ADD8E6")
        self.frame_container.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.frame_left = tk.Frame(self.frame_container, bg="#ADD8E6")
        self.frame_left.grid(row=0, column=0, padx=10, sticky="nsew")

        self.label_left = tk.Label(self.frame_left, text="Choose the category you want to see the summary of:", bg="#ADD8E6")
        self.label_left.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.var = tk.StringVar(value="Category")
        self.rb1 = tk.Radiobutton(self.frame_left, text="Groceries", variable=self.var, value="Groceries", bg="#ADD8E6")
        self.rb1.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.rb2 = tk.Radiobutton(self.frame_left, text="Rent", variable=self.var, value="Rent", bg="#ADD8E6")
        self.rb2.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.rb3 = tk.Radiobutton(self.frame_left, text="Entertainment", variable=self.var, value="Entertainment", bg="#ADD8E6")
        self.rb3.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.rb4 = tk.Radiobutton(self.frame_left, text="Utilities", variable=self.var, value="Utilities", bg="#ADD8E6")
        self.rb4.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.rb5 = tk.Radiobutton(self.frame_left, text="Others", variable=self.var, value="Others", bg="#ADD8E6")
        self.rb5.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        self.category_choice_button = tk.Button(self.frame_left, text="Generate graph", command=self.plot_graph)
        self.category_choice_button.grid(row=6, column=0, padx=10, pady=10)

        self.frame_right = tk.Frame(self.frame_container, bg="#ADD8E6")
        self.frame_right.grid(row=0, column=1, padx=10, sticky="nsew")

        self.canvas = tk.Canvas(self.frame_right, width=500, height=300)
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        self.save_frame = tk.Frame(self.root, bg="#ADD8E6")
        self.save_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.save_label = tk.Label(self.save_frame, text="Do not forget to save before closing the app:", bg="#ADD8E6")
        self.save_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")
        
        self.save_button = tk.Button(self.save_frame, text="Save Expense Changes", command=self.save_expenses)
        self.save_button.grid(row=0, column=1, columnspan=2, pady=20)

        
        
    
    
    def load_expenses(self):
        """Loads expenses from csv file"""
        self.expenses = []
        try:
            with open(self.file_name, mode = 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row["Amount"] = float(row["Amount"])
                    row["Date"] = datetime.strptime(row["Date"], "%Y-%m-%d")
                    self.expenses.append(row)
                
        except FileNotFoundError:
             pass
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading expenses: {str(e)} ")
        
          

    def save_expenses(self):
        """Save expenses to csv file"""
        try:
            with open(self.file_name, mode = "w", newline='') as file:
                fieldnames = ["Date", "Amount", "Category", "Description"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for expense in self.expenses:
                    writer.writerow({
                        "Date" : datetime.strftime(expense["Date"], "%Y-%m-%d"),
                        "Amount" : expense["Amount"],
                        "Category" : expense["Category"],
                        "Description": expense["Description"]
                    })
                self.expenses.clear()
                messagebox.showinfo("Success", "Expanse changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving expenses: {str(e)}") 
         
                  
    def add_expense(self):
        """Add new expense to expenses list"""
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_combobox.get()
        description = self.description_entry.get()
        
        if date != "" and amount != "" and category != "" and description != "":     
            try:
                expense = {
                "Date" : datetime.strptime(date, "%Y-%m-%d"),
                "Amount" : float(amount),
                "Category" :category,
                "Description": description
                 }
            
                self.expenses.append(expense)
                
                #Clear fiedls
                self.date_entry.delete(0,tk.END)
                self.amount_entry.delete(0,tk.END)
                self.category_combobox.set('')
                self.description_entry.delete(0,tk.END)
                
                messagebox.showinfo("Success", "Expanse added successfully!")
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date or amount format!")
            
        else:
            messagebox.showwarning("Warning", "You must fill all the fields before moving forward!")
            
            
    def plot_graph(self):
        """Plots the graph of the wanted category and provides it to the user"""
        category = self.var.get()
        
        amount_list = [expense["Amount"] for expense in self.expenses if expense["Category"] == category]
        date_list = [expense["Date"] for expense in self.expenses if expense["Category"] == category]
        
        if len(amount_list) >= 2:
        
            plt.style.use('seaborn-v0_8')
            fig, ax = plt.subplots(figsize = (6,4))  
            
            ax.plot(date_list, amount_list,linewidth = 3)
            
            ax.set_title(f"Summary for {category}", fontsize = 24)

            ax.set_xlabel("Date", fontsize = 14)
            ax.set_ylabel("Amount", fontsize = 14)
            
            ax.tick_params(labelsize = 14)
            
            min_date, max_date = min(date_list), max(date_list)
            min_amount, max_amount = min(amount_list), max(amount_list)
            
            ax.set_xlim(min_date, max_date)
            ax.set_ylim(min_amount * 0.9, max_amount * 1.1) 
            
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate() 
            
            for widget in self.frame_right.winfo_children():
                widget.destroy()
                
            self.canvas =  FigureCanvasTkAgg(fig, master=self.frame_right)
            self.canvas.draw()
            
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            def resize(event):
                self.canvas.get_tk_widget().configure(width=event.width, height=event.height)
                fig.set_size_inches(event.width / 100, event.height / 100)
                self.canvas.draw()

                self.frame_right.bind("<Configure>", resize)
        else: 
            messagebox.showwarning("Warning",f"There are either no expenses or not enough expenses in the {category} category")
        
        
        
        
        
        
        
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()