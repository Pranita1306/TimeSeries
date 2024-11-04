import pandas as pd
import numpy as np
import random
import os

def sample_30_data_points(file_path):
   
    data = pd.read_csv(file_path)
    
    data = data.sort_values(by="Timestamp").reset_index(drop=True)
    
    
    max_start_index = len(data) - 30
    if max_start_index < 0:
        raise ValueError("The file has fewer than 30 data points.")
    
   
    start_index = random.randint(0, max_start_index)   
    
    sampled_data = data.iloc[start_index:start_index + 30].copy()
    
    return sampled_data

def identify_outliers(sampled_data):
   
    mean_price = sampled_data["Stock Price"].mean()
    std_price = sampled_data["Stock Price"].std()
    
    upper_threshold = mean_price + 2 * std_price
    lower_threshold = mean_price - 2 * std_price
    
    sampled_data["Deviation"] = sampled_data["Stock Price"] - mean_price
    sampled_data["% Deviation"] = (sampled_data["Deviation"].abs() / (2 * std_price)) * 100
    sampled_data["Mean"] = mean_price
    outliers = sampled_data[(sampled_data["Stock Price"] > upper_threshold) | (sampled_data["Stock Price"] < lower_threshold)]
    
    outliers = outliers[["Stock-ID", "Timestamp", "Stock Price", "Mean" "Deviation", "% Deviation"]]
    return outliers, mean_price

def process_files(file_paths, output_directory, sampled_files):
    if sampled_files < 1:
        raise ValueError("sampled_files must be at least 1.")
    for file_path in file_paths:
        try:
            
            sampled_data = sample_30_data_points(file_path)        
            
            outliers, mean_price = identify_outliers(sampled_data)
            
                if not outliers.empty:
                stock_id = sampled_data["Stock-ID"].iloc[0]
                output_file = os.path.join(output_directory, f"{stock_id}_outliers.csv")
                outliers.to_csv(output_file, index=False)
                print(f"Outliers written to {output_file}")
            else:
                print(f"No outliers found in {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

no_of_sampled_files = int(input("Enter no of files sampled for an exchange: "))

folder_path = input("Enter the excahnge: ")
all_entries = os.listdir(folder_path)
    
files = [entry for entry in all_entries if os.path.isfile(os.path.join(folder_path, entry))]

output_directory = "output_directory" 
process_files(files, output_directory, no_of_sampled_files)
