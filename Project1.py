import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# st.title("Nassau Candy Distributor")
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

st.set_page_config(
    page_title="Project Candy Data Science",
    page_icon="🍭",
    layout = "wide"
)

# Read CSV
df = pd.read_csv("Nassau_Candy_Distributor.csv")

# Group by product line (Division)
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
    summary["Gross_Profit"] / summary["Sales"]
) * 100

# Find product line with highest gross margin
top_division = summary.loc[
    summary["Gross Margin %"].idxmax(),
    "Division"
]



# Find highest gross margin
top_margin = summary["Gross Margin %"].max()


st.markdown("""
<style>

.metric-card {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# Total orders layout 
total_orders = df["Order ID"].nunique()
col1, col2, col3, col4, col5 = st.columns(5)

# Adding color and style to col.metrics. ......... 
st.markdown("""
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
""", unsafe_allow_html=True)

col1.metric(
    "Total Orders",
    f"{df['Order ID'].nunique():,}"
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


# First Problem gross margin as per  product 

# -----------------------------------
# Gross Margin by ALL Product Lines
# -----------------------------------

product_margin = (
    df.groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

product_margin["Gross Margin %"] = (
    product_margin["Gross_Profit"] / product_margin["Sales"]
) * 100


# Slider meter ------------top to products 
Course_time= st.slider("Top 1 to 10 Products", min_value= 1, max_value=10, value= 8)

# st.write("Months:", Course_time)


# Top 8 products by Gross Margin %
top_8 = product_margin.sort_values(
    "Gross Margin %",
    ascending=False
).head(Course_time)

# Top eight product list heading 
st.markdown("""
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
            Top 10 Products by Gross Margin %
        </h2>
    </div>
""", unsafe_allow_html=True)




fig = px.bar(
    top_8.sort_values("Gross Margin %"),
    x="Gross Margin %",
    y="Product Name",
    orientation="h",
    text="Gross Margin %",
    title="Top 8 Products – Gross Margin %"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Gross Margin (%)",
    yaxis_title="Product"
)



fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Gross Margin (%)",
    yaxis_title="Product"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="top_8_product_margin"
)




# High sales high profit --------------

profitability = (
    df.groupby("Division")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum")
    )
    .reset_index()
)

# Calculate margin
profitability["Gross Margin (%)"] = (
    profitability["Total_Profit"] /
    profitability["Total_Sales"]
) * 100

# Highest sales division
sales_row = profitability.loc[
    profitability["Total_Sales"].idxmax()
]

# Highest margin division
margin_row = profitability.loc[
    profitability["Gross Margin (%)"].idxmax()
]

# Insight
if sales_row["Gross Margin (%)"] >= profitability["Gross Margin (%)"].mean():
    insight = (
        f"✅ **{sales_row['Division']}** has the highest sales and its "
        f"**{sales_row['Gross Margin (%)']:.1f}% gross margin** is above "
        f"the average division margin. This indicates that high sales are "
        f"also translating into strong profitability."
    )
else:
    insight = (
        f"⚠️ **{sales_row['Division']}** has the highest sales, but its "
        f"**{sales_row['Gross Margin (%)']:.1f}% gross margin** is below "
        f"the average. High sales are therefore not translating into "
        f"equally strong profitability."
    )

st.subheader("💡 Business Insight")
st.success(insight)

# Bubble chart for this business sight 

# Gross Margin %
profitability["Gross Margin (%)"] = (
    profitability["Total_Profit"] /
    profitability["Total_Sales"]
) * 100


# Bubble Chart
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

# Make bubbles attractive
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
    margin=dict(l=60, r=30, t=70, b=50)
)

# Display
st.plotly_chart(
    fig_bubble,
    use_container_width=True,
    key="high_sales_profitability"
)

# Top 10 Products by Profit
# -----------------------------------------
product_profit = df.groupby("Product Name", as_index=False).agg(
    Cost=("Cost", "sum"),
    Profit=("Gross Profit", "sum")
)

# Select top 10 by profit
top_10 = (
    product_profit
    .sort_values("Profit", ascending=False)
    .head(10)
)

# st.subheader("💰 Top 10 Products: Cost vs Profit")

fig_products = px.bar(
    top_10,
    x="Product Name",
    y=["Cost", "Profit"],
    barmode="group",
    title="💰 Cost vs Gross Profit for Top 10 Products",
    
    # Beautiful custom colors
    color_discrete_map={
        "Cost": "#B981C0",       # Red/Pink
        "Profit": "#EBEBEB"      # Green
    },
    
    text_auto=".2s"
)

# Improve chart appearance
fig_products.update_layout(
    xaxis_tickangle=-45,
    
    # Chart background
    plot_bgcolor="rgba(245, 247, 250, 1)",
    paper_bgcolor="rgba(255, 255, 255, 1)",
    
    # Title
    title={
        "x": 0.5,
        "xanchor": "center",
        "font": {
            "size": 24,
            "color": "#2C3E50"
        }
    },
    
    # Axis titles
    xaxis_title="Product Name",
    yaxis_title="Amount ($)",
    
    # Legend
    legend_title="Metric",
    
    # Height
    height=600
)

# Add borders and hover information
fig_products.update_traces(
    marker_line_width=1,
    marker_line_color="white",
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Amount: $%{y:,.2f}<extra></extra>"
)

st.plotly_chart(fig_products, use_container_width=True)


# 4rth Problem -------------------- 



# Product-level summary
prod_df = (
    df.groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

# Calculate margin %
prod_df["Gross Margin %"] = (
    prod_df["Gross_Profit"] / prod_df["Sales"] * 100
)

# ------------------------------------------------
# Margin Risk Definition
# ------------------------------------------------

# Products with low actual profit but reasonable margin %
profit_threshold = prod_df["Gross_Profit"].quantile(0.25)
margin_threshold = prod_df["Gross Margin %"].median()

prod_df["Margin Risk"] = "Normal"

prod_df.loc[
    (prod_df["Gross_Profit"] <= profit_threshold) &
    (prod_df["Gross Margin %"] >= margin_threshold),
    "Margin Risk"
] = "Margin Risk"

# ------------------------------------------------
# Streamlit UI
# ------------------------------------------------

st.subheader("⚠️ Products Representing Margin Risk")

st.write(
    "Products with relatively healthy margin percentages "
    "but low actual gross profit are classified as margin risk."
)

# Plot
fig = px.scatter(
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

# Median margin line
fig.add_vline(
    x=margin_threshold,
    line_dash="dash",
    annotation_text="Median Margin"
)

# Low-profit line
fig.add_hline(
    y=profit_threshold,
    line_dash="dash",
    annotation_text="Low Profit Threshold"
)

fig.update_layout(
    height=650,
    title_x=0.5,
    legend_title="Risk Level"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# Show risky products 4rth 
# ------------------------------------------------
# Margin Risk - same as DAX
# -----------------------------
def margin_risk(margin):

    if margin < 0.15:
        return "Critical Risk"

    elif margin < 0.20:
        return "High Risk"

    elif margin < 0.30:
        return "Moderate Risk"

    else:
        return "Low Risk"


prod_df["Margin Risk"] = (
    prod_df["Gross Margin %"]
    .apply(margin_risk)
)


# -----------------------------
# Risk priority
# -----------------------------
risk_order = {
    "Critical Risk": 1,
    "High Risk": 2,
    "Moderate Risk": 3,
    "Low Risk": 4
}

prod_df["Risk Rank"] = (
    prod_df["Margin Risk"]
    .map(risk_order)
)


# -----------------------------
# Top 3 highest-risk products
# -----------------------------
top_3_risk = (
    prod_df
    .sort_values(
        ["Risk Rank", "Gross Margin %"],
        ascending=[True, True]
    )
    .head(3)
)


# -----------------------------
# Streamlit display
# -----------------------------
st.subheader("🚨 Top 3 Margin Risk Products")


st.dataframe(
    top_3_risk[
        [
            "Product Name",
            "Sales",
            "Gross_Profit",
            "Gross Margin %",
            "Margin Risk"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


st.link_button(
    "⭐ Visit My GitHub",
    "https://github.com/sandeepchauhan13",
    icon=":material/code:",
    type="primary"
)

