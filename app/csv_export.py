import csv
from tkinter import filedialog, messagebox


def export_to_csv(rows):
    if not rows:
        messagebox.showinfo("No DAta", "No history available to export")
        return
    
    file_path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if not file_path:
        return
    
    try:
        with open(file_path, "w",newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "From", "To", "Result", "Timestamp"])
            writer.writerows(rows)
        messagebox.showinfo("Export Successful", f"History exported to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Export Failed", str(e))
