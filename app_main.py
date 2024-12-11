import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import base64

# Importing the defintions back from definition.py

from definition import plot_total_sales_revenue_by_month, plot_total_sales_by_quarter_with_filter, plot_total_sales_by_year 
from definition import plot_sales_growth_rate_by_month, plot_aov_by_month, plot_total_orders_by_quarter, plot_avg_discounted_amount, plot_discount_usage_rate
from definition import plot_top_selling_products, plot_combined_product_sales_with_labels, segment_by_spend_level, plot_refund_rate_with_threshold_label, plot_fulfilled_order_rate_all_orders, segment_by_order_frequency
from definition import visualize_customer_distribution_city, plot_customer_retention_rate_as_gauge, plot_customer_retention_rate_as_gauge, plot_sales_by_region
from definition import plot_region_sales_growth, segment_by_location, plot_new_vs_returning_customers, plot_average_daily_and_hourly_sales_last_90_days, plot_top_discounts
#Importing back regions from region.py

from region import region_mapping

###
st.set_page_config(
    page_title= " Test title",
    page_icon = "📊",
    layout="wide")

world_cities = pd.read_csv('/Users/benedictreymann/Desktop/spiced/final_project/data_sets/worldcities.csv')

# Navigation Pages
def main():
    st.title("Sales Data Analysis Dashboard")
    st.write("Welcome to the Sales Data Analysis Dashboard!")
    st.write("Use the navigation options above to explore the app.")


    ### Intro Text
    st.subheader("🚀 Business Intelligence Adoption Rates")

    st.markdown(
        """
        **Why SMEs Need BI Tools More Than Ever**

        Small and Medium Enterprises (SMEs) often face *unique challenges* in their decision-making processes:
        - 📊 **Lack of actionable data insights**.
        - 🕒 **Time-consuming manual analysis**.
        - 💸 **Lost revenue opportunities due to inefficiencies**.

        Did you know? **Only 22%** of SMEs use BI tools, compared to a whopping **80%** for large enterprises!  
        (Imagine a cool infographic or pie chart here!)  
        """
    )
    #### Embed Mermaid chart with styled legend for better readability about adoption rate of BI Tools 
    st.write(
        "The following pie chart illustrates the adoption rates of Business Intelligence (BI) tools in "
        "Small and Medium Enterprises (SMEs) versus Large Enterprises."
    )
    adoption_rate_BI = """
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            theme: 'base',
            themeVariables: {
                fontFamily: 'Arial, sans-serif', /* Optional: Change font family */
                fontSize: '16px',               /* Optional: Adjust font size */
                fontColor: '#ffffff',           /* White font for text and legend */
                pieLegendTextColor: '#ffffff',  /* White font for legend text */
                background: '#1a1a1a'           /* Dark background to match your theme */
            }
        });
    </script>
<div style="display: flex; justify-content: space-around; align-items: center;">
    <!-- SMEs Pie Chart -->
    <div class="mermaid" style="width: 45%;">
        pie
        "SMEs Without BI Tools" : 78
        "SMEs With BI Tools" : 22
    </div>
    <!-- Large Enterprises Pie Chart -->
    <div class="mermaid" style="width: 45%;">
        pie
        "Large Enterprises Without BI Tools" : 20
        "Large Enterprises With BI Tools" : 80
    </div>
</div>
    """
    st.components.v1.html(adoption_rate_BI, height=400)
    st.markdown("""
    **NOTE:** 
    > Small and medium-sized enterprises (SMEs): Smaller organisations tend to have lower adoption rates, with 22% of organisations with 250 or fewer employees reporting adoption rates below 20%. 

    > These statistics highlight that a significant number of organisations, particularly SMEs, have yet to implement BI tools, potentially missing out on the benefits of data-driven decision making [Source](https://dataprot.net/statistics/business-intelligence-statistics/).
    """)

    st.markdown(
        """
        ---
        ## 🛠️ Why Are We Building This Dashboard?

        ### **To bridge the gap for SMEs.**
        SMEs often miss out on the **power of BI tools** due to cost or complexity. 
        Our goal?  
        ✅ Make data **accessible, actionable**, and **beautiful** for everyone.

        ### **To enable smarter decisions.**
        A simple sales analysis dashboard can help you:
        - Understand customer behavior 📈.
        - Optimize products and services 🛒.
        - Plan smarter campaigns 🧠.

        ---
        """
    )

    st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGVyMHJ5bnFzb2s3aXcwbXl2ZGtyZTB6Mmp2cWk4eGlkb2phYnZ1MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eLvUXqCY7w5sqHM8Eo/giphy.webp", caption="Imagine this as a GIF showing how dashboards can simplify data analysis! 🚀")

    st.markdown(
        """
        ### **What's Next?**

        Explore the dashboard below to see how **modern BI tools** can transform raw data into actionable insights.  
        **No need for a data scientist—just a few clicks and you're ready to go!**

        ---
        """
    )

