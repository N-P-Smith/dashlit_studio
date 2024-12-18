import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import base64

# Importing the defintions back from definition.py

from definition import plot_total_sales_revenue_by_month, plot_total_sales_by_quarter_with_filter, plot_total_sales_by_year,plot_sales_growth_rate_by_month, plot_aov_by_month, plot_total_orders_by_quarter, plot_avg_discounted_amount, plot_discount_usage_rate
from definition import plot_top_selling_products, plot_combined_product_sales_with_labels, segment_by_spend_level, plot_refund_rate_with_threshold_label, plot_fulfilled_order_rate_all_orders
from definition import segment_by_order_frequency, visualize_customer_distribution_city, plot_customer_retention_rate_as_gauge, plot_sales_by_region
from definition import plot_region_sales_growth, segment_by_location, plot_new_vs_returning_customers, plot_average_daily_and_hourly_sales_last_90_days, plot_top_discounts

###
st.set_page_config(
    page_title= "Sales Data Analyzer",
    page_icon = "📊",
    layout="wide")

url_cities = "https://raw.githubusercontent.com/benR24/dashlit_studio/refs/heads/main/app_files/worldcities.csv"

world_cities = pd.read_csv(url_cities)

url_countries = "https://raw.githubusercontent.com/benR24/dashlit_studio/refs/heads/main/app_files/countries.csv"

world_countries = pd.read_csv(url_countries)

