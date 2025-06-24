import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Data storage for plots and CSV
flight_data = []
aoa_history = []
lift_history = []

# AoA and Lift Calculation
def calculate_aoa(vertical_speed, horizontal_speed):
    if horizontal_speed == 0:
        return math.pi / 2, 90.0
    aoa_rad = math.atan(vertical_speed / horizontal_speed)
    return aoa_rad, math.degrees(aoa_rad)

def calculate_lift(air_density, wing_area, v_total, cl):
    return 0.5 * air_density * v_total ** 2 * wing_area * cl

def update_results():
    try:
        v_vertical = float(entry_vertical.get())
        v_horizontal = float(entry_horizontal.get())
        wing_area = float(entry_area.get())
        air_density = float(entry_density.get())

        v_total = math.sqrt(v_vertical ** 2 + v_horizontal ** 2)
        aoa_rad, aoa_deg = calculate_aoa(v_vertical, v_horizontal)
        cl = 2 * math.pi * aoa_rad
        lift = calculate_lift(air_density, wing_area, v_total, cl)

        label_aoa.config(text=f"AoA: {aoa_deg:.2f}°")
        label_lift.config(text=f"Lift: {lift:.2f} N")
        label_cl.config(text=f"Cl: {cl:.2f}")

        if aoa_deg > 15:
            label_warning.config(text="Stall Warning! High AoA")
        else:
            label_warning.config(text="")

        aoa_history.append(aoa_deg)
        lift_history.append(lift)
        flight_data.append([v_vertical, v_horizontal, aoa_deg, lift, cl])
        update_plot()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def update_plot():
    ax.clear()
    ax.set_title("AoA vs Lift")
    ax.set_xlabel("AoA (°)")
    ax.set_ylabel("Lift (N)")
    ax.grid(True)
    ax.plot(aoa_history, lift_history, marker='o', linestyle='-')
    canvas.draw()

def load_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return
    try:
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                v_vertical = float(row['VerticalSpeed'])
                v_horizontal = float(row['HorizontalSpeed'])
                entry_vertical.delete(0, tk.END)
                entry_horizontal.delete(0, tk.END)
                entry_vertical.insert(0, str(v_vertical))
                entry_horizontal.insert(0, str(v_horizontal))
                update_results()
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to load file: {e}")

def save_csv():
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return
    try:
        file_exists = os.path.exists(filepath)
        with open(filepath, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['VerticalSpeed', 'HorizontalSpeed', 'AoA', 'Lift', 'Cl'])
            writer.writerows(flight_data)
        messagebox.showinfo("Saved", f"Flight data appended to {filepath}")
        flight_data.clear()  # Optional: clear after saving
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save file: {e}")

# GUI Setup
root = tk.Tk()
root.title("Flight AoA & Lift Simulator")
root.geometry("900x650")

frame = ttk.Frame(root, padding="10")
frame.pack(fill="x")

# Input Fields
ttk.Label(frame, text="Vertical Speed (m/s):").grid(column=0, row=0, sticky="w")
entry_vertical = ttk.Entry(frame)
entry_vertical.grid(column=1, row=0)

ttk.Label(frame, text="Horizontal Speed (m/s):").grid(column=0, row=1, sticky="w")
entry_horizontal = ttk.Entry(frame)
entry_horizontal.grid(column=1, row=1)

ttk.Label(frame, text="Wing Area (m²):").grid(column=0, row=2, sticky="w")
entry_area = ttk.Entry(frame)
entry_area.grid(column=1, row=2)

ttk.Label(frame, text="Air Density (kg/m³):").grid(column=0, row=3, sticky="w")
entry_density = ttk.Entry(frame)
entry_density.insert(0, "1.225")
entry_density.grid(column=1, row=3)

# Output Labels
label_aoa = ttk.Label(frame, text="AoA: --")
label_aoa.grid(column=0, row=4, columnspan=2, pady=(10, 0))

label_lift = ttk.Label(frame, text="Lift: --")
label_lift.grid(column=0, row=5, columnspan=2)

label_cl = ttk.Label(frame, text="Cl: --")
label_cl.grid(column=0, row=6, columnspan=2)

label_warning = ttk.Label(frame, text="", foreground="red")
label_warning.grid(column=0, row=7, columnspan=2)

# Buttons
ttk.Button(frame, text="Calculate", command=update_results).grid(column=0, row=8, columnspan=2, pady=10)
ttk.Button(frame, text="Load CSV", command=load_csv).grid(column=0, row=9, pady=5)
ttk.Button(frame, text="Save CSV", command=save_csv).grid(column=1, row=9, pady=5)

# Matplotlib Plot
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

root.mainloop()