def documentation_page():
    st.title("Documentation and Instrucions")
    st.markdown("""
    # Sales Data Analysis Dashboard

    This dashboard analyzes sales data to provide insights into trends, growth rates, and more.

    You can input any kind of sales data here to get a comprehensive analysis. 

    ---

    ## What You Need

    To get started, you'll need **three CSV exports** with the following structure and columns:

    ### 1. Sales Data
    - **Columns**:
      - `date` (Date) - The date of the order.
      - `product_name` (String) - The product sold.
      - `net_revenue` (Numeric) - The total revenue per order (after discounts etc.).
      - `city` (String) - The name of city where the sale occurred (e.gl 'London', 'Berlin', 'New York').

    ### 2. Customer Data
    - **Columns**:
      - `customer_id` (Numeric/String) - Unique identifier for the customer.
      - `name` (String) - Name of the customer (first & last name).
      - `email` (String) - The email from the Customer.

    ### 3. Product Data
    - **Columns**:
      - `product_id` (Numeric/String) - Unique identifier for the product.
      - `product_name` (String) - Name of the product.
      - `category` (String) - Category of the product (e.g., electronics, clothing).
      - `price` (Numeric) - Price of the product.

    ---

    ## Instructions

    1. Ensure your data adheres to the required column structure and types.
    2. Upload the three CSV files using the file upload options.
    3. Run the analysis to explore trends, insights, and visualizations.

    ---
                
    ### Example CSV Exports

    You can theoretically use **any kind of sales and customer data** as long as you can export them as a CSV file (e.g., Shopify data). The CSV file should follow the structure shown below. This will ensure the column names and data format are compatible with the tool.

    For your convenience, we also provide **sample CSV files** via the download buttons below. These can be used to test the tool or as a reference for structuring your data.                
    #### **Sales Data**
    | date       | sales  | region   | product       |
    |------------|--------|----------|---------------|
    | 2024-01-01 | 1500   | East     | Product A     |
    | 2024-01-02 | 2000   | West     | Product B     |

    #### **Customer Data**
    | customer_id | name       | region   |
    |-------------|------------|----------|
    | 101         | Alice      | East     |
    | 102         | Bob        | West     |

    #### **Product Data**
    | product_id | product_name | category      | price  |
    |------------|--------------|---------------|--------|
    | 1          | Product A    | Electronics   | 500    |
    | 2          | Product B    | Home Goods    | 700    |

    ---

    By ensuring your data looks like the tables above, you will achieve the most accurate insights from the dashboard.
    """)

    st.markdown(""" ### Example CSV Exports
    Below are links to download a sample sales & customer data as CSV file in order to test the tool:
    """)

    # Add the download button here, positioned right after the relevant text
    with open("/Users/michaelluu/Desktop/spiced/a_final_project/data_sets_ex/cleaned Sgaia Shopify data/shopify_sales_data_cleaned.csv", "r") as file:
            st.download_button(
            label="Download Sample Sales CSV",
            data=file,
            file_name="shopify_sales_data_cleaned.csv",
            mime="text/csv"
        )
    with open("/Users/michaelluu/Desktop/spiced/a_final_project/data_sets_ex/cleaned Sgaia Shopify data/shopify_customer_data_cleaned_newben.csv", "r") as file:
            st.download_button(
            label="Download Sample Customer CSV",
            data=file,
            file_name="shopify_sales_data_cleaned.csv",
            mime="text/csv"
        )        