# Defintiion of the Navigation Pages
def main():
    st.title("Welcome to Dashlit Studio! 🔥 ")

    # Add a horizontal separator below the title
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        Dashlit Studio is a **Streamlit-hosted web tool** designed to simplify your first steps into  
        **Data Analysis** and **Business Intelligence**.

        ### What You Can Do:
        - Upload your **sales and customer data** as CSV files.  
        - Gain valuable insights from pre-built, interactive visualizations.  
        """)

    with col2:
        st.markdown("""  
        ### Explore Dashboards:
        - Insights into **sales performance**.  
        - Trends in **customer behavior**.  
        - Analysis of **regional sales**.  

        Dashlit Studio is built on the principles of:
        - **Accessible Data Analysis**  
        - **Open-Source Collaboration**  

        Take your first step in transforming raw data into actionable insights with ease! 🚀  
        """)

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
    st.components.v1.html(adoption_rate_BI, height=500)
    st.markdown("""
    **NOTE:** 
    > Small and medium-sized enterprises (SMEs): Smaller organisations tend to have lower adoption rates, with 22% of organisations with 250 or fewer employees reporting adoption rates below 20%. 

    > These statistics highlight that a significant number of organisations, particularly SMEs, have yet to implement BI tools, potentially missing out on the benefits of data-driven decision making [Source](https://dataprot.net/statistics/business-intelligence-statistics/).
    """)

    st.markdown(
        """
        ## **Bridging the gap between insight and action**

        As new data analysts step into their first roles, they often find themselves in environments with limited or no BI tools. This not only slows down their learning curve, but also impacts the organisation's ability to make informed decisions.

        This dashboard fills the gap by providing a streamlined, accessible platform for analysing and visualising sales data, enabling current analysts and SMEs to experience the power of BI first-hand.

        Now that the stage is set, let's dive into what lies ahead!
        """
    )

    st.markdown("""

        ## ✨ **What’s Next?**

        Explore the dashboard to:
        - 📈 **Analyze sales trends** by product, region, and timeframe.  
        - 🔍 **Understand customer behavior** to optimize services and campaigns.  

        With just a few clicks, transform raw data into actionable insights—no advanced tools required. 🚀

        """)

    st.image("https://y.yarn.co/e2d0eefa-60d4-4f91-a473-4eee8522eb6c_text.gif", caption="When your friend realizes you built a tool that does all the work for you! 😂🚀")

    st.markdown(
        """
        ### **What are you waiting for?**

        Explore the dashboard above to see how **this tool** can transform raw data into actionable insights.  
        **No need for a data scientist— just two csv files, a few clicks and you're ready to go!**

        ---
        """
    )

def documentation_page():
    st.title("Documentation and Instructions")
    st.markdown("""
    ## What it does.

    This dashboard analyzes sales data to provide insights into trends, customer behavior, and revenue growth.

    You can input your **sales and customer data** to get a comprehensive analysis and interactive charts which you can also download.

    ---
    """)
    st.markdown("### What you need.")
    st.markdown(""" In order to get started you need two CSV files containing your sales and customer data.  
    In the documentation below you can find information about the required columns and their data type. 
    """)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Sales Data (CSV)")
        st.markdown("""
        **Columns**:
        - `order_id` (String) - Unique identifier for each order.
        - `order_date` (DateTime) - The date and time when the order was placed.
        - `product_name` (String) - The name of the product sold.
        - `sales_channel` (String) - The channel through which the sale occurred (e.g., online, in-store).
        - `fulfillment_status` (String) - The fulfillment status of the order (e.g., fulfilled, unfulfilled).
        - `total_sales_revenue` (Numeric) - The total revenue generated by the order, including taxes and shipping.
        - `discount_amount` (Numeric) - The total discount applied to the order.
        - `refund_amount` (Numeric) - The total amount refunded for the order.
        - `quantity_sold` (Numeric) - The quantity of products sold in the order.
        - `product_revenue` (Numeric) - Revenue generated from the product(s) in the order.
        - `location` (String) - The city or country(iso2) where the order was placed (e.g., 'London', 'Berlin', 'New York' or 'GB', 'US', 'DE').
        - `discount_code` (String) - The discount code applied to the order (if any).
        """)

    with col2:
        st.markdown("### Customer Data (CSV)")
        st.markdown("""
        **Columns**:
        - `customer_id` (String/Numeric) - Unique identifier for each customer.
        - `email` (String) - Email address of the customer.
        - `total_orders` (Numeric) - Total number of orders placed by the customer.
        - `total_spent` (Numeric) - The total amount spent by the customer.
        - `location` (String) - The city or region where the customer resides.
        - `iso2` (String) - ISO country code for the customer's location.
        - `returning_customer` (String or Boolean) - Indicates whether the customer is a returning customer (`yes` or `no`, 'true' or 'false').
        """)

    ## Add the note below the descriptions of the required columns
    st.markdown("### ⚠️ Important Note")
    st.markdown("""
    > **Note**: If you do not have data for one or more of the required columns, please still include these columns in your CSV file.  
    > Leave the rows empty for those columns if necessary. This ensures the proper functionality of the Sales Data Analyzer.
    """)


    st.markdown("""
    ---
    ## General Instructions

    1. Ensure your data adheres to the required column structure and types as listed above.
    2. Upload the **two CSV files** using the file upload options in the sidebar or interface on the Sales Data Analyzer Page.
    3. Select the type of analysis you want from the drop down menus - sales, product or regional analysis.

    ---
    """)

    st.markdown("""
    ### Example CSV Exports

    You can use **any type of sales and customer data** as long as it adheres to the required structure. Below are examples to help you structure your data for compatibility with the tool.

    #### **Sales Data Example**
    | order_id | order_date          | product_name | sales_channel | fulfillment_status | total_sales_revenue |
    |----------|---------------------|--------------|---------------|--------------------|---------------------|
    | 101      | 2024-01-01 10:00:00 | Product A    | Online        | fulfilled          | 1500                |
    | 102      | 2024-01-02 14:30:00 | Product B    | In-Store      | unfulfilled        | 2000                |

    **Sales Data continued.**            
    | discount_amount | refund_amount | quantity_sold | product_revenue | location  | discount_code |
    |-----------------|---------------|---------------|-----------------|-----------|---------------|
    | 100             | 0             | 2             | 1400            | London    | NEWYEAR2024   |
    | 200             | 0             | 1             | 1800            | Berlin    | WINTERSALE    |
    
    #### **Customer Data Example**
    | customer_id | email              | total_orders | total_spent | location | iso2 | returning_customer |
    |-------------|--------------------|--------------|-------------|----------|------|--------------------|
    | 1           | alice@email.com    | 5            | 5000        | London   | GB   | yes                |
    | 2           | bob@email.com      | 2            | 1200        | Berlin   | DE   | no                 |

    ---
    By ensuring your data follows the structures shown above, you will achieve the most accurate insights and visualizations from the dashboard.
    """)


    st.markdown(""" ### Example CSV Exports
    Below are links to download a sample sales & customer data as CSV file in order to test the tool:
    """)

    # Define URLs for the sample CSV files
    url_sales_sample = "https://raw.githubusercontent.com/benR24/dashlit_studio/refs/heads/main/app_files/sample_sales_data.csv"
    url_customer_sample = "https://raw.githubusercontent.com/benR24/dashlit_studio/refs/heads/main/app_files/sample_customer_data.csv"

    # Fetch the content of the sales sample CSV file from the URL
    sales_sample_response = requests.get(url_sales_sample)
    if sales_sample_response.status_code == 200:
        st.download_button(
            label="Download Sample Sales CSV",
            data=sales_sample_response.content,
            file_name="sample_sales_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("Failed to load Sample Sales CSV. Please try again later.")

    # Fetch the content of the customer sample CSV file from the URL
    customer_sample_response = requests.get(url_customer_sample)
    if customer_sample_response.status_code == 200:
        st.download_button(
            label="Download Sample Customer CSV",
            data=customer_sample_response.content,
            file_name="sample_customer_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("Failed to load Sample Customer CSV. Please try again later.")

    # Title for the section
    # Title for the section
    st.markdown("## 🔑 Key Statistical Methods")
    st.markdown(""" --- 
                """)
    # Define the three columns
    col1, col2, col3 = st.columns(3)

    # First Column: Aggregation and Count Methods
    with col1:
        st.markdown("""
        ### 📊 Aggregation
        **`sum`**  
        Calculate totals such as:  
        - Total revenue (e.g., `product_revenue`)  
        - Total sales  
        - Total orders  
        - Total customers 

        **`count`**  
        Count occurrences such as:  
        - Number of orders  
        - Number of customers  
        - Frequency of discount codes    
        """)

    # Second Column: Binning and Group Operations
    with col2:
        st.markdown("""
        ### 🗂️ Binning & Group Operations
        **`cut`**  
        Categorize numeric data into defined ranges, such as:  
        - Spending levels (e.g., Low, Medium, High)  
        - Order frequency segments (e.g., 1-5 Orders, 5+ Orders)  

        **`groupby`**  
        Group data for aggregation and analysis by:  
        - Time periods (e.g., year, month, quarter)  
        - Categories (e.g., product, region, customer type)  
        """)

    # Third Column: Percentage and Mean Calculations
    with col3:
        st.markdown("""
        ### 📈 Percentage & Mean Calculations
        **`pct_change`**  
        Compute growth rates over time:  
        - Monthly sales growth rates  

        **Custom Ratios**  
        Calculate specific metrics such as:
        """)

        # LaTeX and Plain Text for Custom Ratios

        st.write("""**1. Discount Usage Rate**  
                 ---
                """)
        st.latex(r" \text{Discount Usage Rate} = \frac{\text{Orders with Discounts}}{\text{Total Orders}} \times 100 ")
        st.write("Plain Text: `(Orders with Discounts ÷ Total Orders) * 100`")

        st.write("**2. Refund Rate**")
        st.latex(r" \text{Refund Rate} = \frac{\text{Refunded Orders}}{\text{Total Orders}} \times 100 ")
        st.write("Plain Text: `(Refunded Orders ÷ Total Orders) * 100`")

        st.write("**3. Retention Rate**")
        st.latex(r" \text{Retention Rate} = \frac{\text{Returning Customers}}{\text{Total Customers}} \times 100 ")
        st.write("Plain Text: `(Returning Customers ÷ Total Customers) * 100`")

        st.markdown("""
        ---
        **`mean`**  
        Compute averages like:  
        - Average Order Value (AOV)  
        - Average daily/hourly sales  
        """)



def data_analyzer_page():
    st.title("Data Analyzer")
    st.sidebar.title("Upload Your Data")
    
    #Initialize upload_key for file uploaders (NEW)
    if "upload_key" not in st.session_state:
        st.session_state["upload_key"] = 0

    # Use session_state for persistence
    if "sales_data" not in st.session_state:
        st.session_state.sales_data = None
    if "customer_data" not in st.session_state:
        st.session_state.customer_data = None

    


    # File upload logic with dynamic key (UPDATED)
    uploaded_sales = st.sidebar.file_uploader(
        "Upload Sales Data CSV", type=["csv"], key=f"sales_{st.session_state.upload_key}"
    )
    uploaded_customers = st.sidebar.file_uploader(
        "Upload Customer Data CSV", type=["csv"], key=f"customers_{st.session_state.upload_key}"
    )

    # Save uploaded files into session_state
    if uploaded_sales:
        st.session_state.sales_data = pd.read_csv(uploaded_sales)
    if uploaded_customers:
        st.session_state.customer_data = pd.read_csv(uploaded_customers)

    # Check if session_state has data
    if st.session_state.sales_data is not None and st.session_state.customer_data is not None:
        try:
            # Process data
            st.session_state.sales_data['order_date'] = pd.to_datetime(
                st.session_state.sales_data['order_date'], errors='coerce', utc=True
            )
            st.session_state.sales_data = st.session_state.sales_data.dropna(subset=['order_date'])

            # Display raw data if checkbox is selected
            if st.sidebar.checkbox("Show raw data"):
                st.subheader("Sales Data")
                st.dataframe(st.session_state.sales_data)
                st.subheader("Customer Data")
                st.dataframe(st.session_state.customer_data)

            # Dropdown menu for analysis
            analysis_menu = st.sidebar.selectbox(
                "Choose Analysis",
                ["Sales Analysis", "Product Analysis", "Demographic Analysis"]
            )

            # Helper function to safely plot charts
            def safe_plot(chart_function, *args, **kwargs):
                try:
                    st.plotly_chart(chart_function(*args, **kwargs))
                except Exception as e:
                    st.warning(f"Error generating chart {chart_function.__name__}: {e}")

            # Sales Analysis
            if analysis_menu == "Sales Analysis":
                st.subheader("Sales Analysis")
                safe_plot(plot_total_sales_by_year, st.session_state.sales_data)
                safe_plot(plot_total_sales_revenue_by_month, st.session_state.sales_data)
                safe_plot(plot_total_sales_by_quarter_with_filter, st.session_state.sales_data)
                safe_plot(plot_sales_growth_rate_by_month, st.session_state.sales_data)
                safe_plot(plot_aov_by_month, st.session_state.sales_data)
                safe_plot(plot_total_orders_by_quarter, st.session_state.sales_data)
                safe_plot(plot_avg_discounted_amount, st.session_state.sales_data)
                safe_plot(plot_discount_usage_rate, st.session_state.sales_data)
                safe_plot(plot_top_discounts, st.session_state.sales_data, top_n=10)
                safe_plot(plot_average_daily_and_hourly_sales_last_90_days, st.session_state.sales_data)

            # Product Analysis
            elif analysis_menu == "Product Analysis":
                st.subheader("Product Analysis")
                safe_plot(plot_top_selling_products, st.session_state.sales_data, top_n=10)
                safe_plot(plot_combined_product_sales_with_labels, st.session_state.sales_data, top_n=10)
                safe_plot(segment_by_spend_level, st.session_state.customer_data)
                safe_plot(plot_refund_rate_with_threshold_label, st.session_state.sales_data)
                safe_plot(plot_fulfilled_order_rate_all_orders, st.session_state.sales_data)
                safe_plot(segment_by_order_frequency, st.session_state.customer_data)

            # Regional Analysis
            elif analysis_menu == "Demographic Analysis":
                st.subheader("Demographic Analysis")
                safe_plot(plot_sales_by_region, st.session_state.sales_data)
                safe_plot(plot_region_sales_growth, st.session_state.sales_data)
                safe_plot(segment_by_location, st.session_state.customer_data)
                safe_plot(plot_customer_retention_rate_as_gauge, st.session_state.customer_data)
                safe_plot(visualize_customer_distribution_city, st.session_state.customer_data, world_cities, world_countries)
                safe_plot(plot_new_vs_returning_customers, st.session_state.customer_data)

        except Exception as e:
            st.error(f"An error occurred while processing your data: {e}")
    else:
        st.info("Please upload all datasets (Sales and Customers) to proceed.")

    # SECTION 2: Reset button logic with upload_key reset (NEW)
    # Reset button
    if st.sidebar.button("Clear Files and Reset"):
        st.session_state.clear()  # Clear all session state variables
        st.session_state["upload_key"] = 1  # Re-initialize upload_key
        st.sidebar.success("Uploaded files and session data have been cleared!")
        st.rerun()  # Rerun the app to fully reset
# Defintion About this Project page

def about_this_page():
    st.title("About This Project")

    # About section
    st.markdown("""
    ---
    This project was created as the **final capstone project** at **Spiced Academy** in **December 2024** by **Michael Luu** and **Benedict Reymann**.

    Our goal was to develop a tool for **aspiring data analysts** who find themselves starting in a new company where tools like **Tableau** or **Metabase** are not yet available. 

    The project assumes the presence of **sales & customer data as csv files** as a basis for analysis, and it aims to provide insights and decision-making support using tools accessible to everyone.
    """)

    col1, col2 = st.columns(2)

    with col1: 
        st.markdown("""
        ## 💻 Explore the Code on GitHub  
        ---
        Curious to see how it works under the hood?  
        - View the **full source code** and documentation.  
        - Check out the latest updates and improvements.  

        👉 Visit our [Project Repository](https://github.com/benR24/dashlit_studio/tree/main) to explore the code and features!  

        <div style="text-align: center;">
            <a href="https://github.com/benR24/final_project" target="_blank">
                <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/github-white-icon.png" 
                alt="GitHub" width="60" style="margin: 10px;">
            </a>
            <p>Click the logo to visit our project repository</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        ## 🌍 Open Source Project  
        ---
        This project is proudly **open source** under the [MIT License](https://github.com/benR24/final_project/blob/f1969677e5bfc897170871f07288afae5bad5ca5/LICENSE).

        ##### How You Can Contribute 🚀:
        - **Fork** the repository and add your improvements.  
        - **Raise issues** for bugs or feature requests.  
        - **Submit pull requests** to help enhance the project.  
        - **Create new graphs** by changing or adding functions to the `definition.py` file.  
        - ⚠️ **Be careful** when editing `main_app.py` as it contains the Streamlit code that runs the app.

        Your contributions are welcome and appreciated! 🎉
        """)



    ## Tools Section
    st.markdown("""## Tools and Datasets Overview """)
    st.markdown(""" --- 
                """)

    # Create columns for tools
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg" alt="VS Code" width="130">
            <p>VS Code</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" width="130">
            <p>Python</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://dash.plotly.com/assets/images/plotly_logo_dark.png" alt="Plotly" width="350">
            <p>Plotly</p>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit" width="150">
            <p>Streamlit</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://ai.ls/assets/openai-logos/PNGs/openai-white-lockup.png" alt="OpenAI" width="300">
            <p>OpenAI</p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://cdn.prod.website-files.com/5e8cd99ef9ea7c76500188b4/60782ef6dafd1509c3258abc_kreativbox-shopify-partners-agentur.png" alt="Shopify" width="300">
            <p>Shopify Sales & Customer Data</p>
        </div>
        """, unsafe_allow_html=True)

    ## Project Goals
    st.markdown("""
    ## Project Goals ##
    ---            
    - Develop a beginner-friendly tool for data analysis without requiring costly licenses.
    - Provide insights into sales performance based on simple generic sales data exports, which are available as CSV files.
    - Demonstrate advanced data analytics & dashboarding skills acquired at Spiced Academy.
    """)

    # CV Section
    st.markdown("""
    ## Our CVs & Contact
    ---

    Below, you can find our professional CVs showcasing our skills, experience, and expertise.
    """)

    col1, col2 = st.columns(2)

    import streamlit.components.v1 as components

    # Button styles
    button_style = """
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        color: white;
        background-color: #4CAF50;
        border: none;
        border-radius: 5px;
        text-align: center;
        text-decoration: none;
        cursor: pointer;
        margin-top: 10px;
    """

    # Serve Michael Luu's CV
    with col1:
        st.markdown("### Michael Luu's CV")
        linkedin_url = "https://www.linkedin.com/in/michael-luu-17767235/"
        st.markdown(
            f"""
            <a href="{linkedin_url}" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" width="50" style="margin: 10px;">
            </a>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("**Preview:**")
        components.html(
            f"""
            <iframe src="https://drive.google.com/file/d/1NNo3SIi5w3iskpr-aF-I2Lohp372CJhC/preview" width="100%" height="500" style="border: none;"></iframe>
            """,
            height=550,
        )
        st.markdown(
            f"""
            <a href="https://drive.google.com/file/d/1NNo3SIi5w3iskpr-aF-I2Lohp372CJhC/view?usp=sharing" target="_blank" style="{button_style}">
            Download Michael Luu's CV
            </a>
            """,
            unsafe_allow_html=True,
        )

    # Serve Benedict Reymann's CV
    with col2:
        st.markdown("### Benedict Reymann's CV")
        linkedin_url = "https://www.linkedin.com/in/benedict-reymann-12bb5b117/"
        st.markdown(
            f"""
            <a href="{linkedin_url}" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" width="50" style="margin: 10px;">
            </a>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("**Preview:**")
        components.html(
            f"""
            <iframe src="https://drive.google.com/file/d/1ku8UZchQnvP207PjnVlMCzTKeVe5-q2E/preview" width="100%" height="500" style="border: none;"></iframe>
            """,
            height=550,
        )
        st.markdown(
            f"""
            <a href="https://drive.google.com/file/d/1ku8UZchQnvP207PjnVlMCzTKeVe5-q2E/view?usp=sharing" target="_blank" style="{button_style}">
            Download Benedict Reymann's CV
            </a>
            """,
            unsafe_allow_html=True,
        )
    

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

# Inject custom CSS for background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i.postimg.cc/PJvs5bcM/bitmap2.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)
