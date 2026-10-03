import streamlit as st
import pandas as pd

# =========================
# KONFIGURASI DASHBOARD
# =========================

st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("Data/SuperMarket Analysis.csv")

# Mengubah kolom Date menjadi datetime
df["Date"] = pd.to_datetime(df["Date"])


# =========================
# JUDUL DASHBOARD
# =========================

st.title("📊 Supermarket Sales Dashboard")
st.write(
    "Dashboard interaktif untuk menganalisis data penjualan supermarket."
)


# =========================
# FILTER
# =========================

st.sidebar.header("🔎 Filter Data")

# Filter Branch
branch_options = ["Semua"] + sorted(df["Branch"].unique().tolist())

selected_branch = st.sidebar.selectbox(
    "Branch",
    branch_options
)

# Filter Product Line
product_options = ["Semua"] + sorted(df["Product line"].unique().tolist())

selected_product = st.sidebar.selectbox(
    "Product Line",
    product_options
)

# Filter Gender
gender_options = ["Semua"] + sorted(df["Gender"].unique().tolist())

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)


# =========================
# FILTER DATA
# =========================

filtered_df = df.copy()

if selected_branch != "Semua":
    filtered_df = filtered_df[
        filtered_df["Branch"] == selected_branch
    ]

if selected_product != "Semua":
    filtered_df = filtered_df[
        filtered_df["Product line"] == selected_product
    ]

if selected_gender != "Semua":
    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]


# =========================
# KPI
# =========================

total_sales = filtered_df["Sales"].sum()
total_transactions = filtered_df["Invoice ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
average_rating = filtered_df["Rating"].mean()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"Rp {total_sales:,.2f}"
    )

with col2:
    st.metric(
        "Total Transaksi",
        f"{total_transactions:,}"
    )

with col3:
    st.metric(
        "Total Quantity",
        f"{total_quantity:,}"
    )

with col4:
    st.metric(
        "Rata-rata Rating",
        f"{average_rating:.2f}"
    )


st.divider()


# =========================
# SALES PRODUCT LINE
# =========================

st.subheader("📦 Sales berdasarkan Product Line")

sales_by_product = (
    filtered_df
    .groupby("Product line")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(sales_by_product)


# =========================
# SALES BRANCH
# =========================

st.subheader("🏢 Sales berdasarkan Branch")

sales_by_branch = (
    filtered_df
    .groupby("Branch")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(sales_by_branch)


# =========================
# TREN SALES BULANAN
# =========================

st.subheader("📈 Tren Sales Bulanan")

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Date"].dt.to_period("M"))["Sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)


# =========================
# METODE PEMBAYARAN
# =========================

st.subheader("💳 Metode Pembayaran")

payment_counts = filtered_df["Payment"].value_counts()

st.bar_chart(payment_counts)


# =========================
# DATA
# =========================

st.subheader("📋 Data Transaksi")

st.dataframe(
    filtered_df,
    use_container_width=True
)