import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set the output directory for saving files
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

def create_bar_charts():
    """Create various bar charts from the sales data"""
    print("=== Creating Sales Bar Charts ===\n")
    
    # Load the CSV file
    csv_path = os.path.join(parent_dir, 'sales_data.csv')
    df = pd.read_csv(csv_path)
    
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Add month column for monthly analysis
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    
    # Set the style
    plt.style.use('ggplot')
    
    # 1. Bar chart of total sales by product
    print("Creating bar chart of total sales by product...")
    plt.figure(figsize=(12, 8))
    
    # Group by product and calculate total sales
    product_sales = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
    
    # Create the bar chart
    bars = plt.bar(product_sales.index, product_sales, color='skyblue')
    plt.title('Total Sales by Product', fontsize=16, fontweight='bold')
    plt.xlabel('Product', fontsize=12)
    plt.ylabel('Total Sales ($)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on top of each bar
    for i, v in enumerate(product_sales):
        plt.text(i, v + 5000, f'${v:.0f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'product_sales_bar.png'))
    plt.close()
    
    # 2. Bar chart of total sales by region
    print("Creating bar chart of total sales by region...")
    plt.figure(figsize=(10, 8))
    
    # Group by region and calculate total sales
    region_sales = df.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False)
    
    # Create the bar chart with different colors
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
    bars = plt.bar(region_sales.index, region_sales, color=colors)
    plt.title('Total Sales by Region', fontsize=16, fontweight='bold')
    plt.xlabel('Region', fontsize=12)
    plt.ylabel('Total Sales ($)', fontsize=12)
    
    # Add value labels on top of each bar
    for i, v in enumerate(region_sales):
        plt.text(i, v + 5000, f'${v:.0f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'region_sales_bar.png'))
    plt.close()
    
    # 3. Bar chart of average unit price by product
    print("Creating bar chart of average unit price by product...")
    plt.figure(figsize=(12, 8))
    
    # Group by product and calculate average unit price
    avg_price = df.groupby('Product')['Unit_Price'].mean().sort_values(ascending=False)
    
    # Create the bar chart
    bars = plt.bar(avg_price.index, avg_price, color='lightgreen')
    plt.title('Average Unit Price by Product', fontsize=16, fontweight='bold')
    plt.xlabel('Product', fontsize=12)
    plt.ylabel('Average Unit Price ($)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on top of each bar
    for i, v in enumerate(avg_price):
        plt.text(i, v + 20, f'${v:.2f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'avg_price_bar.png'))
    plt.close()
    
    # 4. Bar chart of units sold by product
    print("Creating bar chart of units sold by product...")
    plt.figure(figsize=(12, 8))
    
    # Group by product and calculate total units sold
    units_sold = df.groupby('Product')['Units_Sold'].sum().sort_values(ascending=False)
    
    # Create the bar chart
    bars = plt.bar(units_sold.index, units_sold, color='#ff9999')
    plt.title('Total Units Sold by Product', fontsize=16, fontweight='bold')
    plt.xlabel('Product', fontsize=12)
    plt.ylabel('Units Sold', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on top of each bar
    for i, v in enumerate(units_sold):
        plt.text(i, v + 10, f'{v}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'units_sold_bar.png'))
    plt.close()
    
    # 5. Grouped bar chart comparing units sold and average price
    print("Creating grouped bar chart comparing units sold and average price...")
    plt.figure(figsize=(14, 8))
    
    # Prepare data
    products = units_sold.index
    units = units_sold.values
    prices = [avg_price[product] for product in products]
    
    # Normalize prices to be on similar scale as units for visualization
    max_units = max(units)
    max_price = max(prices)
    normalized_prices = [price * (max_units / max_price) * 0.5 for price in prices]
    
    # Set up bar positions
    x = np.arange(len(products))
    width = 0.35
    
    # Create the grouped bar chart
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Units sold bars
    bars1 = ax1.bar(x - width/2, units, width, label='Units Sold', color='#66b3ff')
    ax1.set_xlabel('Product', fontsize=12)
    ax1.set_ylabel('Units Sold', fontsize=12, color='#66b3ff')
    ax1.tick_params(axis='y', labelcolor='#66b3ff')
    
    # Add a second y-axis for price
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, prices, width, label='Avg Price ($)', color='#ff9999')
    ax2.set_ylabel('Average Price ($)', fontsize=12, color='#ff9999')
    ax2.tick_params(axis='y', labelcolor='#ff9999')
    
    # Set x-axis labels
    ax1.set_xticks(x)
    ax1.set_xticklabels(products, rotation=45)
    
    # Add title and legend
    plt.title('Units Sold vs Average Price by Product', fontsize=16, fontweight='bold')
    
    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'units_vs_price_bar.png'))
    plt.close()
    
    print(f"\nAll bar charts saved to: {script_dir}")
    print("\n=== Bar Chart Creation Completed ===")

if __name__ == "__main__":
    create_bar_charts()
