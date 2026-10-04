import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# KONFIGURASI DASHBOARD
# =========================

st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# CUSTOM STYLE
# =========================

st.markdown("""
<style>

    /* =========================
       BACKGROUND UTAMA
       ========================= */

    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }


    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        background-color: #eef2f7;
        border-right: 1px solid #d9dee7;
    }

    [data-testid="stSidebar"] h1 {
        color: #1e3a5f;
        font-size: 24px;
        font-weight: 700;
    }

    [data-testid="stSidebar"] h3 {
        color: #1e3a5f;
        font-size: 16px;
        font-weight: 600;
    }


    /* =========================
       JUDUL DASHBOARD
       ========================= */

    .dashboard-title {
        font-size: 36px;
        font-weight: 700;
        color: #172033;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        color: #687386;
        font-size: 16px;
        margin-bottom: 25px;
    }


    /* =========================
       KPI CARD
       ========================= */

    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e1e5eb;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        min-height: 105px;
    }

    .kpi-title {
        color: #687386;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #172033;
        font-size: 25px;
        font-weight: 700;
    }


    /* =========================
       JUDUL SECTION
       ========================= */

    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #172033;
        margin-top: 15px;
        margin-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)


# =========================
# LOAD DATA
# =========================

df = pd.read_csv("Data/SuperMarket Analysis.csv")

df["Date"] = pd.to_datetime(df["Date"])


# =========================
# SIDEBAR
# =========================

st.sidebar.title("📊 Sales Dashboard")

st.sidebar.markdown("### 🔎 Filter Data")

# Branch
branch_options = ["Semua"] + sorted(
    df["Branch"].unique().tolist()
)

selected_branch = st.sidebar.selectbox(
    "Branch",
    branch_options
)

# Product Line
product_options = ["Semua"] + sorted(
    df["Product line"].unique().tolist()
)

selected_product = st.sidebar.selectbox(
    "Product Line",
    product_options
)

# Gender
gender_options = ["Semua"] + sorted(
    df["Gender"].unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)
# Date Range
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

st.sidebar.divider()

st.sidebar.info(
    "Gunakan filter di atas untuk melihat perubahan "
    "data penjualan secara interaktif."
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

if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date) &
        (filtered_df["Date"].dt.date <= end_date)
    ]

# =========================
# HEADER
# =========================

st.markdown(
    '<div class="dashboard-title">Supermarket Sales Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive dashboard untuk menganalisis performa penjualan supermarket.'
    '</div>',
    unsafe_allow_html=True
)


# =========================
# KPI
# =========================

total_sales = filtered_df["Sales"].sum()
total_transactions = filtered_df["Invoice ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
average_rating = filtered_df["Rating"].mean()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Total Sales</div>
            <div class="kpi-value">Rp {total_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🧾 Total Transaksi</div>
            <div class="kpi-value">{total_transactions:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Total Quantity</div>
            <div class="kpi-value">{total_quantity:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">⭐ Rata-rata Rating</div>
            <div class="kpi-value">{average_rating:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================
# SALES PRODUCT LINE
# =========================

# =========================
# GRAFIK UTAMA
# =========================

col_left, col_right = st.columns(2)


# =========================
# SALES PRODUCT LINE
# =========================

with col_left:

    st.markdown(
        '<div class="section-title">📦 Sales berdasarkan Product Line</div>',
        unsafe_allow_html=True
    )

    sales_by_product = (
        filtered_df
        .groupby("Product line", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_product = px.bar(
        sales_by_product,
        x="Product line",
        y="Sales",
        text_auto=".2s",
        title="Total Sales per Product Line"
    )

    fig_product.update_layout(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=80),
        xaxis_title="",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True
    )


# =========================
# SALES BRANCH
# =========================

with col_right:

    st.markdown(
        '<div class="section-title">🏢 Sales berdasarkan Branch</div>',
        unsafe_allow_html=True
    )

    sales_by_branch = (
        filtered_df
        .groupby("Branch", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_branch = px.bar(
        sales_by_branch,
        x="Branch",
        y="Sales",
        text_auto=".2s",
        title="Total Sales per Branch"
    )

    fig_branch.update_layout(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis_title="",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_branch,
        use_container_width=True
    )


# =========================
# TREND + PAYMENT
# =========================

col_left, col_right = st.columns(2)


# =========================
# TREN SALES BULANAN
# =========================

with col_left:

    st.markdown(
        '<div class="section-title">📈 Tren Sales Bulanan</div>',
        unsafe_allow_html=True
    )

    monthly_sales = (
        filtered_df
        .groupby(
            filtered_df["Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Date"] = (
        monthly_sales["Date"]
        .astype(str)
    )

    monthly_sales.columns = [
        "Month",
        "Sales"
    ]

    fig_monthly = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Tren Total Sales per Bulan"
    )

    fig_monthly.update_layout(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis_title="",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )


# =========================
# METODE PEMBAYARAN
# =========================

with col_right:

    st.markdown(
        '<div class="section-title">💳 Metode Pembayaran</div>',
        unsafe_allow_html=True
    )

    payment_counts = (
        filtered_df["Payment"]
        .value_counts()
        .reset_index()
    )

    payment_counts.columns = [
        "Payment",
        "Count"
    ]

    fig_payment = px.pie(
        payment_counts,
        names="Payment",
        values="Count",
        hole=0.5,
        title="Distribusi Metode Pembayaran"
    )

    fig_payment.update_layout(
        height=400,
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=40)
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )

# =========================
# SALES INSIGHTS
# =========================
# =========================
# SALES INSIGHTS
# =========================

st.markdown(
    '<div class="section-title">💡 Sales Insights</div>',
    unsafe_allow_html=True
)

# Product line dengan sales tertinggi
top_product = (
    filtered_df
    .groupby("Product line")["Sales"]
    .sum()
    .idxmax()
)

# Branch dengan sales tertinggi
top_branch = (
    filtered_df
    .groupby("Branch")["Sales"]
    .sum()
    .idxmax()
)

# Metode pembayaran terbanyak
top_payment = (
    filtered_df["Payment"]
    .value_counts()
    .idxmax()
)

# Rata-rata rating
avg_rating = filtered_df["Rating"].mean()


insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)


with insight_col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🏆 Product Line Terlaris</div>
            <div class="kpi-value">{top_product}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with insight_col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🏢 Branch Sales Tertinggi</div>
            <div class="kpi-value">{top_branch}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with insight_col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💳 Pembayaran Terbanyak</div>
            <div class="kpi-value">{top_payment}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with insight_col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">⭐ Rata-rata Rating</div>
            <div class="kpi-value">{avg_rating:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# DATA TRANSAKSI
# =========================

st.markdown(
    '<div class="section-title">📋 Data Transaksi</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_df,
    width="stretch",
    height=400
)

