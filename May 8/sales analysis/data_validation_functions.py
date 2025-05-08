import pandas as pd
import numpy as np
import os

# Set the output directory for saving files
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

def load_sales_data():
    """Load the sales data from CSV file"""
    csv_path = os.path.join(parent_dir, 'sales_data.csv')
    df = pd.read_csv(csv_path)
    
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def check_null_values(df):
    """Check for null values in the dataset"""
    print("\n=== Null Values Check ===")
    
    # Count null values in each column
    null_counts = df.isnull().sum()
    
    # Check  any null values
    if null_counts.sum() == 0:
        print("No null values found in the dataset.")
    else:
        print("Null values found in the following columns:")
        for column, count in null_counts.items():
            if count > 0:
                print(f"- {column}: {count} null values")
    
    # Calculate percentage of null values
    null_percentage = (df.isnull().sum() / len(df)) * 100
    
    # Display columns with null values (if any)
    columns_with_nulls = null_percentage[null_percentage > 0]
    if not columns_with_nulls.empty:
        print("\nPercentage of null values by column:")
        for column, percentage in columns_with_nulls.items():
            print(f"- {column}: {percentage:.2f}%")
    
    return null_counts

def check_duplicates(df):
    """Check for duplicate records in the dataset"""
    print("\n=== Duplicate Records Check ===")
    
    # Count duplicate rows
    duplicate_count = df.duplicated().sum()
    
    if duplicate_count == 0:
        print("No duplicate records found in the dataset.")
    else:
        print(f"Found {duplicate_count} duplicate records in the dataset.")
        
        # Show a sample of duplicate records
        duplicate_rows = df[df.duplicated(keep='first')]
        if not duplicate_rows.empty:
            print("\nSample of duplicate records:")
            print(duplicate_rows.head(3))
    
    return duplicate_count

def check_data_types(df):
    """Check data types of each column"""
    print("\n=== Data Types Check ===")
    
    # Get data types
    data_types = df.dtypes
    
    print("Data types for each column:")
    for column, dtype in data_types.items():
        print(f"- {column}: {dtype}")
    
    return data_types

def check_value_ranges(df):
    """Check the range of values in numerical columns"""
    print("\n=== Value Ranges Check ===")
    
    # Identify numerical columns
    numerical_columns = df.select_dtypes(include=['number']).columns
    
    print("Value ranges for numerical columns:")
    for column in numerical_columns:
        min_val = df[column].min()
        max_val = df[column].max()
        
        if column in ['Total_Sales', 'Unit_Price']:
            print(f"- {column}: ${min_val:.2f} to ${max_val:.2f}")
        else:
            print(f"- {column}: {min_val} to {max_val}")
    
    return {col: (df[col].min(), df[col].max()) for col in numerical_columns}

def check_categorical_values(df):
    """Check unique values in categorical columns"""
    print("\n=== Categorical Values Check ===")
    
    # Identify categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    for column in categorical_columns:
        unique_values = df[column].unique()
        value_counts = df[column].value_counts()
        
        print(f"\n{column} - Unique Values: {len(unique_values)}")
        print("Value counts:")
        for value, count in value_counts.items():
            print(f"- {value}: {count} ({count/len(df)*100:.1f}%)")
    
    return {col: df[col].unique() for col in categorical_columns}

def check_date_range(df):
    """Check the range of dates in the dataset"""
    print("\n=== Date Range Check ===")
    
    # Check if Date column exists and is datetime
    if 'Date' in df.columns and pd.api.types.is_datetime64_any_dtype(df['Date']):
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        date_range = max_date - min_date
        
        print(f"Date range: {min_date.date()} to {max_date.date()}")
        print(f"Total time span: {date_range.days} days")
        
        # Count records by month
        monthly_counts = df.groupby(df['Date'].dt.strftime('%Y-%m')).size()
        
        print("\nRecords by month:")
        for month, count in monthly_counts.items():
            print(f"- {month}: {count} records")
    else:
        print("No valid date column found in the dataset.")
    
    return min_date, max_date if 'Date' in df.columns else None

def check_for_outliers(df):
    """Check for outliers in numerical columns using IQR method"""
    print("\n=== Outliers Check ===")
    
    # Identify numerical columns
    numerical_columns = df.select_dtypes(include=['number']).columns
    
    outliers_summary = {}
    
    for column in numerical_columns:
        # Calculate IQR
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outlier boundaries
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Find outliers
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        outlier_count = len(outliers)
        
        # Store results
        outliers_summary[column] = {
            'outlier_count': outlier_count,
            'percentage': outlier_count / len(df) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
        
        # Print results
        if column in ['Total_Sales', 'Unit_Price']:
            print(f"\n{column}:")
            print(f"- Outlier boundaries: ${lower_bound:.2f} to ${upper_bound:.2f}")
            print(f"- Outliers found: {outlier_count} ({outlier_count/len(df)*100:.1f}%)")
        else:
            print(f"\n{column}:")
            print(f"- Outlier boundaries: {lower_bound:.2f} to {upper_bound:.2f}")
            print(f"- Outliers found: {outlier_count} ({outlier_count/len(df)*100:.1f}%)")
    
    return outliers_summary

def main():
    """Main function to run all data validation checks"""
    print("=== Sales Data Validation Functions ===\n")
    

    # Load the data
    df = load_sales_data()
    print(f"Loaded sales data with {len(df)} records")
    
    # Run validation checks
    check_null_values(df)
    check_duplicates(df)
    check_data_types(df)
    check_value_ranges(df)
    check_categorical_values(df)
    check_date_range(df)
    check_for_outliers(df)
    
    print("\n=== Data Validation Complete ===")


if __name__ == "__main__":
    main()
