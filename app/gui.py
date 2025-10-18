import tkinter as tk 
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfile
from .converter import convert, get_currencies
from .db_history import Database
from .utils import resource_path
from dotenv import load_dotenv
from .csv_export import export_to_csv
import os


class CurrencyConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x450+300+150")
        self.title("Currency Converter")
        self.resizable(width=False, height=False)

        self.db = Database()

        load_dotenv()
        if not os.getenv("API_KEY"):
            messagebox.ERROR("API Key Error.", "API_KEY environment variable is not set.")
            self.destroy()
            return

        self.build_gui()

    def build_gui(self):
        logo_path = resource_path("images/logo.png")
        self.logo = tk.PhotoImage(file=logo_path)
        tk.Label(self, image=self.logo).pack()

        frame = tk.Frame(self)
        frame.pack()

        ttk.Label(frame, text="From:").grid(row=0, column=0,padx=5,pady=5, sticky=tk.W)
        ttk.Label(frame, text="To:").grid(row=0,column=1,padx=5, pady=5, sticky=tk.W)

        self.from_combo = ttk.Combobox(frame, state="readonly")
        self.from_combo.grid(row=1, column=0, padx=5, pady=5)
        self.to_combo = ttk.Combobox(frame,state="readonly")
        self.to_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)       
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.insert(0, "1.00")
        self.amount_entry.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E
        )

        self.result_label = ttk.Label(font=("Arial", 20, "bold"), text="")
        self.result_label.pack(pady=10)

        convert_button = ttk.Button(self,text="Convert",width=20,command=self.convert_curr)
        convert_button.pack(pady=5)
        history_button = ttk.Button(self,text="History",width=20,command=self.show_history)
        history_button.pack(pady=5)

        try:
            currencies = get_currencies() 
            self.from_combo["values"] = currencies
            self.to_combo["values"] = currencies
            if currencies:
                self.from_combo.current(0)
                self.to_combo.current(0)
        except Exception as e:
            messagebox.showerror("Currency Load Error", str(e))

    def convert_curr(self):
        try:
            src = self.from_combo.get()
            dest = self.to_combo.get()
            amount = float(self.amount_entry.get())

            if not src or not dest:
                messagebox.showerror("Error, please select both currencies.")
                return
            
            result = convert(amount, src,dest)
            self.result_label.config(text=f"{amount:.2f} {src} = {result:.2f} {dest}")

            self.db.save_conversion(amount,src, dest, result)
        except ValueError:
            messagebox.showerror("Invalid input, please enter a valid numeric number.")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def show_history(self):
        win = tk.Toplevel(self)
        win.title("Conversion History")

        tree = ttk.Treeview(win, columns=("Amount", "From", "To", "Result", "Time"), show="headings")
        tree.pack(fill="both", expand=True)

        for col in ("Amount", "From", "To", "Result", "Time"):
            tree.heading(col, text=col)
        
        rows = self.db.fetch_history()
        for row in rows:
            tree.insert("", "end", values=row)


        def clear_and_close():
            self.db.clear_history()
            win.destroy()


        ttk.Button(win, text="Clear", command=clear_and_close).pack(pady=5)
        ttk.Button(win, text="Export CSV", command=lambda: export_to_csv(rows)).pack(pady=5)
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=5)