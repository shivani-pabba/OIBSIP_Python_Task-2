import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class BMI_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        self.label_font = ("Arial", 11)
        self.result_font = ("Arial", 13, "bold")

        self.bmi_data = []

        # Clear file on startup
        open("bmi_data.txt", "w").close()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter Weight (kg):", font=self.label_font, bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Enter Height (m):", font=self.label_font, bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.height_entry = tk.Entry(self.root)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi, bg="#4CAF50", fg="white", font=self.label_font).grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        tk.Button(self.root, text="Clear", command=self.clear_entries, bg="#f44336", fg="white", font=self.label_font).grid(row=2, column=1, padx=10, pady=10)

        self.result_label = tk.Label(self.root, text="", font=self.result_font, bg="#f0f0f0")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Setup only histogram
        self.figure = plt.Figure(figsize=(6, 3.2), dpi=100)
        self.ax_hist = self.figure.add_subplot(111)
        self.chart_canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.chart_canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if height <= 0:
                raise ZeroDivisionError

            bmi = weight / (height ** 2)
            category = self.get_category(bmi)
            color = self.get_color(category)

            self.result_label.config(text=f"Your BMI: {bmi:.2f} ({category})", fg=color)

            # Store only one BMI entry
            self.bmi_data = [(weight, height, bmi, category)]
            self.save_bmi_data(weight, height, bmi, category)
            self.plot_bmi_data()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
        except ZeroDivisionError:
            messagebox.showerror("Input Error", "Height must be greater than zero.")

    def get_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def get_color(self, category):
        return {
            "Underweight": "#FF6347",
            "Normal": "#008000",
            "Overweight": "#FFA500",
            "Obese": "#FF0000"
        }.get(category, "#000000")

    def plot_bmi_data(self):
        self.ax_hist.clear()
        bmi_values = [entry[2] for entry in self.bmi_data]
        self.ax_hist.hist(bmi_values, bins=5, color="#007ACC", edgecolor="black")
        self.ax_hist.set_title("Your BMI (Histogram)")
        self.ax_hist.set_xlabel("BMI")
        self.ax_hist.set_ylabel("Frequency")
        self.figure.tight_layout(pad=2.0)
        self.chart_canvas.draw()

    def save_bmi_data(self, weight, height, bmi, category):
        try:
            with open("bmi_data.txt", "w") as file:  # Overwrite file
                file.write(f"{weight},{height},{bmi},{category}\n")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save data: {e}")

    def clear_entries(self):
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.ax_hist.clear()
        self.chart_canvas.draw()
        self.bmi_data = []
        open("bmi_data.txt", "w").close()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()
