from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import os, sys
from tkinter import messagebox as m

WINDOW_SIZE = "720x900"
APP_TITLE = "🏃‍♂️ Health BMI Tracker"
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 45
ENTRY_WIDTH = 280
ENTRY_HEIGHT = 35

COLORS = {
    "primary": "#6366f1",
    "secondary": "#ec4899",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#06b6d4",
    "dark": "#1f2937",
    "light": "#f9fafb"
}

BMI_CATEGORIES = {
    "underweight": {"max": 18.5, "color": COLORS["info"], "text": "⚡ LOW BMI\nOptimize nutrition intake"},
    "normal": {"min": 18.5, "max": 24.9, "color": COLORS["success"], "text": "✓ OPTIMAL RANGE\nMaintaining peak health"},
    "overweight": {"min": 25.0, "max": 29.9, "color": COLORS["warning"], "text": "⚠ ELEVATED BMI\nActivate fitness protocol"},
    "obese": {"min": 30.0, "max": 34.9, "color": COLORS["danger"], "text": "🔴 HIGH RISK\nConsult health specialist"},
    "extreme": {"min": 35, "color": "#dc2626", "text": "🚨 CRITICAL LEVEL\nImmediate medical attention"}
}

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title(APP_TITLE)
root.geometry(WINDOW_SIZE)
root.resizable(False, False)
root.configure(fg_color=COLORS["light"])

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def validate_inputs():
    if not h_entry.get() or not w_entry.get():
        m.showerror(APP_TITLE, "Enter Values first to Calculate")
        return False
    try:
        float(h_entry.get())
        float(w_entry.get())
        return True
    except ValueError:
        m.showerror(APP_TITLE, "Please enter valid numbers")
        return False

def get_bmi_category(bmi):
    for category, data in BMI_CATEGORIES.items():
        if category == "underweight" and bmi < data["max"]:
            return data
        elif category == "extreme" and bmi >= data["min"]:
            return data
        elif "min" in data and "max" in data and data["min"] <= bmi <= data["max"]:
            return data
    return BMI_CATEGORIES["normal"]

def calculate_bmi():
    if not validate_inputs():
        return
    
    height_feet = float(h_entry.get())
    weight_kg = float(w_entry.get())
    
    weight_pounds = weight_kg / 0.453592
    height_inches = height_feet * 12
    bmi = (weight_pounds / (height_inches ** 2)) * 703
    bmi_rounded = round(bmi, 2)
    
    category = get_bmi_category(bmi_rounded)
    results.configure(
        text=f"BMI: {bmi_rounded}\n{category['text']}", 
        text_color=category["color"]
    )
    
    update_bmi_indicator(bmi_rounded)

def clear_screen(event=None):
    h_entry.delete(0, END)
    w_entry.delete(0, END)
    results.configure(text="Enter your details to calculate BMI", text_color=COLORS["dark"])

def create_entry_with_label(placeholder, focus_text, focus_color):
    label = customtkinter.CTkLabel(
        master=root, 
        text="", 
        font=("Segoe UI", 16, "bold"),
        text_color=COLORS["dark"]
    )
    label.pack(pady=(10, 0))
    
    entry = customtkinter.CTkEntry(
        master=root,
        placeholder_text=placeholder,
        width=ENTRY_WIDTH,
        height=ENTRY_HEIGHT,
        border_width=2,
        corner_radius=15,
        font=("Segoe UI", 14),
        border_color=COLORS["primary"],
        fg_color="white",
        text_color=COLORS["dark"]
    )
    entry.pack(pady=(5, 15))
    entry.bind("<FocusIn>", lambda e: label.configure(text=focus_text, text_color=focus_color))
    entry.bind("<FocusOut>", lambda e: label.configure(text=""))
    
    return entry


header_label = customtkinter.CTkLabel(
    master=root,
    text="BMI HEALTH ANALYZER",
    font=("Segoe UI", 26, "bold"),
    text_color=COLORS["primary"]
)
header_label.pack(pady=(20, 10))

subtitle_label = customtkinter.CTkLabel(
    master=root,
    text="ADVANCED BODY MASS INDEX MONITORING SYSTEM",
    font=("Segoe UI", 11),
    text_color=COLORS["dark"]
)
subtitle_label.pack(pady=(0, 20))

