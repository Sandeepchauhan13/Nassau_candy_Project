import streamlit as st
import pandas as pd
import plotly.express as px


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Project Candy Data Science",
    page_icon="🍭",
    layout="wide"
)


# ------------------------------------------------
# TITLE
# ------------------------------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: white;
               background-color: #420C42;
               padding: 15px;
               border-radius: 10px;'>
        🍬 Nassau Candy Distributor 🍭
    </h1>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
try:
    df = pd.read_csv("Nassau_Candy_Distributor.csv")
except FileNotFoundError:
    st.error(
        "Nassau_Candy_Distributor.csv was not found. "
        "Please make sure the CSV file is in the same GitHub repository "
        "as Project1.py."
    )
    st.stop()


# ------------------------------------------------
# CHECK REQUIRED COLUMNS
# ------------------------------------------------
required_columns = [
    "Division",
    "Sales",
    "Gross Profit",
    "Order ID",
    "Product Name",
    "Units",
    "Cost"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Missing columns in CSV file: {', '.join(missing_columns)}"
    )
    st.stop()


# ------------------------------------------------
# BASIC DATA CLEANING
# ------------------------------------------------
numeric_columns = [
    "Sales",
    "Gross Profit",
    "Units",
    "Cost"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(
    subset=[
        "Division",
        "Sales",
        "Gross Profit",
        "Order ID",
        "Product Name"
    ]
)


# ================================================================
# OVERALL DIVISION SUMMARY
# ================================================================

summary = (
    df.groupby("Division")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)


# Calculate Gross Margin %
summary["Gross Margin %"] = (
    summary["Gross_Profit"] /
    summary["Sales"].replace(0, pd.NA)
) * 100


# Find division with highest gross margin
top_division = summary.loc[
    summary["Gross Margin %"].idxmax(),
    "Division"
]

top_margin = summary["Gross Margin %"].max()


# ================================================================
# METRIC CARD STYLING
# ================================================================

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: #E3F2FD;
        border: 2px solid #2196F3;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }

    div[data-testid="stMetricLabel"] {
        color: #1565C0;
        font-size: 16px;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #0D47A1;
        font-size: 30px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ================================================================
# KEY METRICS
# ================================================================

total_orders = df["Order ID"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col2.metric(
    "Highest Margin Product Line",
    top_division
)

col3.metric(
    "Highest Gross Margin",
    f"{top_margin:.2f}%"
)

col4.metric(
    "Total Sales",
    f"${df['Sales'].sum():,.2f}"
)

col5.metric(
    "Total Gross Profit",
    f"${df['Gross Profit'].sum():,.2f}"
)


# ================================================================
# TOP PRODUCTS BY GROSS MARGIN
# ================================================================

product_margin = (
    df.groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

product_margin["Gross Margin %"] = (
    product_margin["Gross_Profit"] /
    product_margin["Sales"].replace(0, pd.NA)
) * 100


# Slider
course_time = st.slider(
    "Top 1 to 10 Products",
    min_value=1,
    max_value=10,
    value=8
)


top_products = (
    product_margin
    .sort_values("Gross Margin %", ascending=False)
    .head(course_time)
)


st.markdown(
    """
    <div style="
        text-align: center;
        padding: 12px;
        margin-bottom: 20px;
        border-radius: 10px;
        background-color: #f5f5f5;
    ">
        <h2 style="
            margin: 0;
            font-size: 26px;
            font-weight: 700;
        ">
            Top Products by Gross Margin %
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)


fig_margin = px.bar(
    top_products.sort_values("Gross Margin %"),
    x="Gross Margin %",
    y="Product Name",
    orientation="h",
    text="Gross Margin %",
    title=f"Top {course_time} Products – Gross Margin %"
)

fig_margin.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_margin.update_layout(
    xaxis_title="Gross Margin (%)",
    yaxis_title="Product",
    height=500
)

st.plotly_chart(
    fig_margin,
    use_container_width=True,
    key="top_product_margin"
)


# ================================================================
# HIGH SALES / HIGH PROFIT ANALYSIS
# ================================================================

profitability = (
    df.groupby("Division")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum")
    )
    .reset_index()
)


profitability["Gross Margin (%)"] = (
    profitability["Total_Profit"] /
    profitability["Total_Sales"].replace(0, pd.NA)
) * 100


# Highest sales division
sales_row = profitability.loc[
    profitability["Total_Sales"].idxmax()
]


# Highest margin division
margin_row = profitability.loc[
    profitability["Gross Margin (%)"].idxmax()
]


# Average margin
average_margin = profitability["Gross Margin (%)"].mean()


# Business insight
if sales_row["Gross Margin (%)"] >= average_margin:

    insight = (
        f"**{sales_row['Division']}** has the highest sales and its "
        f"**{sales_row['Gross Margin (%)']:.1f}% gross margin** is above "
        f"the average division margin. This indicates that high sales are "
        f"also translating into strong profitability."
    )

else:

    insight = (
        f"**{sales_row['Division']}** has the highest sales, but its "
        f"**{sales_row['Gross Margin (%)']:.1f}% gross margin** is below "
        f"the average. High sales are therefore not translating into "
        f"equally strong profitability."
    )


st.subheader("💡 Business Insight")
st.success(insight)


# ================================================================
# BUBBLE CHART
# ================================================================

fig_bubble = px.scatter(
    profitability,
    x="Total_Sales",
    y="Total_Profit",
    size="Total_Units",
    color="Division",
    hover_name="Division",
    hover_data={
        "Total_Sales": ":,.0f",
        "Total_Profit": ":,.0f",
        "Total_Units": ":,.0f",
        "Gross Margin (%)": ":.1f"
    },
    size_max=55,
    title="💎 High Sales High Profit"
)


fig_bubble.update_traces(
    marker=dict(
        opacity=0.80,
        line=dict(
            width=1,
            color="white"
        )
    )
)


fig_bubble.update_layout(
    height=550,
    xaxis_title="Total Sales ($)",
    yaxis_title="Total Profit ($)",
    legend_title="Product Line",
    margin=dict(
        l=60,
        r=30,
        t=70,
        b=50
    )
)


st.plotly_chart(
    fig_bubble,
    use_container_width=True,
    key="high_sales_profitability"
)


# ================================================================
# TOP 10 PRODUCTS - COST VS PROFIT
# ================================================================

product_profit = (
    df.groupby("Product Name", as_index=False)
    .agg(
        Cost=("Cost", "sum"),
        Profit=("Gross Profit", "sum")
    )
)


top_10 = (
    product_profit
    .sort_values("Profit", ascending=False)
    .head(10)
)


fig_products = px.bar(
    top_10,
    x="Product Name",
    y=["Cost", "Profit"],
    barmode="group",
    title="💰 Cost vs Gross Profit for Top 10 Products",
    color_discrete_map={
        "Cost": "#B981C0",
        "Profit": "#4CAF50"
    },
    text_auto=".2s"
)


fig_products.update_layout(
    xaxis_tickangle=-45,

    plot_bgcolor="rgba(245, 247, 250, 1)",
    paper_bgcolor="rgba(255, 255, 255, 1)",

    title={
        "x": 0.5,
        "xanchor": "center",
        "font": {
            "size": 24,
            "color": "#2C3E50"
        }
    },

    xaxis_title="Product Name",
    yaxis_title="Amount ($)",
    legend_title="Metric",
    height=600
)


fig_products.update_traces(
    marker_line_width=1,
    marker_line_color="white",
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Amount: $%{y:,.2f}<extra></extra>"
)


st.plotly_chart(
    fig_products,
    use_container_width=True,
    key="top_10_cost_profit"
)


# ================================================================
# MARGIN RISK ANALYSIS
# ================================================================

prod_df = (
    df.groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)


prod_df["Gross Margin %"] = (
    prod_df["Gross_Profit"] /
    prod_df["Sales"].replace(0, pd.NA)
) * 100


# ------------------------------------------------
# Margin Risk Definition
# ------------------------------------------------

profit_threshold = prod_df["Gross_Profit"].quantile(0.25)
margin_threshold = prod_df["Gross Margin %"].median()


prod_df["Margin Risk"] = "Normal"


prod_df.loc[
    (prod_df["Gross_Profit"] <= profit_threshold) &
    (prod_df["Gross Margin %"] >= margin_threshold),
    "Margin Risk"
] = "Margin Risk"


# ------------------------------------------------
# Margin Risk Chart
# ------------------------------------------------

st.subheader("⚠️ Products Representing Margin Risk")

st.write(
    "Products with relatively healthy margin percentages "
    "but low actual gross profit are classified as margin risk."
)


fig_risk = px.scatter(
    prod_df,
    x="Gross Margin %",
    y="Gross_Profit",
    size="Sales",
    color="Margin Risk",
    hover_name="Product Name",
    hover_data={
        "Sales": ":,.0f",
        "Gross_Profit": ":,.0f",
        "Gross Margin %": ":.2f"
    },
    title="Margin Risk: High Margin % but Low Gross Profit",
    labels={
        "Gross Margin %": "Gross Margin (%)",
        "Gross_Profit": "Gross Profit"
    },
    size_max=45
)


fig_risk.add_vline(
    x=margin_threshold,
    line_dash="dash",
    annotation_text="Median Margin"
)


fig_risk.add_hline(
    y=profit_threshold,
    line_dash="dash",
    annotation_text="Low Profit Threshold"
)


fig_risk.update_layout(
    height=650,
    title_x=0.5,
    legend_title="Risk Level"
)


st.plotly_chart(
    fig_risk,
    use_container_width=True,
    key="margin_risk_chart"
)


# ================================================================
# TOP 3 HIGHEST-RISK PRODUCTS
# ================================================================

def margin_risk(margin):

    if margin < 15:
        return "Critical Risk"

    elif margin < 20:
        return "High Risk"

    elif margin < 30:
        return "Moderate Risk"

    else:
        return "Low Risk"


prod_df["Margin Risk Level"] = (
    prod_df["Gross Margin %"]
    .apply(margin_risk)
)


# Risk priority
risk_order = {
    "Critical Risk": 1,
    "High Risk": 2,
    "Moderate Risk": 3,
    "Low Risk": 4
}


prod_df["Risk Rank"] = (
    prod_df["Margin Risk Level"]
    .map(risk_order)
)


# Top 3 highest-risk products
top_3_risk = (
    prod_df
    .sort_values(
        ["Risk Rank", "Gross Margin %"],
        ascending=[True, True]
    )
    .head(3)
)


# ------------------------------------------------
# Display Top 3 Risk Products
# ------------------------------------------------

st.subheader("🚨 Top 3 Margin Risk Products")


st.dataframe(
    top_3_risk[
        [
            "Product Name",
            "Sales",
            "Gross_Profit",
            "Gross Margin %",
            "Margin Risk Level"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# ================================================================
# GITHUB BUTTON
# ================================================================

st.link_button(
    "⭐ Visit My GitHub",
    "https://github.com/sandeepchauhan13",
    icon=":material/code:",
    type="primary"
)
