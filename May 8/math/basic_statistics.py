import numpy as np
import pandas as pd
import os

# Set the output directory for saving files
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

def calculate_basic_statistics():
    """Calculate and display basic statistics from the sales data"""
    print("=== Basic Sales Data Statistics using NumPy ===\n")
    
    # Load the CSV file
    csv_path = os.path.join(parent_dir, 'sales_data.csv')
    df = pd.read_csv(csv_path)
    
    # Extract numerical columns for analysis
    sales_array = df['Total_Sales'].to_numpy()
    units_array = df['Units_Sold'].to_numpy()
    price_array = df['Unit_Price'].to_numpy()
    

    # 1. Basic Statistics for Total Sales
    print("\n--- Total Sales Statistics ---")
    
    # Calculate statistics using NumPy
    mean_sales = np.mean(sales_array)
    median_sales = np.median(sales_array)
    std_sales = np.std(sales_array)
    var_sales = np.var(sales_array)
    
    # Output the results
    print(f"Mean (Average): ${mean_sales:.2f}")
    print(f"Median: ${median_sales:.2f}")
    print(f"Standard Deviation: ${std_sales:.2f}")
    print(f"Variance: ${var_sales:.2f}")
    
    # 2. Statistics for Units Sold
    print("\n--- Units Sold Statistics ---")
    
    # Calculate statistics
    mean_units = np.mean(units_array)
    median_units = np.median(units_array)
    std_units = np.std(units_array)
    var_units = np.var(units_array)
    
    # Output the results
    print(f"Mean (Average): {mean_units:.2f} units")
    print(f"Median: {median_units:.2f} units")
    print(f"Standard Deviation: {std_units:.2f} units")
    print(f"Variance: {var_units:.2f}")
    
    # 3. Statistics for Unit Price
    print("\n--- Unit Price Statistics ---")
    
    # Calculate statistics
    mean_price = np.mean(price_array)
    median_price = np.median(price_array)
    std_price = np.std(price_array)
    var_price = np.var(price_array)
    
    # Output the results
    print(f"Mean (Average): ${mean_price:.2f}")
    print(f"Median: ${median_price:.2f}")
    print(f"Standard Deviation: ${std_price:.2f}")
    print(f"Variance: ${var_price:.2f}")
    
    print("\n=== Basic Statistics Calculation Completed ===")

if __name__ == "__main__":
    calculate_basic_statistics()