# Data Analyzer Page
def data_analyzer_page():
    st.title("Data Analyzer")
    st.sidebar.title("Upload Your Data")
    global sales_data, customer_data

    # Uploading files
    uploaded_sales = st.sidebar.file_uploader("Upload Sales Data CSV", type=["csv"])
    uploaded_customers = st.sidebar.file_uploader("Upload Customer Data CSV", type=["csv"])

    if uploaded_sales and uploaded_customers:
        try:
            # Read uploaded files
            sales_data = pd.read_csv(uploaded_sales)
            customer_data = pd.read_csv(uploaded_customers)

            # Ensure 'order_date' column exists
            if 'order_date' not in sales_data.columns:
                raise ValueError("The 'order_date' column is missing from the dataset.")

            # Ensure 'order_date' is in datetime format
            sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], errors='coerce', utc=True)

            # Check and drop rows with invalid or missing 'order_date'
            invalid_dates = sales_data[sales_data['order_date'].isnull()]
            if not invalid_dates.empty:
                print(f"Warning: Found {len(invalid_dates)} rows with invalid dates. Dropping these rows.")
                sales_data = sales_data.dropna(subset=['order_date'])

            # Show raw data if checkbox is selected
            if st.sidebar.checkbox("Show raw data"):
                st.subheader("Sales Data")
                st.dataframe(sales_data)
                st.subheader("Customer Data")
                st.dataframe(customer_data)

            # Analysis menu: Group options into multiple dropdowns
            st.sidebar.title("Analysis Menu")
            # Dropdown for Sales Analysis
            sales_analysis = st.sidebar.selectbox(
                "Sales Analysis",
                [
                    "Total Sales by Year",
                    "Total Sales by Month",
                    "Total Sales by Quarter",
                    "Sales Growth by Month",
                    "Average Order Value by Month",
                    "Total Orders by Quarter",
                    "Avg Discounted Amount",
                    "Discount Usage Rate",
                    "Top 10 Used Discounts",
                    "Average daily & Hourly Revenue (Last 90 days)"
                ],
                key="sales_analysis",
            )

            # Dropdown for Product Analysis
            product_analysis = st.sidebar.selectbox(
                "Product Analysis",
                [
                    "Top Selling Products",
                    "Product Impact on Revenue",
                    "Spend by Customer Segmentation",
                    "Refund Rate",
                    "Fulfillment Rate",
                    "Order Frequency"
                ],
                key="product_analysis",
            )

            # Dropdown for Regional Analysis
            regional_analysis = st.sidebar.selectbox(
                "Regional Analysis",
                [
                    "Top 10 Sales by Region (Bar)",
                    "Sales growth by Region (Line)",
                    "Top 10 Locations by Customer",
                    "Customer Retention Rate",
                    "Visualize Customer Distribution City",
                    "New vs returning Customers"
                ],
                key="regional_analysis",
            )

            # Perform analysis based on selected dropdown
            if sales_analysis:
                if sales_analysis == "Total Sales by Year":
                    st.subheader("Total Sales by Year")
                    fig = plot_total_sales_by_year(sales_data)
                    st.plotly_chart(fig)
                elif sales_analysis == "Total Sales by Month":
                    st.subheader("Total Sales by Month")
                    fig = plot_total_sales_revenue_by_month(sales_data)
                    st.plotly_chart(fig)
                elif sales_analysis == "Total Sales by Quarter":
                    st.subheader("Total Sales by Quarter")
                    fig = plot_total_sales_by_quarter_with_filter(sales_data)
                    st.plotly_chart(fig)
                elif sales_analysis == "Sales Growth by Month":
                    st.subheader("Sales Growth by Month")
                    fig = plot_sales_growth_rate_by_month(sales_data)
                    st.plotly_chart(fig)
                elif sales_analysis == "Average Order Value by Month":
                    st.subheader("Average Order Value by Month")
                    fig = plot_aov_by_month(sales_data)
                    st.plotly_chart(fig)
                elif sales_analysis == "Total Orders by Quarter":
                    st.subheader("Total Orders by Quarter")
                    fig = plot_total_orders_by_quarter(sales_data)
                    st.plotly_chart(fig)
                elif sales_analysis == "Avg Discounted Amount":
                    st.subheader("Avg Discounted Amount")
                    fig = plot_avg_discounted_amount(sales_data)
                    st.plotly_chart(fig)
                elif sales_analysis == "Discount Usage Rate":
                    st.subheader("Discount Usage Rate")
                    fig = plot_discount_usage_rate(sales_data)
                    st.plotly_chart(fig)
                elif sales_analysis == "Top 10 Used Discounts":
                    st.subheader("Top 10 Used Discounts")
                    fig = plot_top_discounts(sales_data, top_n=10)
                    st.plotly_chart(fig)
                elif sales_analysis == "Average daily & Hourly Revenue (Last 90 days)":
                    st.subheader("Average daily & Hourly Revenue (Last 90 days)")
                    fig = plot_average_daily_and_hourly_sales_last_90_days(sales_data)
                    st.plotly_chart(fig)

            if product_analysis:
                if product_analysis == "Top Selling Products":
                    st.subheader("Top Selling Products")
                    fig = plot_top_selling_products(sales_data, top_n=10)
                    st.plotly_chart(fig)
                elif product_analysis == "Product Impact on Revenue":
                        st.subheader("Product Impact on Revenue")
                        fig = plot_combined_product_sales_with_labels(sales_data, top_n=10)
                        st.plotly_chart(fig)
                elif product_analysis == "Spend by Customer Segmentation":
                    st.subheader("Spend by Customer Segmentation")
                    fig = segment_by_spend_level(customer_data)
                    st.plotly_chart(fig)
                elif product_analysis == "Refund Rate":
                    st.subheader("Refund Rate")
                    fig = plot_refund_rate_with_threshold_label(sales_data)
                    st.plotly_chart(fig)
                elif product_analysis == "Fulfillment Rate":
                    st.subheader("Fulfillment Rate")
                    fig = plot_fulfilled_order_rate_all_orders(sales_data)
                    st.plotly_chart(fig)
                elif product_analysis == "Order Frequency":
                 st.subheader("Order Frequency")
                 try:
                    fig = segment_by_order_frequency(customer_data)
                    st.plotly_chart(fig)
                 except ValueError as e:
                    st.warning(f"Could not generate the plot: {e}")
    

            if regional_analysis:
                if regional_analysis == "Top 10 Sales by Region (Bar)":
                    st.subheader("Top 10 Sales by Region (Bar)")
                    fig = plot_sales_by_region(sales_data)
                    st.plotly_chart(fig)
                elif regional_analysis == "Sales growth by Region (Line)":
                    st.subheader("Sales growth by Region (Line)")
                    fig = plot_region_sales_growth(sales_data)
                    st.plotly_chart(fig)
                elif regional_analysis == "Top 10 Locations by Customer":
                    st.subheader("Top 10 Locations by Customer")
                    fig = segment_by_location(sales_data)
                    st.plotly_chart(fig)
                elif regional_analysis == "Customer Retention Rate":
                    st.subheader("Customer Retention Rate")
                    fig = plot_customer_retention_rate_as_gauge(customer_data)
                    st.plotly_chart(fig)
                elif regional_analysis == "Visualize Customer Distribution City":
                    st.subheader("Visualize Customer Distribution City")
                    fig = visualize_customer_distribution_city(customer_data, world_cities)
                    if fig:
                        st.plotly_chart(fig)
                elif regional_analysis == "New vs returning Customers":
                    st.subheader("New vs returning Customers")
                    fig = plot_new_vs_returning_customers(customer_data)
                    if fig:
                        st.plotly_chart(fig)
                    else:
                        st.write("No data available to generate the map. Please check your input.")
        except Exception as e:
            st.error(f"An error occurred while processing your data: {e}")
    else:
        st.info("Please upload all three datasets (Sales, Products, Customers) to proceed.")

