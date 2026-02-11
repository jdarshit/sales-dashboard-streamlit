import pandas as pd
import matplotlib.pyplot as plt
import os

print("Program started")

# current script ka path
script_dir = os.path.dirname(os.path.abspath(__file__))

# csv file ka path
data_path = os.path.join(script_dir, "../data/sales_data.csv")

# data load
data = pd.read_csv(data_path)

# date convert
data['Date'] = pd.to_datetime(data['Date'])

# total sales column
data['Total_Sales'] = data['Quantity'] * data['Price']

print("Data loaded successfully")

# product wise sales
product_sales = data.groupby('Product')['Total_Sales'].sum()

plt.figure(figsize=(8,5))
product_sales.plot(kind='bar')

plt.title("Product-wise Sales")
plt.xlabel("Product")
plt.ylabel("Total Sales")

plt.tight_layout()

# output path
output_path = os.path.join(script_dir, "../output/product_sales.png")
plt.savefig(output_path)

print("Product-wise graph saved")

plt.show(block=True)
print("Program finished")

monthly_sales = data.groupby(data['Date'].dt.to_period('M'))['Total_Sales'].sum()

plt.figure(figsize=(8,5))
monthly_sales.plot()

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")

plt.tight_layout()

output_path = os.path.join(script_dir, "../output/monthly_sales.png")
plt.savefig(output_path)

print("Monthly sales graph saved")

plt.show(block=True)

top_products = product_sales.sort_values(ascending=False).head(5)

plt.figure(figsize=(8,5))
top_products.plot(kind='bar')

plt.title("Top 5 Products by Sales")
plt.xlabel("Product")
plt.ylabel("Total Sales")

plt.tight_layout()

output_path = os.path.join(script_dir, "../output/top_5_products.png")
plt.savefig(output_path)

print("Top 5 products graph saved")

plt.show(block=True)
