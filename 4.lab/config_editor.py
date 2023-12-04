import tkinter as tk
import os

def save_parameters():
    base_path = "./4.lab"
    config_path = os.path.join(base_path, "config.py")

    with open(config_path, "w") as file:  
        file.write(f'population_size = {int(population_size_entry.get())}\n')
        file.write(f'max_iterations = {int(max_iterations_entry.get())}\n')
        file.write(f'mutation_chance = {float(mutation_chance_entry.get())}\n')
        file.write(f'min_range = {float(min_range_entry.get())}\n')
        file.write(f'max_range = {float(max_range_entry.get())}\n')
        file.write(f'delay_between_iteration_sec = {float(delay_between_iteration_sec_entry.get())}\n')

    print(f"Parameters appended to '{config_path}' file.")

window = tk.Tk()
window.title("Configurator")

population_size_label = tk.Label(window, text="Population size (int):")
population_size_label.pack()
population_size_entry = tk.Entry(window)
population_size_entry.pack()

max_iterations_label = tk.Label(window, text="Max iterations (int):")
max_iterations_label.pack()
max_iterations_entry = tk.Entry(window)
max_iterations_entry.pack()

mutation_chance_label = tk.Label(window, text="Mutation chance (int):")
mutation_chance_label.pack()
mutation_chance_entry = tk.Entry(window)
mutation_chance_entry.pack()

min_range_label = tk.Label(window, text="Min range (float):")
min_range_label.pack()
min_range_entry = tk.Entry(window)
min_range_entry.pack()

max_range_label = tk.Label(window, text="Max range (float):")
max_range_label.pack()
max_range_entry = tk.Entry(window)
max_range_entry.pack()

delay_between_iteration_sec_label = tk.Label(window, text="Delay between iterations in seconds (float):")
delay_between_iteration_sec_label.pack()
delay_between_iteration_sec_entry = tk.Entry(window)
delay_between_iteration_sec_entry.pack()

save_button = tk.Button(window, text="Save Parameters", command=save_parameters)
save_button.pack()

window.mainloop()
