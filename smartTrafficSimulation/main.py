import tkinter as tk
import time

# Initial vehicle density
vehicle_density = {
    "North": 10,
    "South": 4,
    "East": 20,
    "West": 5
}

# Calculate green time based on vehicle density
def calculate_green_time(vehicle_count):
    return 5 + (vehicle_count // 2)

# Initialize signal timings
signal_timings = {direction: calculate_green_time(count) for direction, count in vehicle_density.items()}

# GUI window
root = tk.Tk()
root.title("Smart Traffic Signal Simulation")
root.geometry("500x700")  # Increased height

# Labels for directions
labels = {
    "North": tk.Label(root, text="North", width=20, height=2, bg="red", font=('Arial', 16)),
    "South": tk.Label(root, text="South", width=20, height=2, bg="red", font=('Arial', 16)),
    "East":  tk.Label(root, text="East",  width=20, height=2, bg="red", font=('Arial', 16)),
    "West":  tk.Label(root, text="West",  width=20, height=2, bg="red", font=('Arial', 16))
}

# Layout the labels in the window
labels["North"].pack(pady=5)
labels["South"].pack(pady=5)
labels["East"].pack(pady=5)
labels["West"].pack(pady=5)

# Vehicle count labels and entries
vehicle_entries = {}
for direction in ["North", "South", "East", "West"]:
    frame = tk.Frame(root)
    frame.pack()
    
    label = tk.Label(frame, text=f"{direction} Vehicle Count:", font=('Arial', 12))
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame, width=5, font=('Arial', 12))
    entry.insert(0, str(vehicle_density[direction]))  # default value
    entry.pack(side=tk.LEFT)

    vehicle_entries[direction] = entry

# Function to update vehicle count and recalculate signal timings
def update_vehicle_counts():
    global signal_timings
    for direction in vehicle_entries:
        try:
            count = int(vehicle_entries[direction].get())
            vehicle_density[direction] = count
            signal_timings[direction] = calculate_green_time(count)
        except ValueError:
            vehicle_density[direction] = 0
            signal_timings[direction] = 5
    print("✅ Vehicle counts updated!")
    print("🕒 New Signal Timings:", signal_timings)

# Button to update vehicle counts and signal timings
update_btn = tk.Button(root, text="Update Vehicle Density", command=update_vehicle_counts, font=('Arial', 12))
update_btn.pack(pady=10)

# Countdown labels
countdown_labels = {
    direction: tk.Label(root, text=f"{signal_timings[direction]}s", font=('Arial', 14), bg="white")
    for direction in ["North", "South", "East", "West"]
}
for lbl in countdown_labels.values():
    lbl.pack(pady=2)

# Canvas for simulation
canvas = tk.Canvas(root, width=400, height=200, bg="white")
canvas.pack(pady=10)

# Vehicle simulation
def animate_vehicles(direction, green_time):
    vehicle_size = 10
    speed = 5

    canvas.delete("all")  # Clear before each direction animation

    vehicles = []

    for i in range(min(vehicle_density[direction], 10)):  # Limit to 10 vehicles for clarity
        if direction == "North":
            x1, y1 = 180, 10 - i * 25
            x2, y2 = x1 + vehicle_size, y1 + vehicle_size
            dx, dy = 0, speed
        elif direction == "South":
            x1, y1 = 220, 190 + i * 25
            x2, y2 = x1 + vehicle_size, y1 + vehicle_size
            dx, dy = 0, -speed
        elif direction == "East":
            x1, y1 = 10 - i * 25, 100
            x2, y2 = x1 + vehicle_size, y1 + vehicle_size
            dx, dy = speed, 0
        elif direction == "West":
            x1, y1 = 390 + i * 25, 120
            x2, y2 = x1 + vehicle_size, y1 + vehicle_size
            dx, dy = -speed, 0
        
        rect = canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
        vehicles.append((rect, dx, dy))

    # Animate for green_time seconds
    for t in range(green_time):
        for rect, dx, dy in vehicles:
            canvas.move(rect, dx, dy)
        countdown_labels[direction].config(text=f"{green_time - t}s")
        root.update()
        time.sleep(1)

# Simulation logic
def run_simulation():
    directions = ["North", "South", "East", "West"]
    for cycle in range(3):
        for direction in directions:
            for lbl in labels.values():
                lbl.config(bg="red")
            labels[direction].config(bg="green")

            green_time = signal_timings[direction]
            animate_vehicles(direction, green_time)
            countdown_labels[direction].config(text="0s")
            root.update()
            time.sleep(0.5)

# Start Simulation Button
start_btn = tk.Button(root, text="Start Simulation", command=run_simulation, font=('Arial', 14), bg="green", fg="white")
start_btn.pack(pady=15)

root.mainloop()
