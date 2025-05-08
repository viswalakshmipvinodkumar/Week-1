import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

def analyze_product_performance(df):
    """Analyze product performance based on total sales and units sold"""
    print("\n=== Product Performance Analysis ===")
    
    # Group by product
    product_analysis = df.groupby('Product').agg({
        'Total_Sales': 'sum',
        'Units_Sold': 'sum',
        'Unit_Price': 'mean'
    }).reset_index()
    
    # Calculate average sale per unit
    product_analysis['Avg_Sale_Per_Unit'] = product_analysis['Total_Sales'] / product_analysis['Units_Sold']
    
    # Sort by total sales
    product_analysis = product_analysis.sort_values('Total_Sales', ascending=False)
    
    # Format currency columns
    product_analysis['Total_Sales'] = product_analysis['Total_Sales'].apply(lambda x: f"${x:.2f}")
    product_analysis['Unit_Price'] = product_analysis['Unit_Price'].apply(lambda x: f"${x:.2f}")
    product_analysis['Avg_Sale_Per_Unit'] = product_analysis['Avg_Sale_Per_Unit'].apply(lambda x: f"${x:.2f}")
    
    print("\nProduct Performance (Sorted by Total Sales):")
    print(product_analysis.to_string(index=False))
    
    return product_analysis

def analyze_regional_sales(df):
    """Analyze sales performance by region"""
    print("\n=== Regional Sales Analysis ===")
    
    # Group by region
    region_analysis = df.groupby('Region').agg({
        'Total_Sales': 'sum',
        'Units_Sold': 'sum',
        'Product': 'count'
    }).reset_index()
    
    # Rename columns for clarity
    region_analysis = region_analysis.rename(columns={'Product': 'Transaction_Count'})
    
    # Calculate average sale per transaction
    region_analysis['Avg_Sale_Per_Transaction'] = region_analysis['Total_Sales'] / region_analysis['Transaction_Count']
    
    # Sort by total sales
    region_analysis = region_analysis.sort_values('Total_Sales', ascending=False)
    
    # Format currency columns
    region_analysis['Total_Sales'] = region_analysis['Total_Sales'].apply(lambda x: f"${x:.2f}")
    region_analysis['Avg_Sale_Per_Transaction'] = region_analysis['Avg_Sale_Per_Transaction'].apply(lambda x: f"${x:.2f}")
    
    print("\nRegional Sales Performance:")
    print(region_analysis.to_string(index=False))
    
    return region_analysis

def analyze_monthly_trends(df):
    """Analyze monthly sales trends"""
    print("\n=== Monthly Sales Trends ===")
    
    # Extract month and year
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    
    # Group by month
    monthly_analysis = df.groupby('Month').agg({
        'Total_Sales': 'sum',
        'Units_Sold': 'sum',
        'Product': 'count'
    }).reset_index()
    
    # Rename columns for clarity
    monthly_analysis = monthly_analysis.rename(columns={'Product': 'Transaction_Count'})
    
    # Calculate average sale per transaction
    monthly_analysis['Avg_Sale_Per_Transaction'] = monthly_analysis['Total_Sales'] / monthly_analysis['Transaction_Count']
    
    # Format currency columns
    monthly_analysis['Total_Sales'] = monthly_analysis['Total_Sales'].apply(lambda x: f"${x:.2f}")
    monthly_analysis['Avg_Sale_Per_Transaction'] = monthly_analysis['Avg_Sale_Per_Transaction'].apply(lambda x: f"${x:.2f}")
    
    print("\nMonthly Sales Trends:")
    print(monthly_analysis.to_string(index=False))
    
    return monthly_analysis

def identify_top_performers(df):
    """Identify top performing products and regions"""
    print("\n=== Top Performers Analysis ===")
    
    # Top products by sales
    top_products = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False).head(3)
    top_products_formatted = [f"{product}: ${sales:.2f}" for product, sales in top_products.items()]
    
    # Top regions by sales
    top_regions = df.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).head(3)
    top_regions_formatted = [f"{region}: ${sales:.2f}" for region, sales in top_regions.items()]
    
    # Best selling product in each region
    best_by_region = df.groupby(['Region', 'Product'])['Total_Sales'].sum().reset_index()
    best_products = best_by_region.loc[best_by_region.groupby('Region')['Total_Sales'].idxmax()]
    
    print("\nTop 3 Products by Sales:")
    for item in top_products_formatted:
        print(f"- {item}")
    
    print("\nTop 3 Regions by Sales:")
    for item in top_regions_formatted:
        print(f"- {item}")
    
    print("\nBest Selling Product by Region:")
    for _, row in best_products.iterrows():
        print(f"- {row['Region']}: {row['Product']} (${row['Total_Sales']:.2f})")
    
    return top_products, top_regions, best_products

def calculate_basic_statistics(df):
    """Calculate basic statistics for the sales data"""
    print("\n=== Basic Sales Statistics ===")
    
    # Extract numerical columns
    sales = df['Total_Sales']
    units = df['Units_Sold']
    prices = df['Unit_Price']
    
    # Calculate statistics
    stats = {
        'Total Sales': {
            'Mean': np.mean(sales),
            'Median': np.median(sales),
            'Std Dev': np.std(sales),
            'Min': np.min(sales),
            'Max': np.max(sales)
        },
        'Units Sold': {
            'Mean': np.mean(units),
            'Median': np.median(units),
            'Std Dev': np.std(units),
            'Min': np.min(units),
            'Max': np.max(units)
        },
        'Unit Price': {
            'Mean': np.mean(prices),
            'Median': np.median(prices),
            'Std Dev': np.std(prices),
            'Min': np.min(prices),
            'Max': np.max(prices)
        }
    }
    
    # Print statistics
    for category, values in stats.items():
        print(f"\n{category} Statistics:")
        for stat, value in values.items():
            if category in ['Total Sales', 'Unit Price']:
                print(f"- {stat}: ${value:.2f}")
            else:
                print(f"- {stat}: {value:.2f}")
    
    return stats

def main():
    """Main function to run all analyses"""
    print("=== Sales Analysis Functions ===\n")
    
    # Load the data
    df = load_sales_data()
    print(f"Loaded sales data with {len(df)} records")
    
    # Run analyses
    analyze_product_performance(df)
    analyze_regional_sales(df)
    analyze_monthly_trends(df)
    identify_top_performers(df)
    calculate_basic_statistics(df)
    
    print("\n=== Analysis Complete ===")

if __name__ == "__main__":
    main()
