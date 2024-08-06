import tkinter as tk
from tkinter import messagebox
from chickensim import plot_population

class ChickenSimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chicken Population Simulation")

        self.create_widgets()

    def create_widgets(self):
        # Initial Adults
        tk.Label(self.root, text="Initial Adults:").grid(row=0, column=0)
        self.adults_entry = tk.Entry(self.root)
        self.adults_entry.grid(row=0, column=1)

        # Initial Babies
        tk.Label(self.root, text="Initial Babies:").grid(row=1, column=0)
        self.babies_entry = tk.Entry(self.root)
        self.babies_entry.grid(row=1, column=1)

        # Dispenser Rate
        tk.Label(self.root, text="Dispenser Rate (seconds):").grid(row=2, column=0)
        self.dispenser_rate_entry = tk.Entry(self.root)
        self.dispenser_rate_entry.grid(row=2, column=1)

        # Simulation Duration
        tk.Label(self.root, text="Simulation Duration (minutes):").grid(row=3, column=0)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=3, column=1)

        # Start Simulation Button
        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=4, column=0, columnspan=2)

    def start_simulation(self):
        try:
            adults = int(self.adults_entry.get())
            babies = int(self.babies_entry.get())
            dispenser_rate = float(self.dispenser_rate_entry.get())
            duration = int(self.duration_entry.get())
            plot_population(adults, babies, dispenser_rate, duration)
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChickenSimulationGUI(root)
    root.mainloop()