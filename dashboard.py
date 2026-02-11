import streamlit as st
import pandas as pd
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Analysis Dashboard")
st.markdown("Professional sales insights with filters & KPIs")

# ---------------- LOAD DATA ----------------
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "data", "sales_data.csv")

data = pd.read_csv(data_path)

data['Date'] = pd.to_datetime(data['Date'])
data['Total_Sales'] = data['Quantity'] * data['Price']

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

start_date = st.sidebar.date_input(
    "Start Date", data['Date'].min()
)

end_date = st.sidebar.date_input(
    "End Date", data['Date'].max()
)

products = data['Product'].unique()

selected_products = st.sidebar.multiselect(
    "Select Products",
    options=products,
    default=products
)

# ---------------- APPLY FILTERS ----------------
filtered_data = data[
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date)) &
    (data['Product'].isin(selected_products))
]

if filtered_data.empty:
    st.warning("⚠️ No data available for selected filters")
    st.stop()

# ---------------- KPI SECTION ----------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

total_sales = filtered_data['Total_Sales'].sum()
total_quantity = filtered_data['Quantity'].sum()
total_orders = filtered_data.shape[0]

col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("📦 Total Quantity", total_quantity)
col3.metric("🧾 Total Orders", total_orders)

# ---------------- SALES TREND ----------------
st.subheader("📈 Sales Trend Over Time")

daily_sales = (
    filtered_data
    .groupby('Date')['Total_Sales']
    .sum()
)

st.line_chart(daily_sales)

# ---------------- PRODUCT WISE SALES ----------------
st.subheader("📊 Product-wise Sales")

product_sales = (
    filtered_data
    .groupby('Product')['Total_Sales']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_sales)

# ---------------- TOP 5 PRODUCTS ----------------
st.subheader("🏆 Top 5 Products")

top_5_products = product_sales.head(5)
st.bar_chart(top_5_products)

# ---------------- DATA TABLE ----------------
st.subheader("📋 Filtered Sales Data")
st.dataframe(filtered_data)

# ---------------- DOWNLOAD BUTTON ----------------
csv = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.subheader("📊 Monthly Sales Growth")

monthly_sales = (
    filtered_data
    .set_index('Date')
    .resample('M')['Total_Sales']
    .sum()
)

monthly_growth = monthly_sales.pct_change() * 100

st.line_chart(monthly_growth)

st.subheader("📉 Sales Trend with Moving Average")

daily_sales_df = daily_sales.reset_index()
daily_sales_df['7_day_MA'] = daily_sales_df['Total_Sales'].rolling(7).mean()

st.line_chart(
    daily_sales_df.set_index('Date')[['Total_Sales', '7_day_MA']]
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sales Trend")
    st.line_chart(daily_sales)

with col2:
    st.subheader("🏆 Top Products")
    st.bar_chart(top_5_products)

st.sidebar.markdown("## 📊 Sales Dashboard")
st.sidebar.markdown("Built with Python & Streamlit")