def create_bmi_meter():
    meter_frame = customtkinter.CTkFrame(
        master=root,
        width=400,
        height=200,
        corner_radius=15,
        fg_color="white",
        border_width=2,
        border_color=COLORS["primary"]
    )
    meter_frame.pack(pady=20)
    
    meter_title = customtkinter.CTkLabel(
        master=meter_frame,
        text="BMI ANALYSIS SCALE",
        font=("Segoe UI", 16, "bold"),
        text_color=COLORS["dark"]
    )
    meter_title.pack(pady=(15, 10))
    
    scale_frame = customtkinter.CTkFrame(meter_frame, fg_color="transparent")
    scale_frame.pack(pady=10)
    
    categories = [
        ("LOW", COLORS["info"], "<18.5"),
        ("OPTIMAL", COLORS["success"], "18.5-24.9"),
        ("ELEVATED", COLORS["warning"], "25.0-29.9"),
        ("HIGH", COLORS["danger"], "30.0-34.9"),
        ("CRITICAL", "#dc2626", "≥35.0")
    ]
    
    for i, (name, color, range_text) in enumerate(categories):
        bar = customtkinter.CTkFrame(
            master=scale_frame,
            width=65,
            height=25,
            fg_color=color,
            corner_radius=8
        )
        bar.grid(row=0, column=i, padx=3)
        
        label = customtkinter.CTkLabel(
            master=scale_frame,
            text=name,
            font=("Segoe UI", 10, "bold"),
            text_color=COLORS["dark"]
        )
        label.grid(row=1, column=i, pady=(8, 2))
        
        range_label = customtkinter.CTkLabel(
            master=scale_frame,
            text=range_text,
            font=("Segoe UI", 11, "bold"),
            text_color=COLORS["primary"]
        )
        range_label.grid(row=2, column=i, pady=(0, 5))
    
    global bmi_indicator
    bmi_indicator = customtkinter.CTkLabel(
        master=meter_frame,
        text="▼",
        font=("Segoe UI", 20, "bold"),
        text_color=COLORS["primary"]
    )
    
    return meter_frame

def update_bmi_indicator(bmi_value):
    if bmi_value < 18.5:
        position = 0
        color = COLORS["info"]
    elif bmi_value < 25:
        position = 1
        color = COLORS["success"]
    elif bmi_value < 30:
        position = 2
        color = COLORS["warning"]
    elif bmi_value < 35:
        position = 3
        color = COLORS["danger"]
    else:
        position = 4
        color = "#dc2626"
    
    bmi_indicator.configure(text_color=color)
    bmi_indicator.pack(pady=(0, 15))

meter_widget = create_bmi_meter()

h_entry = create_entry_with_label("HEIGHT INPUT (feet)", "📏 Height measurement in feet", COLORS["primary"])
w_entry = create_entry_with_label("WEIGHT INPUT (kg)", "⚖️ Weight measurement in kilograms", COLORS["secondary"])

calculate_btn = customtkinter.CTkButton(
    master=root,
    text="⚡ ANALYZE BMI",
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    font=("Segoe UI", 16, "bold"),
    fg_color=COLORS["primary"],
    hover_color="#5856eb",
    corner_radius=20,
    command=calculate_bmi,
)
calculate_btn.pack(pady=15)

clear_btn = customtkinter.CTkButton(
    master=root,
    text="� RESET DATA",
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    font=("Segoe UI", 16, "bold"),
    fg_color=COLORS["secondary"],
    hover_color="#e11d7e",
    corner_radius=20,
    command=clear_screen,
)
clear_btn.pack(pady=(5, 15))

results_frame = customtkinter.CTkFrame(
    master=root,
    width=350,
    height=130,
    corner_radius=20,
    fg_color=COLORS["light"],
    border_width=2,
    border_color=COLORS["primary"]
)
results_frame.pack(pady=20)

results = customtkinter.CTkLabel(
    master=results_frame, 
    text="READY FOR BMI ANALYSIS", 
    font=("Segoe UI", 16, "bold"),
    text_color=COLORS["dark"],
    wraplength=300
)
results.pack(pady=30)

def clear_screen(event=None):
    h_entry.delete(0, END)
    w_entry.delete(0, END)
    results.configure(text="READY FOR BMI ANALYSIS", text_color=COLORS["dark"])

if __name__ == "__main__":
    root.mainloop()
