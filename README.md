🍬 Nassau Candy Distributor Analytics Dashboard

The Nassau Candy Distributor Analytics Dashboard is an end-to-end data analytics project designed to analyze sales performance, profitability, product margins, and potential margin risks.

The project transforms raw sales data into meaningful business insights using Python, Pandas, Plotly, and Streamlit.

The interactive dashboard helps business users understand where revenue is being generated, how profitable different products and divisions are, and which products may require further management attention.

🎯 Business Objectives

The main objective of this project is to help decision-makers understand whether revenue generation is translating into healthy profitability.

Key Objectives
✅ Analyze overall sales performance
✅ Identify highly profitable products
✅ Compare profitability across product divisions
✅ Analyze Gross Margin %
✅ Identify products with lower margins
✅ Detect potential margin-risk products
✅ Classify products by margin risk level
✅ Highlight products requiring management attention
✅ Build an interactive dashboard for business users
📊 Business Questions

The dashboard addresses important business questions such as:

Which products generate the highest sales?
Which products have the highest gross margins?
Are high-sales products also highly profitable?
How does profitability vary across product divisions?
Which products have relatively healthy margins but low gross profit?
Which products have critical, high, or moderate margin risk?
Which products should management investigate further?
📈 Dashboard Features

The dashboard includes the following analyses:

1. Overall Business Performance

Key performance indicators include:

Total Orders
Highest Margin Product Division
Highest Gross Margin
Total Sales
Total Gross Profit
2. Top Products by Gross Margin

An interactive slider allows users to select the Top 1–10 products based on Gross Margin %.

3. High Sales vs. High Profit Analysis

A bubble chart compares product divisions based on:

Total Sales
Total Gross Profit
Total Units
Gross Margin %

This helps identify divisions that combine strong revenue with strong profitability.

4. Cost vs. Gross Profit

A comparison of Cost vs. Gross Profit for the top 10 products helps identify products that contribute significantly to profitability.

5. Margin Risk Analysis

Products are analyzed based on Gross Margin % and Gross Profit.

Products with relatively healthy margin percentages but lower actual gross profit are highlighted as potential margin-risk products.

6. Top 3 Margin Risk Products

The dashboard identifies the three products with the highest margin-risk priority based on their Gross Margin %.

🗂️ Dataset

The project uses the following dataset:

Nassau_Candy_Distributor.csv

Important fields used in the analysis include:

Division
Sales
Gross Profit
Order ID
Product Name
Units
Cost

The data is cleaned and converted into appropriate numeric formats before analysis.

🛠️ Technologies Used
Python
Pandas – Data cleaning and analysis
Plotly – Interactive data visualization
Streamlit – Interactive dashboard development
GitHub – Version control and project hosting
📁 Project Structure
Nassau-Candy-Project/
│
├── Project1.py
├── Nassau_Candy_Distributor.csv
├── requirements.txt
└── README.md

⚙️ Installation & Setup
1. Clone the repository
git clone <your-github-repository-url>

2. Navigate to the project directory
cd Nassau-Candy-Project

3. Install the required libraries
pip install -r requirements.txt

4. Run the Streamlit application
streamlit run Project1.py


The dashboard will open in your web browser.

📦 Requirements

The project requires:

streamlit
pandas
plotly


These dependencies are also included in requirements.txt.

💡 Key Business Insights

The dashboard is designed to help management identify:

High-revenue product divisions
Products generating strong gross profit
Products with high Gross Margin %
Differences between sales volume and profitability
Products that may require margin investigation
Potential opportunities to improve product-level profitability
🚀 Deployment

The dashboard can be deployed using Streamlit Community Cloud by connecting the GitHub repository and selecting:

Project1.py


as the main application file.

The dataset should remain in the same repository so that the application can load:

pd.read_csv("Nassau_Candy_Distributor.csv")

📌 Future Improvements

Potential future enhancements include:

Add interactive filters for Division and Product
Add date-based sales analysis if date information is available
Add sales trend analysis
Add profit contribution percentage
Add downloadable reports
Add additional KPI cards
Improve margin-risk scoring using both margin and profit contribution
Add management recommendations based on selected products
👤 Author

Sandeep Chauhan

GitHub:
https://github.com/sandeepchauhan13

⭐ If you find this project useful, consider giving the repository a star!