# Defintion About this Project page

def about_this_page():
    st.title("About This Project")

    # About section
    st.markdown("""
    This project was created as the **final capstone project** at **Spiced Academy** in **December 2024** by **Michael Luu** and **Benedict Reymann**.

    Our goal was to develop a tool for **aspiring data analysts** who find themselves starting in a new company where tools like **Tableau** or **Metabase** are not yet available. 

    The project assumes the presence of **Shopify sales data** as a basis for analysis, and it aims to provide insights and decision-making support using tools accessible to everyone.
    """)

    ## Project Goals
    st.markdown("""
    ## Project Goals ##
    ---            
    - Develop a beginner-friendly tool for data analysis without requiring costly licenses.
    - Provide insights into sales performance based on Shopify data or other generic sales data exports in csv.
    - Demonstrate advanced data analytics skills learned at Spiced Academy.
    """)

    # CV section introduction

    st.markdown("""
    ## Our CVs

    Below, you can find our professional CVs showcasing our skills, experience, and expertise.
    """)
    # Making 2 coloumns 

    col1, col2 = st.columns(2)


    # Serve Michael Luu's CV
    with col1:
        st.markdown("### Michael Luu's CV")
        michael_cv_path = "/Users/benedictreymann/Desktop/spiced/final_project/michael_luu_cv.pdf"
        if os.path.exists(michael_cv_path):
            # Read the file content
            with open(michael_cv_path, "rb") as file:
                file_content = file.read()
                # Base64 encode the file content
                base64_pdf = base64.b64encode(file_content).decode("utf-8")
            
            # Define the LinkedIn URL
            linkedin_url = "https://www.linkedin.com/in/michael-luu-17767235/"

            # Display the LinkedIn logo as a clickable link
            st.markdown(
            f"""
            <a href="{linkedin_url}" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" width="50" style="margin: 10px;">
            </a>
            """,
            unsafe_allow_html=True,
            )



            # Display embedded PDF
            st.markdown(
                f"""
                <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400"></iframe>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error("Michael Luu's CV is not found.")

    # Serve Ben Reymann's CV
    with col2:
        st.markdown("### Benedict Reymann's CV")
        ben_cv_path = "/Users/benedictreymann/Desktop/spiced/final_project/ben_reymann_cv.pdf"
        if os.path.exists(ben_cv_path):
            # Read the file content
            with open(ben_cv_path, "rb") as file:
                file_content = file.read()
                # Base64 encode the file content
                base64_pdf = base64.b64encode(file_content).decode("utf-8")
            

            # Define the LinkedIn URL
            linkedin_url = "https://www.linkedin.com/in/benedict-reymann-12bb5b117/"

            # Display the LinkedIn logo as a clickable link
            st.markdown(
            f"""
            <a href="{linkedin_url}" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" width="50" style="margin: 10px;">
            </a>
            """,
            unsafe_allow_html=True,
            )

            # Display embedded PDF
            st.markdown(
                f"""
                <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400"></iframe>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error("Ben Reymann's CV is not found.")

# Navigation logic
page = st.radio(
    "Navigate to:",
    ["Home", "Documentation", "Data Analyzer", "About this project"],
    index=0,
    horizontal=True
)

# Page routing logic
if page == "Home":
    main()
elif page == "Documentation":
    documentation_page()
elif page == "Data Analyzer":
    data_analyzer_page()
elif page == "About this project":
    about_this_page()
# Page logic
##if page == "Home":
##    main()
##elif page == "Documentation":
##    documentation_page()
##elif page == "Data Analyzer":
##    data_analyzer_page()


# Inject custom CSS for background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i.postimg.cc/W3wkG6Hv/bitmap.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)