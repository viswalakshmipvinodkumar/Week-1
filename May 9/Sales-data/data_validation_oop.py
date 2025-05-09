"""
Data Validation and Statistics OOP Implementation
- Implements classes for data validation, statistics, and output generation
- Demonstrates encapsulation, inheritance, and other OOP concepts
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime

class DataLoader:
    """Class for loading data from various sources."""
    
    def __init__(self, file_path=None):
        """Initialize with an optional file path."""
        self.file_path = file_path
        self.data = None
    
    def load_csv(self, file_path=None):
        """Load data from a CSV file."""
        if file_path:
            self.file_path = file_path
        
        if not self.file_path:
            raise ValueError("No file path provided")
        
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"Successfully loaded data from {self.file_path}")
            print(f"Data shape: {self.data.shape}")
            return self.data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def get_data(self):
        """Return the loaded data."""
        return self.data


class DataValidator:
    """Class for validating data quality."""
    
    def __init__(self, data):
        """Initialize with the data to validate."""
        self.data = data
        self.validation_results = {}
    
    def check_null_values(self):
        """Check for null values in the dataset."""
        print("\n=== Null Values Check ===")
        
        # Count null values in each column
        null_counts = self.data.isnull().sum()
        
        # Check if there are any null values
        if null_counts.sum() == 0:
            print("No null values found in the dataset.")
        else:
            print("Null values found in the following columns:")
            for column, count in null_counts.items():
                if count > 0:
                    print(f"- {column}: {count} null values")
        
        # Calculate percentage of null values
        null_percentage = (self.data.isnull().sum() / len(self.data)) * 100
        
        # Display columns with null values (if any)
        columns_with_nulls = null_percentage[null_percentage > 0]
        if not columns_with_nulls.empty:
            print("\nPercentage of null values by column:")
            for column, percentage in columns_with_nulls.items():
                print(f"- {column}: {percentage:.2f}%")
        
        # Store results
        self.validation_results['null_values'] = {
            'null_counts': null_counts,
            'null_percentage': null_percentage
        }
        
        return null_counts
    
    def check_duplicates(self):
        """Check for duplicate records in the dataset."""
        print("\n=== Duplicate Records Check ===")
        
        # Count duplicate rows
        duplicate_count = self.data.duplicated().sum()
        duplicate_percentage = (duplicate_count / len(self.data)) * 100
        
        print(f"Duplicate records: {duplicate_count} ({duplicate_percentage:.2f}%)")
        
        # Store results
        self.validation_results['duplicates'] = {
            'count': duplicate_count,
            'percentage': duplicate_percentage
        }
        
        return duplicate_count
    
    def check_data_types(self):
        """Check data types of each column."""
        print("\n=== Data Types Check ===")
        
        # Get data types
        dtypes = self.data.dtypes
        
        print("Column data types:")
        for column, dtype in dtypes.items():
            print(f"- {column}: {dtype}")
        
        # Store results
        self.validation_results['data_types'] = dtypes
        
        return dtypes
    
    def check_value_ranges(self):
        """Check the range of values in numerical columns."""
        print("\n=== Value Ranges Check ===")
        
        # Identify numerical columns
        numerical_columns = self.data.select_dtypes(include=['number']).columns
        
        ranges = {}
        for column in numerical_columns:
            min_val = self.data[column].min()
            max_val = self.data[column].max()
            
            print(f"\n{column}:")
            if column in ['Sales', 'Price']:
                print(f"- Range: ${min_val:.2f} to ${max_val:.2f}")
            else:
                print(f"- Range: {min_val} to {max_val}")
            
            ranges[column] = {
                'min': min_val,
                'max': max_val
            }
        
        # Store results
        self.validation_results['value_ranges'] = ranges
        
        return ranges
    
    def check_categorical_values(self):
        """Check unique values in categorical columns."""
        print("\n=== Categorical Values Check ===")
        
        # Identify categorical columns
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        
        categorical_summary = {}
        for column in categorical_columns:
            unique_values = self.data[column].unique()
            value_counts = self.data[column].value_counts()
            
            print(f"\n{column}:")
            print(f"- Unique values: {len(unique_values)}")
            print("- Top 5 most common values:")
            for value, count in value_counts.head(5).items():
                print(f"  * {value}: {count} ({count/len(self.data)*100:.1f}%)")
            
            categorical_summary[column] = {
                'unique_count': len(unique_values),
                'value_counts': value_counts
            }
        
        # Store results
        self.validation_results['categorical_values'] = categorical_summary
        
        return categorical_summary
    
    def check_date_range(self):
        """Check the range of dates in the dataset."""
        print("\n=== Date Range Check ===")
        
        date_columns = []
        
        # Find date columns
        for column in self.data.columns:
            if 'date' in column.lower() or self.data[column].dtype == 'datetime64[ns]':
                date_columns.append(column)
        
        date_ranges = {}
        for column in date_columns:
            # Convert to datetime if not already
            if self.data[column].dtype != 'datetime64[ns]':
                try:
                    self.data[column] = pd.to_datetime(self.data[column])
                except:
                    print(f"Could not convert {column} to datetime.")
                    continue
            
            min_date = self.data[column].min()
            max_date = self.data[column].max()
            date_range = max_date - min_date
            
            print(f"\n{column}:")
            print(f"- Earliest date: {min_date.strftime('%Y-%m-%d')}")
            print(f"- Latest date: {max_date.strftime('%Y-%m-%d')}")
            print(f"- Date range: {date_range.days} days")
            
            date_ranges[column] = {
                'min_date': min_date,
                'max_date': max_date,
                'range_days': date_range.days
            }
        
        # Store results
        self.validation_results['date_ranges'] = date_ranges
        
        return date_ranges
    
    def check_for_outliers(self):
        """Check for outliers in numerical columns using IQR method."""
        print("\n=== Outliers Check ===")
        
        # Identify numerical columns
        numerical_columns = self.data.select_dtypes(include=['number']).columns
        
        outliers_summary = {}
        
        for column in numerical_columns:
            # Calculate IQR
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outlier boundaries
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Find outliers
            outliers = self.data[(self.data[column] < lower_bound) | (self.data[column] > upper_bound)]
            outlier_count = len(outliers)
            
            # Store results
            outliers_summary[column] = {
                'outlier_count': outlier_count,
                'percentage': outlier_count / len(self.data) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
            
            # Print results
            if column in ['Sales', 'Price']:
                print(f"\n{column}:")
                print(f"- Outlier boundaries: ${lower_bound:.2f} to ${upper_bound:.2f}")
                print(f"- Outliers found: {outlier_count} ({outlier_count/len(self.data)*100:.1f}%)")
            else:
                print(f"\n{column}:")
                print(f"- Outlier boundaries: {lower_bound:.2f} to {upper_bound:.2f}")
                print(f"- Outliers found: {outlier_count} ({outlier_count/len(self.data)*100:.1f}%)")
        
        # Store results
        self.validation_results['outliers'] = outliers_summary
        
        return outliers_summary
    
    def run_all_validations(self):
        """Run all validation checks."""
        self.check_null_values()
        self.check_duplicates()
        self.check_data_types()
        self.check_value_ranges()
        self.check_categorical_values()
        self.check_date_range()
        self.check_for_outliers()
        
        return self.validation_results


class DataProcessor:
    """Class for processing and cleaning data."""
    
    def __init__(self, data):
        """Initialize with the data to process."""
        self.data = data.copy()
        self.processing_log = []
    
    def handle_missing_values(self, strategy='drop'):
        """Handle missing values in the dataset."""
        initial_rows = len(self.data)
        
        if strategy == 'drop':
            # Drop rows with any missing values
            self.data.dropna(inplace=True)
            dropped_rows = initial_rows - len(self.data)
            
            log_message = f"Dropped {dropped_rows} rows with missing values."
            print(log_message)
            self.processing_log.append(log_message)
        
        elif strategy == 'fill_mean':
            # Fill missing values with column mean (for numeric columns only)
            numeric_columns = self.data.select_dtypes(include=['number']).columns
            for column in numeric_columns:
                if self.data[column].isnull().sum() > 0:
                    mean_value = self.data[column].mean()
                    self.data[column].fillna(mean_value, inplace=True)
                    
                    log_message = f"Filled missing values in {column} with mean: {mean_value:.2f}"
                    print(log_message)
                    self.processing_log.append(log_message)
        
        elif strategy == 'fill_median':
            # Fill missing values with column median (for numeric columns only)
            numeric_columns = self.data.select_dtypes(include=['number']).columns
            for column in numeric_columns:
                if self.data[column].isnull().sum() > 0:
                    median_value = self.data[column].median()
                    self.data[column].fillna(median_value, inplace=True)
                    
                    log_message = f"Filled missing values in {column} with median: {median_value:.2f}"
                    print(log_message)
                    self.processing_log.append(log_message)
        
        return self.data
    
    def remove_duplicates(self):
        """Remove duplicate records from the dataset."""
        initial_rows = len(self.data)
        
        # Drop duplicate rows
        self.data.drop_duplicates(inplace=True)
        
        dropped_rows = initial_rows - len(self.data)
        log_message = f"Removed {dropped_rows} duplicate rows."
        print(log_message)
        self.processing_log.append(log_message)
        
        return self.data
    
    def handle_outliers(self, method='clip', columns=None):
        """Handle outliers in numerical columns."""
        if columns is None:
            # Use all numeric columns
            columns = self.data.select_dtypes(include=['number']).columns
        
        for column in columns:
            # Calculate IQR
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outlier boundaries
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            if method == 'clip':
                # Clip values outside the boundaries
                original_min = self.data[column].min()
                original_max = self.data[column].max()
                
                self.data[column] = self.data[column].clip(lower=lower_bound, upper=upper_bound)
                
                log_message = f"Clipped outliers in {column}: range changed from [{original_min:.2f}, {original_max:.2f}] to [{lower_bound:.2f}, {upper_bound:.2f}]"
                print(log_message)
                self.processing_log.append(log_message)
            
            elif method == 'remove':
                # Remove rows with outliers
                initial_rows = len(self.data)
                self.data = self.data[(self.data[column] >= lower_bound) & (self.data[column] <= upper_bound)]
                
                removed_rows = initial_rows - len(self.data)
                log_message = f"Removed {removed_rows} rows with outliers in {column}."
                print(log_message)
                self.processing_log.append(log_message)
        
        return self.data
    
    def convert_data_types(self, type_conversions):
        """Convert columns to specified data types."""
        for column, dtype in type_conversions.items():
            if column in self.data.columns:
                try:
                    self.data[column] = self.data[column].astype(dtype)
                    log_message = f"Converted {column} to {dtype}"
                    print(log_message)
                    self.processing_log.append(log_message)
                except Exception as e:
                    log_message = f"Error converting {column} to {dtype}: {e}"
                    print(log_message)
                    self.processing_log.append(log_message)
        
        return self.data
    
    def get_processing_log(self):
        """Get the processing log."""
        return self.processing_log


class StatisticsCalculator:
    """Class for calculating statistics on data."""
    
    def __init__(self, data):
        """Initialize with the data to analyze."""
        self.data = data
        self.stats = {}
    
    def calculate_basic_stats(self, columns=None):
        """Calculate basic statistics for numerical columns."""
        if columns is None:
            # Use all numeric columns
            columns = self.data.select_dtypes(include=['number']).columns
        
        print("\n=== Basic Statistics ===")
        
        for column in columns:
            mean = self.data[column].mean()
            median = self.data[column].median()
            std_dev = self.data[column].std()
            variance = self.data[column].var()
            min_val = self.data[column].min()
            max_val = self.data[column].max()
            
            self.stats[column] = {
                'mean': mean,
                'median': median,
                'std_dev': std_dev,
                'variance': variance,
                'min': min_val,
                'max': max_val
            }
            
            print(f"\n{column} Statistics:")
            print(f"- Mean: {mean:.2f}")
            print(f"- Median: {median:.2f}")
            print(f"- Standard Deviation: {std_dev:.2f}")
            print(f"- Variance: {variance:.2f}")
            print(f"- Range: {min_val:.2f} to {max_val:.2f}")
        
        return self.stats
    
    def calculate_correlation(self, columns=None):
        """Calculate correlation between numerical columns."""
        if columns is None:
            # Use all numeric columns
            columns = self.data.select_dtypes(include=['number']).columns
        
        print("\n=== Correlation Analysis ===")
        
        # Calculate correlation matrix
        correlation_matrix = self.data[columns].corr()
        
        print("Correlation Matrix:")
        print(correlation_matrix.round(2))
        
        # Store results
        self.stats['correlation'] = correlation_matrix
        
        return correlation_matrix
    
    def calculate_group_stats(self, group_by, agg_columns=None):
        """Calculate statistics grouped by a categorical column."""
        if agg_columns is None:
            # Use all numeric columns
            agg_columns = self.data.select_dtypes(include=['number']).columns
        
        print(f"\n=== Group Statistics by {group_by} ===")
        
        # Group by the specified column
        grouped_stats = self.data.groupby(group_by)[agg_columns].agg(['mean', 'median', 'std', 'min', 'max'])
        
        print(grouped_stats)
        
        # Store results
        self.stats[f'group_by_{group_by}'] = grouped_stats
        
        return grouped_stats
    
    def get_all_stats(self):
        """Get all calculated statistics."""
        return self.stats


class OutputGenerator:
    """Class for generating output files and visualizations."""
    
    def __init__(self, data, output_dir=None):
        """Initialize with data and output directory."""
        self.data = data
        
        # Set output directory
        if output_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.output_dir = os.path.join(script_dir, "output")
        else:
            self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
    
    def save_to_csv(self, filename, data=None):
        """Save data to a CSV file."""
        if data is None:
            data = self.data
        
        file_path = os.path.join(self.output_dir, filename)
        
        try:
            data.to_csv(file_path, index=False)
            print(f"Data saved to {file_path}")
            return True
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
            return False
    
    def save_stats_to_csv(self, stats, filename):
        """Save statistics to a CSV file."""
        file_path = os.path.join(self.output_dir, filename)
        
        try:
            # Convert stats dictionary to DataFrame
            stats_df = pd.DataFrame()
            
            for column, column_stats in stats.items():
                if isinstance(column_stats, dict):
                    # Skip non-basic stats
                    if column in ['correlation', 'group_by_Category', 'group_by_Region']:
                        continue
                    
                    # Create a row for each statistic
                    for stat_name, stat_value in column_stats.items():
                        stats_df.loc[column, stat_name] = stat_value
            
            # Save to CSV
            stats_df.to_csv(file_path)
            print(f"Statistics saved to {file_path}")
            return True
        except Exception as e:
            print(f"Error saving statistics to CSV: {e}")
            return False
    
    def create_bar_chart(self, x_column, y_column, title, filename):
        """Create a bar chart and save it to a file."""
        plt.figure(figsize=(10, 6))
        plt.bar(self.data[x_column], self.data[y_column], color='skyblue')
        plt.title(title)
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        file_path = os.path.join(self.output_dir, filename)
        plt.savefig(file_path)
        plt.close()
        
        print(f"Bar chart saved to {file_path}")
        return file_path
    
    def create_histogram(self, column, bins=10, title=None, filename=None):
        """Create a histogram and save it to a file."""
        if title is None:
            title = f"Distribution of {column}"
        
        if filename is None:
            filename = f"{column}_histogram.png"
        
        plt.figure(figsize=(10, 6))
        plt.hist(self.data[column], bins=bins, color='skyblue', edgecolor='black')
        plt.title(title)
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        file_path = os.path.join(self.output_dir, filename)
        plt.savefig(file_path)
        plt.close()
        
        print(f"Histogram saved to {file_path}")
        return file_path
    
    def create_pie_chart(self, column, title=None, filename=None):
        """Create a pie chart for a categorical column and save it to a file."""
        if title is None:
            title = f"Distribution of {column}"
        
        if filename is None:
            filename = f"{column}_pie_chart.png"
        
        # Get value counts
        value_counts = self.data[column].value_counts()
        
        plt.figure(figsize=(10, 8))
        plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', 
                shadow=True, startangle=90)
        plt.title(title)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        file_path = os.path.join(self.output_dir, filename)
        plt.savefig(file_path)
        plt.close()
        
        print(f"Pie chart saved to {file_path}")
        return file_path


class DataAnalysisApp:
    """Main class that orchestrates the data analysis process."""
    
    def __init__(self, file_path=None):
        """Initialize the data analysis application."""
        self.file_path = file_path
        self.loader = None
        self.data = None
        self.validator = None
        self.processor = None
        self.stats_calculator = None
        self.output_generator = None
    
    def load_data(self, file_path=None):
        """Load data from a file."""
        if file_path:
            self.file_path = file_path
        
        self.loader = DataLoader(self.file_path)
        self.data = self.loader.load_csv()
        
        return self.data is not None
    
    def validate_data(self):
        """Validate the loaded data."""
        if self.data is None:
            print("No data loaded. Call load_data() first.")
            return None
        
        self.validator = DataValidator(self.data)
        validation_results = self.validator.run_all_validations()
        
        return validation_results
    
    def process_data(self):
        """Process and clean the data."""
        if self.data is None:
            print("No data loaded. Call load_data() first.")
            return None
        
        self.processor = DataProcessor(self.data)
        
        # Handle missing values
        self.processor.handle_missing_values(strategy='fill_mean')
        
        # Remove duplicates
        self.processor.remove_duplicates()
        
        # Handle outliers
        self.processor.handle_outliers(method='clip')
        
        # Update the data
        self.data = self.processor.data
        
        return self.data
    
    def calculate_statistics(self):
        """Calculate statistics on the processed data."""
        if self.data is None:
            print("No data loaded. Call load_data() first.")
            return None
        
        self.stats_calculator = StatisticsCalculator(self.data)
        
        # Calculate basic statistics
        self.stats_calculator.calculate_basic_stats()
        
        # Calculate correlation
        self.stats_calculator.calculate_correlation()
        
        # Calculate group statistics
        if 'Category' in self.data.columns:
            self.stats_calculator.calculate_group_stats('Category')
        
        if 'Region' in self.data.columns:
            self.stats_calculator.calculate_group_stats('Region')
        
        return self.stats_calculator.get_all_stats()
    
    def generate_output(self, output_dir=None):
        """Generate output files and visualizations."""
        if self.data is None:
            print("No data loaded. Call load_data() first.")
            return False
        
        self.output_generator = OutputGenerator(self.data, output_dir)
        
        # Save processed data to CSV
        self.output_generator.save_to_csv("processed_data.csv")
        
        # Save statistics to CSV
        if self.stats_calculator:
            self.output_generator.save_stats_to_csv(
                self.stats_calculator.get_all_stats(),
                "statistics.csv"
            )
        
        # Create visualizations
        if 'Category' in self.data.columns and 'Sales' in self.data.columns:
            # Group by Category and sum Sales
            category_sales = self.data.groupby('Category')['Sales'].sum().reset_index()
            self.output_generator.create_bar_chart(
                'Category', 'Sales',
                'Sales by Category',
                'category_sales_bar.png'
            )
        
        if 'Region' in self.data.columns and 'Sales' in self.data.columns:
            # Group by Region and sum Sales
            region_sales = self.data.groupby('Region')['Sales'].sum().reset_index()
            self.output_generator.create_bar_chart(
                'Region', 'Sales',
                'Sales by Region',
                'region_sales_bar.png'
            )
        
        # Create histograms for numerical columns
        for column in self.data.select_dtypes(include=['number']).columns:
            self.output_generator.create_histogram(column)
        
        # Create pie charts for categorical columns
        for column in self.data.select_dtypes(include=['object']).columns:
            if self.data[column].nunique() < 10:  # Only for columns with few unique values
                self.output_generator.create_pie_chart(column)
        
        return True
    
    def run_full_analysis(self):
        """Run the complete data analysis process."""
        print("=== Starting Data Analysis ===")
        
        # Load data
        if self.load_data():
            print("\nData loaded successfully.")
        else:
            print("\nFailed to load data. Exiting.")
            return False
        
        # Validate data
        print("\n--- Data Validation ---")
        self.validate_data()
        
        # Process data
        print("\n--- Data Processing ---")
        self.process_data()
        
        # Calculate statistics
        print("\n--- Statistical Analysis ---")
        self.calculate_statistics()
        
        # Generate output
        print("\n--- Output Generation ---")
        self.generate_output()
        
        print("\n=== Data Analysis Complete ===")
        return True


# Example usage
if __name__ == "__main__":
    # Get the path to the sales data CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "sales_data.csv")
    
    # Create output directory
    output_dir = os.path.join(script_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create and run the data analysis app
    app = DataAnalysisApp(csv_path)
    app.run_full_analysis()
