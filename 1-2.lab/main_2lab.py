import tkinter as tk
from tkinter import filedialog
import concurrent.futures
from datetime import datetime
import json
import os
import pandas as pd
import numpy as np
import tkinter.simpledialog as sd

def process_data_and_save(chunk):
    #size checker
    # Create a DataFrame
    df = pd.DataFrame(chunk)
    num_threads=None
    if num_threads is None:
        num_threads = os.cpu_count() or 1
    num_line = num_threads * df.shape[0]
    
    def generalize_quasi_identifier(row, precision=2):
        start_latitude = 59.93
        start_longitude = 30.36

        # Extract coordinates, split, and convert to float
        coordinates = row
        latitude, longitude = map(float, coordinates.split(','))

        # Rounding to the specified precision
        lat_rounded = round(latitude, precision)
        lon_rounded = round(longitude, precision)

        # Determine the direction based on proximity
        if abs(latitude - start_latitude) <= abs(longitude - start_longitude):
            latitude_direction = 'север' if latitude >= start_latitude else 'юг'
            longitude_direction = 'восток' if longitude >= start_longitude else 'запад'
        else:
            latitude_direction = 'север' if latitude >= start_latitude else 'юг'
            longitude_direction = 'восток' if longitude >= start_longitude else 'запад'

        return f"{latitude_direction}-{longitude_direction}".strip()
    if num_line <= 51000:
                # Place
        df['place'] = df['place'].apply(generalize_quasi_identifier)

        # Date
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.quarter
        df['date'] = df['year'].astype(str) + '.' + df['month'].astype(str)
        df = df.drop(columns=['year', 'month'])
        
        df['time'] = pd.to_datetime(df['time'])

        # Extract hour
        df['hour'] = df['time'].dt.hour

        # Define a function to map hours to time intervals
        def map_to_time_interval(hour):
            if 7 < hour <= 13:
                return '8:00-13:00'
            elif 13 < hour <= 16:
                return '13:01-16:00'
            elif 16 < hour:
                return '16:01-22:00'

        # Apply the function to create a new 'time_interval' column
        df['time'] = df['hour'].apply(map_to_time_interval)
        df = df.drop(columns = ['hour'])
        
        # Card_Numbers
        df['card_number'] = df['card_number'].apply(lambda x: f"xxx")
        
        def price_range(price):
            if price >= 50000:
                return "51000-100000"
            else:
                return "1000-50000"

        #Price
        df['price'] = df['price'].apply(lambda x: price_range(x))
        
        # Other
        df['name_of_shop'] = df['name_of_shop'].apply(lambda x: "xxx")
        df['cathegory_of_item'] = df['cathegory_of_item']
        df['item_brand'] = df['item_brand']
        
        
    if 51000 <= num_line <= 105000:
        # Place
        df['place'] = df['place'].apply(generalize_quasi_identifier)

        # Date
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.quarter
        df['date'] = df['year'].astype(str) + '.' + df['month'].astype(str)
        df = df.drop(columns=['year', 'month'])
        
        df['time'] = pd.to_datetime(df['time'])

        # Extract hour
        df['hour'] = df['time'].dt.hour

        # Define a function to map hours to time intervals
        def map_to_time_interval(hour):
            if 7 < hour <= 13:
                return '8:00-13:00'
            elif 13 < hour <= 16:
                return '13:01-16:00'
            elif 16 < hour:
                return '16:01-22:00'

        # Apply the function to create a new 'time_interval' column
        df['time'] = df['hour'].apply(map_to_time_interval)
        df = df.drop(columns = ['hour'])
        
        # Card_Numbers
        df['card_number'] = df['card_number'].apply(lambda x: f"xxx")
        
        def price_range(price):
            if price >= 66000:
                return "66000-100000"
            elif 66000 > price >= 33000:
                return "65000-33000"
            else:
                return "32000-1000"
        
        #Price
        df['price'] = df['price'].apply(lambda x: price_range(x))
        
        # Other
        df['name_of_shop'] = df['name_of_shop'].apply(lambda x: "xxx")
        df['cathegory_of_item'] = df['cathegory_of_item']
        df['item_brand'] = df['item_brand']
        
        
    if 105000 <= num_line:
                # Place
        df['place'] = df['place'].apply(generalize_quasi_identifier)

        # Date
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.quarter
        df['date'] = df['year'].astype(str) + '.' + df['month'].astype(str)
        df = df.drop(columns=['year', 'month'])
        
        df['time'] = pd.to_datetime(df['time'])

        # Extract hour
        df['hour'] = df['time'].dt.hour

        # Define a function to map hours to time intervals
        def map_to_time_interval(hour):
            if 8 < hour <= 12:
                return '8:00-12:00'
            elif 12 < hour <= 14:
                return '12:01-14:00'
            elif 14 < hour <= 16:
                return '14:01-16:00'
            elif 16 < hour <= 18:
                return '16:01-18:00'
            elif 18 < hour <= 22:
                return '18:01-22:00'

        # Apply the function to create a new 'time_interval' column
        df['time'] = df['hour'].apply(map_to_time_interval)
        df = df.drop(columns = ['hour'])
        
        # Card_Numbers
        df['card_number'] = df['card_number'].apply(lambda x: f"xxx")
        
        def price_range(price):
            if price >= 835000:
                return "83500-100000"
            elif 83500 > price >= 67000:
                return "83500-67000"
            elif 67000 > price >= 50500:
                return "67000-50500"
            elif 50500 > price >= 34000:
                return "50500-34000"
            elif 34000 > price >= 17500:
                return "34000-17500"
            else:
                return "17500-1000"
        
        #Price
        df['price'] = df['price'].apply(lambda x: price_range(x))
        
        # Other
        df['name_of_shop'] = df['name_of_shop'].apply(lambda x: "xxx")
        df['cathegory_of_item'] = df['cathegory_of_item']
        df['item_brand'] = df['item_brand']
        
        

        return df
    else:
        pass

