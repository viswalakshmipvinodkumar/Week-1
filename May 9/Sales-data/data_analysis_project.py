"""
Data Analysis Project
 project integrating OOP concepts, data processing, and visualization
 Loads CSV data, processes it using classes, and creates visualizations
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class DataLoader:
    """Class for loading and validating data from CSV files."""
    
    def __init__(self, file_path):
        """Initialize with the file path."""
        self.file_path = file_path
        self.data = None
        
    def load_data(self):
        """Load data from the CSV file."""
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"Successfully loaded data from {self.file_path}")
            print(f"Data shape: {self.data.shape}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def validate_data(self, required_columns=None):
        """Validate that the data contains required columns."""
        if self.data is None:
            print("No data loaded. Call load_data() first.")
            return False
        
        if required_columns:
            missing_columns = [col for col in required_columns if col not in self.data.columns]
            if missing_columns:
                print(f"Error: Missing required columns: {missing_columns}")
                return False
        
        print("Data validation successful.")
        return True
    
    def get_data(self):
        """Return the loaded data."""
        return self.data


class DataProcessor:
    """Class for processing and analyzing data."""
    
    def __init__(self, data):
        """Initialize with the data to process."""
        self.data = data
        self.processed_data = None
    
    def clean_data(self):
        """Clean the data by handling missing values and duplicates."""
        if self.data is None:
            print("No data to clean.")
            return
        
        # Make a copy to avoid modifying the original
        self.processed_data = self.data.copy()
        
        # Handle missing values
        self.processed_data.fillna({
            'Sales': 0,
            'Units': 0,
            'Price': 0
        }, inplace=True)
        
        # Remove duplicates
        initial_rows = len(self.processed_data)
        self.processed_data.drop_duplicates(inplace=True)
        removed_rows = initial_rows - len(self.processed_data)
        
        print(f"Cleaned data: Removed {removed_rows} duplicate rows.")
        
        # Convert date column to datetime
        if 'Date' in self.processed_data.columns:
            self.processed_data['Date'] = pd.to_datetime(self.processed_data['Date'])
            print("Converted 'Date' column to datetime format.")
    
    def aggregate_by_product(self):
        """Aggregate data by product."""
        if self.processed_data is None:
            print("No processed data. Call clean_data() first.")
            return None
        
        if 'Product' in self.processed_data.columns and 'Total_Sales' in self.processed_data.columns:
            product_sales = self.processed_data.groupby('Product')['Total_Sales'].sum().reset_index()
            print("Data aggregated by product.")
            return product_sales
        else:
            print("Required columns 'Product' or 'Total_Sales' not found.")
            return None
    
    def aggregate_by_region(self):
        """Aggregate data by region."""
        if self.processed_data is None:
            print("No processed data. Call clean_data() first.")
            return None
        
        if 'Region' in self.processed_data.columns and 'Total_Sales' in self.processed_data.columns:
            region_sales = self.processed_data.groupby('Region')['Total_Sales'].sum().reset_index()
            print("Data aggregated by region.")
            return region_sales
        else:
            print("Required columns 'Region' or 'Total_Sales' not found.")
            return None
    
    def monthly_sales_trend(self):
        """Calculate monthly sales trend."""
        if self.processed_data is None:
            print("No processed data. Call clean_data() first.")
            return None
        
        if 'Date' in self.processed_data.columns and 'Total_Sales' in self.processed_data.columns:
            # Convert Date to datetime if it's not already
            if self.processed_data['Date'].dtype != 'datetime64[ns]':
                self.processed_data['Date'] = pd.to_datetime(self.processed_data['Date'])
            
            # Extract month from date
            self.processed_data['Month'] = self.processed_data['Date'].dt.strftime('%Y-%m')
            
            # Group by month and sum sales
            monthly_sales = self.processed_data.groupby('Month')['Total_Sales'].sum().reset_index()
            print("Monthly sales trend calculated.")
            return monthly_sales
        else:
            print("Required columns 'Date' or 'Total_Sales' not found.")
            return None
    
    def calculate_statistics(self):
        """Calculate basic statistics for numerical columns."""
        if self.processed_data is None:
            print("No processed data. Call clean_data() first.")
            return None
        
        numerical_columns = self.processed_data.select_dtypes(include=[np.number]).columns
        stats = {}
        
        for col in numerical_columns:
            stats[col] = {
                'mean': self.processed_data[col].mean(),
                'median': self.processed_data[col].median(),
                'std': self.processed_data[col].std(),
                'min': self.processed_data[col].min(),
                'max': self.processed_data[col].max()
            }
        
        print(f"Calculated statistics for {len(numerical_columns)} numerical columns.")
        return stats


class DataVisualizer:
    """Class for creating visualizations from processed data."""
    
    def __init__(self, output_dir=None):
        """Initialize with an optional output directory."""
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
    
    def bar_chart(self, data, x_column, y_column, title, xlabel, ylabel, filename=None):
        """Create a bar chart."""
        plt.figure(figsize=(10, 6))
        plt.bar(data[x_column], data[y_column], color='skyblue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if filename and self.output_dir:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath)
            print(f"Bar chart saved to {filepath}")
        
        plt.show()
    
    def line_chart(self, data, x_column, y_column, title, xlabel, ylabel, filename=None):
        """Create a line chart."""
        plt.figure(figsize=(12, 6))
        plt.plot(data[x_column], data[y_column], marker='o', linestyle='-', color='green')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        if filename and self.output_dir:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath)
            print(f"Line chart saved to {filepath}")
        
        plt.show()
    
    def pie_chart(self, data, labels_column, values_column, title, filename=None):
        """Create a pie chart."""
        plt.figure(figsize=(10, 8))
        plt.pie(data[values_column], labels=data[labels_column], autopct='%1.1f%%', 
                shadow=True, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title(title)
        plt.tight_layout()
        
        if filename and self.output_dir:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath)
            print(f"Pie chart saved to {filepath}")
        
        plt.show()


class SalesAnalysisReport:
    """Class for generating a comprehensive sales analysis report."""
    
    def __init__(self, data_file, output_dir=None):
        """Initialize with data file path and output directory."""
        self.data_file = data_file
        self.output_dir = output_dir
        
        # Create instances of helper classes
        self.loader = DataLoader(data_file)
        self.data = None
        self.processor = None
        self.visualizer = DataVisualizer(output_dir)
    
    def run_analysis(self):
        """Run the complete analysis process."""
        # Load and validate data
        if not self.loader.load_data():
            return False
        
        if not self.loader.validate_data(['Date', 'Product', 'Region', 'Units_Sold', 'Unit_Price', 'Total_Sales']):
            return False
        
        # Get the data and initialize processor
        self.data = self.loader.get_data()
        self.processor = DataProcessor(self.data)
        
        # Clean and process data
        self.processor.clean_data()
        
        # Create output directory for visualizations if needed
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Generate and display visualizations
        self._generate_product_analysis()
        self._generate_region_analysis()
        self._generate_time_series_analysis()
        
        # Calculate and display statistics
        self._display_statistics()
        
        return True
    
    def _generate_product_analysis(self):
        """Generate product-based analysis and visualizations."""
        # Group by Product and sum Total_Sales
        product_sales = self.data.groupby('Product')['Total_Sales'].sum().reset_index()
        
        if product_sales is not None:
            print("\n=== Product Analysis ===")
            print(product_sales)
            
            # Create bar chart
            self.visualizer.bar_chart(
                product_sales, 'Product', 'Total_Sales',
                'Sales by Product', 'Product', 'Total Sales ($)',
                'product_sales_bar.png'
            )
            
            # Create pie chart
            self.visualizer.pie_chart(
                product_sales, 'Product', 'Total_Sales',
                'Sales Distribution by Product',
                'product_sales_pie.png'
            )
    
    def _generate_region_analysis(self):
        """Generate region-based analysis and visualizations."""
        # Group by Region and sum Total_Sales
        region_sales = self.data.groupby('Region')['Total_Sales'].sum().reset_index()
        
        if region_sales is not None:
            print("\n=== Region Analysis ===")
            print(region_sales)
            
            # Create bar chart
            self.visualizer.bar_chart(
                region_sales, 'Region', 'Total_Sales',
                'Sales by Region', 'Region', 'Total Sales ($)',
                'region_sales_bar.png'
            )
            
            # Create pie chart
            self.visualizer.pie_chart(
                region_sales, 'Region', 'Total_Sales',
                'Sales Distribution by Region',
                'region_sales_pie.png'
            )
    
    def _generate_time_series_analysis(self):
        """Generate time-series analysis and visualizations."""
        # Convert Date to datetime if it's not already
        if self.data['Date'].dtype != 'datetime64[ns]':
            self.data['Date'] = pd.to_datetime(self.data['Date'])
        
        # Extract month from date and group by month
        self.data['Month'] = self.data['Date'].dt.strftime('%Y-%m')
        monthly_sales = self.data.groupby('Month')['Total_Sales'].sum().reset_index()
        
        if not monthly_sales.empty:
            print("\n=== Monthly Sales Trend ===")
            print(monthly_sales)
            
            # Create line chart
            self.visualizer.line_chart(
                monthly_sales, 'Month', 'Total_Sales',
                'Monthly Sales Trend', 'Month', 'Total Sales ($)',
                'monthly_sales_trend.png'
            )
    
    def _display_statistics(self):
        """Display statistical analysis of the data."""
        stats = self.processor.calculate_statistics()
        
        if stats:
            print("\n=== Statistical Analysis ===")
            for col, col_stats in stats.items():
                print(f"\n{col} Statistics:")
                for stat_name, stat_value in col_stats.items():
                    print(f"  {stat_name}: {stat_value:.2f}")


# Example usage
if __name__ == "__main__":
    # Get the path to the sales data CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "sales_data.csv")
    
    # Create output directory for visualizations
    output_dir = os.path.join(script_dir, "visualizations")
    
    # Create and run the sales analysis report
    report = SalesAnalysisReport(csv_path, output_dir)
    report.run_analysis()