def process_data_and_save_parallel(file_path, num_threads=None):
    # Determine the number of threads if not specified
    start_time = datetime.now()
    if num_threads is None:
        num_threads = os.cpu_count() or 1

    # Load the example data
    with open(file_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    # Split the dataset into chunks for parallel processing
    chunk_size = len(dataset) // num_threads
    chunks = [dataset[i:i + chunk_size] for i in range(0, len(dataset), chunk_size)]

    # Process each chunk in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        dfs = list(executor.map(process_data_and_save, chunks))
        
    df_result = pd.concat(dfs, ignore_index=True)

    analyzed_json_path = "./1-2.lab/result/analyzed.json"
    df_result.to_json(analyzed_json_path, orient="records", lines=True, force_ascii=False, default_handler=str)

    # Read the file again and write JSON data with UTF-8 encoding in the desired format
    with open(analyzed_json_path, 'r', encoding='utf-8') as json_file:
        data = [json.loads(line) for line in json_file]

    with open(analyzed_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # Save obfuscated data to analyzed.xlsx
    analyzed_xlsx_path = "./1-2.lab/result/analyzed.xlsx"
    df_result.to_excel(analyzed_xlsx_path, index=False)

    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Time taken for processing: {execution_time}")

def calculate_k_anonymity(data, quasi_identifiers):
    data_matrix = np.array([list(d.values()) for d in data])

    # Get column indices corresponding to quasi identifiers
    column_indices = [list(data[0].keys()).index(column) for column in quasi_identifiers]

    # Convert data types to numeric
    quasi_identifiers_columns = data_matrix[:, column_indices].astype(str)
    
    frequencies = np.unique(quasi_identifiers_columns, axis=0, return_counts=True)

    # Calculate k-anonymity
    k_anonymity = np.min(frequencies[1])

    return k_anonymity


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

# Program picker
def run_program(program_number):
    if program_number == 1:
        file_path = os.path.join(os.getcwd(), './1-2.lab/result', 'output.json')
        start_time = datetime.now()
        process_data_and_save_parallel(file_path)
        end_time = datetime.now()
        execution_time = end_time - start_time
        time_label.config(text=f"Time taken for de-identifying: {execution_time}")
    elif program_number == 2:
        file_path = "./1-2.lab/result/analyzed.json"
        data = load_data(file_path)
        if data:
            quasi_identifiers_list = ["date","place","time","price"]
            k_anonymity_result = calculate_k_anonymity(data, quasi_identifiers_list)
            k_anonymity_label.config(text=f"K-anonymity: {k_anonymity_result}")

# GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Program Selection")

    button1 = tk.Button(root, text="1. De-identificator", command=lambda: run_program(1))
    button1.pack(pady=10)

    button2 = tk.Button(root, text="2. Anonymity Analyzer", command=lambda: run_program(2))
    button2.pack(pady=10)

    # Labels to display time and K-anonymity
    time_label = tk.Label(root, text="")
    time_label.pack()

    k_anonymity_label = tk.Label(root, text="")
    k_anonymity_label.pack()

    root.mainloop()
