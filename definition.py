## This page is to load all definitions into one seperate pyhton file

import pandas as pd
import plotly.express as px
import requests
import plotly.graph_objects as go
import streamlit as st

# Sales Analysis Definitions (Dropdown)

def plot_total_sales_revenue_by_month(sales_data):
    """
    Plots total sales revenue (sum of product revenue) by month with a simple checkbox legend for year selection.
    """

    # Extract year and month
    sales_data['Year'] = sales_data['order_date'].dt.year
    sales_data['Month'] = sales_data['order_date'].dt.month
    sales_data['Month-Year'] = sales_data['order_date'].dt.strftime('%b-%Y')  # e.g., "Jan-2024"

    # Group by year and month, and sum the product revenue
    monthly_sales = sales_data.groupby(['Year', 'Month-Year'], as_index=False)['product_revenue'].sum()

    # Sort data by Year and Month
    monthly_sales['Month-Year-Sort'] = pd.to_datetime(monthly_sales['Month-Year'], format='%b-%Y')
    monthly_sales = monthly_sales.sort_values('Month-Year-Sort')

    # Initialize the figure
    fig = go.Figure()

    # Add traces for each year
    years = monthly_sales['Year'].unique()
    for year in years:
        year_data = monthly_sales[monthly_sales['Year'] == year]
        fig.add_trace(go.Bar(
            x=year_data['Month-Year'],
            y=year_data['product_revenue'],
            name=str(year),  # Each year as a separate trace
            text=year_data['product_revenue'],
            texttemplate='$%{text:.2f}',
            textposition='outside'
        ))

    # Update layout for a simple checkbox-style legend
    fig.update_layout(
        title="Total Sales Revenue by Month",
        xaxis_title="Month-Year",
        yaxis_title="Total Sales Revenue ($)",
        barmode='group',  # Group bars by year
        xaxis=dict(tickangle=-45),  # Rotate x-axis labels for better readability
        legend=dict(
            title="Select Year",
            traceorder="normal",
            orientation="v",
            x=1.02,  # Position to the right
            y=1.0,
            bordercolor="Black",
            borderwidth=1
        ),
        template="plotly_dark",
        height=600,
        width=1000
    )
    st.caption("This graph shows the total sales revenue grouped by month, with comparisons across selected years.")
    return fig

def plot_total_sales_by_quarter_with_filter(sales_data): 
    """
    Plots total sales revenue by quarter with a simple checkbox-style legend for year selection.

    Parameters:
        - sales_data: DataFrame containing sales data with 'order_date' and 'product_revenue'.
    """

    # Extract year and quarter
    sales_data['Year'] = sales_data['order_date'].dt.year
    sales_data['Quarter'] = sales_data['order_date'].dt.to_period('Q').astype(str)

    # Group by year and quarter, and sum the product revenue
    quarterly_sales = sales_data.groupby(['Year', 'Quarter'], as_index=False)['product_revenue'].sum()

    # Sort data by Year and Quarter using Period objects
    quarterly_sales['Quarter-Sort'] = pd.PeriodIndex(quarterly_sales['Quarter'], freq='Q')
    quarterly_sales = quarterly_sales.sort_values(['Quarter-Sort'])

    # Initialize the figure
    fig = go.Figure()

    # Add traces for each year
    years = quarterly_sales['Year'].unique()
    for year in years:
        year_data = quarterly_sales[quarterly_sales['Year'] == year]
        fig.add_trace(go.Bar(
            x=year_data['Quarter'],
            y=year_data['product_revenue'],
            name=str(year),  # Each year as a separate trace
            text=year_data['product_revenue'],
            texttemplate='$%{text:.2f}',
            textposition='outside'
        ))

    # Update layout for a simple checkbox-style legend
    fig.update_layout(
        title="Total Sales Revenue by Quarter",
        xaxis_title="Quarter",
        yaxis_title="Total Sales Revenue ($)",
        barmode='group',  # Group bars by year
        xaxis=dict(tickangle=-45),  # Rotate x-axis labels for better readability
        legend=dict(
            title="Select Year",
            traceorder="normal",
            orientation="v",
            x=1.02,  # Position to the right
            y=1.0,
            bordercolor="Black",
            borderwidth=1
        ),
        template="plotly_dark"
    )
    st.caption("🔍 Total sales revenue grouped by quarters, filtered by selected years.")
    return fig

def plot_total_sales_by_year(sales_data):
    """
    Plots total sales revenue by year using the provided sales data structure.
    Ensures the x-axis only displays full years.
    """
    # Drop rows with invalid or missing dates
    sales_data = sales_data.dropna(subset=['order_date'])

    # Verify if the column is properly converted to datetime
    if not pd.api.types.is_datetime64_any_dtype(sales_data['order_date']):
        raise ValueError(
            "The 'order_date' column is not in datetime format even after conversion. "
            "Ensure all dates are valid and properly formatted in the source data."
        )
    
    # Extract year from the date column
    sales_data['year'] = sales_data['order_date'].dt.year
    
    # Calculate total sales revenue by year
    yearly_sales = sales_data.groupby('year', as_index=False)['product_revenue'].sum()

    # Convert year to string to ensure the x-axis only displays full years
    yearly_sales['year'] = yearly_sales['year'].astype(str)
    
    # Plot the data
    fig = px.bar(
        yearly_sales,
        x='year',
        y='product_revenue',
        title='Total Sales Revenue by Year',
        labels={'year': 'Year', 'product_revenue': 'Total Sales Revenue'},
        text='product_revenue',
        color='year'  # Optional: Assign unique colors by year
    )
    fig.update_traces(texttemplate='%{text:.2f}')
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Year",
        xaxis_type='category',  # Ensure x-axis uses categorical values
        yaxis_title="Total Sales Revenue",
        coloraxis_showscale=False
    )
    st.caption("📊 This chart shows total sales revenue aggregated for each year.")
    return fig

def plot_sales_growth_rate_by_month(sales_data):
    # Extract year and month for grouping
    sales_data['year_month'] = sales_data['order_date'].dt.to_period('M').astype(str)
    
    # Calculate total sales by year and month
    monthly_sales = sales_data.groupby('year_month', as_index=False)['product_revenue'].sum()
    
    # Calculate the percentage change in total_sales_revenue (growth rate)
    monthly_sales['sales_growth_rate'] = monthly_sales['product_revenue'].pct_change() * 100
    
    # Plot the data
    fig = px.line(
        monthly_sales,
        x='year_month',
        y='sales_growth_rate',
        title='Monthly Sales Growth Rate',
        labels={'year_month': 'Year-Month', 'sales_growth_rate': 'Sales Growth Rate (%)'},
        markers=True
    )
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Year-Month",
        yaxis_title="Sales Growth Rate (%)",
        hovermode="x unified"
    )
    st.caption("📈 Monthly growth rate of sales revenue to identify trends over time.")
    return fig

def plot_aov_by_month(sales_data):

    # Extract year and month for grouping
    sales_data['year_month'] = sales_data['order_date'].dt.to_period('M').astype(str)
    
    # Calculate total total_sales_revenue and number of orders by month
    monthly_data = sales_data.groupby('year_month', as_index=False).agg(
        total_sales=('product_revenue', 'sum'),
        num_orders=('product_revenue', 'count')
    )
    
    # Calculate AOV
    monthly_data['aov'] = monthly_data['total_sales'] / monthly_data['num_orders']
    
    # Plot AOV by month
    fig = px.line(
        monthly_data,
        x='year_month',
        y='aov',
        title='Average Order Value (AOV) by Month',
        labels={'year_month': 'Year-Month', 'aov': 'Average Order Value'},
        markers=True
    )
    fig.update_layout(
        template='plotly_white',
        xaxis_title="Year-Month",
        yaxis_title="Average Order Value",
        hovermode="x unified"
    )
    st.caption("💡 Displays the average revenue per order on a monthly basis.")
    return fig
    
def plot_total_orders_by_quarter(sales_data):
    """
    Plots the total number of orders placed by quarter.
    """
    # Drop rows with invalid dates after conversion
    sales_data = sales_data.dropna(subset=['order_date'])
    
    # Extract the year and quarter from the order_date
    sales_data['Year_Quarter'] = sales_data['order_date'].dt.to_period('Q')
    
    # Group by Year_Quarter and count unique orders
    quarterly_orders = sales_data.groupby('Year_Quarter')['order_id'].nunique().reset_index()
    quarterly_orders.columns = ['Quarter', 'Total Orders']
    
    # Sort the data by quarter
    quarterly_orders = quarterly_orders.sort_values(by='Quarter')
    
    # Convert Quarter back to a string for better display
    quarterly_orders['Quarter'] = quarterly_orders['Quarter'].astype(str)
    
    # Create a bar chart
    fig = px.bar(
        quarterly_orders,
        x='Quarter',
        y='Total Orders',
        title='Total Orders by Quarter',
        labels={'Quarter': 'Quarter', 'Total Orders': 'Number of Orders'},
        text='Total Orders'  # Add text labels for the bar values
    )
    
    # Position text labels outside the bars and adjust layout
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="Quarter",
        yaxis_title="Number of Orders"
    )
    st.caption("🛒 Total number of orders grouped by quarters for all years.")
    return fig

def plot_avg_discounted_amount(sales_data):
    """
    Plots the average amount discounted for orders where a discount code was used.
    """
    # Filter for orders where a discount code was used (discount_amount > 0)
    discounted_orders = sales_data[sales_data['discount_amount'] > 0]
    
    # Calculate the average discount amount
    avg_discount = round(discounted_orders['discount_amount'].mean(),2)
    
    # Prepare a DataFrame for visualization
    discount_summary = pd.DataFrame({
        'Category': ['Average Discounted Amount'],
        'Value': [avg_discount]
    })
    
    # Create a bar chart
    fig = px.bar(
        discount_summary,
        x='Category',
        y='Value',
        title='Average Amount Discounted (for orders with discount code)',
        labels={'Value': 'Average Discount', 'Category': ''},
        text='Value'  # Add the average value as a label on the bar
    )
    
    # Position text labels outside the bar
    fig.update_layout(
        yaxis_title="Average Discount ($)",
        height=400,
        width=800
    )
    st.caption("🎟️ Shows the average discount amount for orders with a discount code.")
    return fig

def plot_discount_usage_rate(sales_data):
    """
    Plots the Discount Usage Rate as a gauge chart.
    Formula: (Orders with Discounts / Total Orders) x 100
    """
    # Total orders
    total_orders = sales_data['order_id'].nunique()
    # Orders with discounts (discount_amount > 0)
    discounted_orders = sales_data[sales_data['discount_amount'] > 0]['order_id'].nunique()
    # Calculate discount usage rate
    discount_rate = round((discounted_orders / total_orders) * 100, 2) if total_orders > 0 else 0
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=discount_rate,
        title={'text': "Discount Usage Rate (%)"},
        number={'valueformat': '.2f'},
        gauge={
            'axis': {'range': [0, 100]},  # Gauge range (0 to 100%)
            'bar': {'color': "green"},  # Pastel greenish blue for the needle
            'steps': [
                {'range': [0, 10], 'color': "#FFCCCB"},  # Pastel red
                {'range': [10, 50], 'color': "#FFE4B5"},  # Pastel yellow
                {'range': [50, 100], 'color': "#B2DFDB"}  # Pastel greenish blue
            ],
            'threshold': {
                'line': {'color': "#4682B4", 'width': 4},  # Steel blue for the threshold line
                'thickness': 0.75,
                'value': discount_rate
            }
        }
    ))
    # Add a threshold label
    fig.add_annotation(
        x=0.5,  # Position near the gauge center
        y=-0.1,  # Below the gauge
        text=f"Threshold: {discount_rate:.2f}%",
        showarrow=False,
        font=dict(size=14, color="#4682B4"),  # Match threshold line color
        align="center"
    )
    fig.update_layout(
        title=f"Discount Usage Rate: {discount_rate}%"
    )
    st.caption("🎯 Proportion of orders where a discount code was applied.")
    return fig

def plot_average_daily_and_hourly_sales_last_90_days(sales_data):
    """
    Plots the average sum of product revenue per day of the week and hourly sales trends
    for the last 90 days.

    Parameters:
        - sales_data: DataFrame containing sales data with 'order_date' and 'product_revenue'.
    """
    # Filter data for the last 90 days
    last_90_days = pd.Timestamp.utcnow() - pd.Timedelta(days=90)
    sales_data = sales_data[sales_data['order_date'] >= last_90_days]


    # Extract day of week, hour, and week
    sales_data['day_of_week'] = sales_data['order_date'].dt.day_name()
    sales_data['hour'] = sales_data['order_date'].dt.hour
    sales_data['week'] = sales_data['order_date'].dt.to_period('W')

    # Aggregate by day of the week to calculate the average sum of product revenue
    daily_sales = sales_data.groupby(['day_of_week']).agg({'product_revenue': 'sum'}).reset_index()
    daily_sales['average_revenue'] = daily_sales['product_revenue'] / sales_data['week'].nunique()

    # Ensure correct day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_sales['day_of_week'] = pd.Categorical(daily_sales['day_of_week'], categories=day_order, ordered=True)
    daily_sales = daily_sales.sort_values('day_of_week')

    # Aggregate by hour and week, then calculate the average sum of product revenue per hour
    hourly_sales = sales_data.groupby(['hour', 'week']).agg({'product_revenue': 'sum'}).reset_index()
    hourly_sales = hourly_sales.groupby('hour').agg({'product_revenue': 'mean'}).reset_index()
    hourly_sales.rename(columns={'product_revenue': 'average_revenue'}, inplace=True)

    # Create subplots for daily and hourly sales trends
    fig = go.Figure()

    # Add average daily sales trend
    fig.add_trace(go.Bar(
        x=daily_sales['day_of_week'],
        y=daily_sales['average_revenue'],
        name='Average Daily Sales',
        text=daily_sales['average_revenue'],
        texttemplate='$%{text:.2f}',
        textposition='outside',
        marker_color='lightblue'
    ))

    # Add average hourly sales trend
    fig.add_trace(go.Scatter(
        x=hourly_sales['hour'],
        y=hourly_sales['average_revenue'],
        name='Average Hourly Sales',
        mode='lines+markers',
        line=dict(color='orange', width=3),
        marker=dict(size=8),
        text=hourly_sales['average_revenue'],
        hovertemplate='Hour: %{x}<br>Average Sales: $%{y:.2f}'
    ))

    # Update layout
    fig.update_layout(
        title="Average Daily and Hourly Sales Trends (Last 90 Days)",
        xaxis=dict(title="Day of Week (Daily Sales) / Hour of Day (Hourly Sales)", tickangle=-45),
        yaxis=dict(title="Average Sales ($)"),
        legend=dict(title="Trends", x=1.05, y=1.0),
        template='plotly_dark'
    )
    st.caption("📅 Highlights average daily and hourly sales performance for the last 90 days.")
    return fig

def plot_top_discounts(sales_data, top_n=10):
    """
    Plots the top N most-used discounts based on the number of orders using each discount.

    Parameters:
        - sales_data: DataFrame containing sales data with a 'discount_code' column.
        - top_n: Number of top discounts to display (default is 10).
    """
    # Check if 'discount_code' column exists
    if 'discount_code' not in sales_data.columns:
        raise ValueError("The 'discount_code' column is missing from the dataset.")

    # Filter rows where discounts were used (non-null discount codes)
    discount_data = sales_data[sales_data['discount_code'].notnull()]

    # Normalize the discount codes to lowercase and trim whitespace
    discount_data['discount_code'] = discount_data['discount_code'].str.strip().str.lower()

    # Count the occurrences of each discount code
    discount_usage = discount_data.groupby('discount_code', as_index=False).size()
    discount_usage.rename(columns={'size': 'count'}, inplace=True)

    # Sort by usage count in descending order
    discount_usage = discount_usage.sort_values(by='count', ascending=False)

    # Limit to the top N discounts
    top_discounts = discount_usage.head(top_n)

    # Plot the data
    fig = px.bar(
        top_discounts,
        x='discount_code',
        y='count',
        title=f'Top {top_n} Most-Used Discounts',
        labels={'discount_code': 'Discount Code', 'count': 'Number of Uses'},
        text='count',
        color='discount_code',  # Optional: Assign unique colors by discount code
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(texttemplate='%{text}')
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Discount Code",
        yaxis_title="Number of Uses",
        showlegend=False  # Hide legend since each bar is labeled
    )
    st.caption(f"Description: 🔝 Top {top_n} discount codes used most frequently by customers.")
    return fig

# Order/ Product Analysis Definitions (Dropdown)

def plot_top_selling_products(sales_data,top_n=10):
    # Calculate total revenue for each product in the sales data
    product_revenue = sales_data.groupby('product_name', as_index=False)['product_revenue'].sum()
    
    # Sort by revenue in descending order
    top_products = product_revenue.sort_values(by='product_revenue', ascending=False).head(top_n)
    
    # Plot top-selling products
    fig = px.bar(
        top_products,
        x='product_name',
        y='product_revenue',
        title=f'Top {top_n} Selling Products by Revenue',
        labels={'Product Name': 'product_name', 'Revenue': 'product_revenue'},
        text='product_revenue',
        color='product_name',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=700
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        template='plotly_dark',
        xaxis_title='product_name',
        yaxis_title="Total Revenue",
        xaxis=dict(categoryorder='total descending'),
        showlegend=False
    )
    st.caption(f"🛍️ Top {top_n} products ranked by total sales revenue.")
    return fig

def plot_combined_product_sales_with_labels(sales_data, top_n=10):
    """
    Plots a combined bar graph showing percentage shares of sales volume (order counts)
    and sales revenue for each product, with revenue labels underneath the revenue bars.

    Parameters:
        - sales_data: DataFrame containing sales data with 'product_name' and 'product_revenue'.
        - top_n: Number of top products to include.
    """
    # Calculate total sales volume (order counts) for each product
    product_sales_volume = sales_data.groupby('product_name', as_index=False)['product_revenue'].count()
    product_sales_volume.rename(columns={'product_revenue': 'order_count'}, inplace=True)
    product_sales_volume['percentage_volume'] = (
        product_sales_volume['order_count'] / product_sales_volume['order_count'].sum() * 100
    )
    
    # Calculate total sales revenue for each product
    product_sales_revenue = sales_data.groupby('product_name', as_index=False)['product_revenue'].sum()
    product_sales_revenue['percentage_revenue'] = (
        product_sales_revenue['product_revenue'] / product_sales_revenue['product_revenue'].sum() * 100
    )
    
    # Merge the two metrics into one DataFrame
    combined_data = pd.merge(product_sales_volume, product_sales_revenue, on='product_name')
    
    # Sort by sales revenue (or volume) and limit to top N products
    combined_data = combined_data.sort_values(by='percentage_revenue', ascending=False).head(top_n)
    
    # Prepare data for plotting
    fig = go.Figure()

    # Add bars for "Percentage of Order Counts"
    fig.add_trace(go.Bar(
        x=combined_data['product_name'],
        y=combined_data['percentage_volume'],
        name='Percentage Share per Order',
        text=[f'{val:.2f}%' for val in combined_data['percentage_volume']],
        textposition='outside',
        marker_color='lightskyblue'
    ))

    # Add bars for "Percentage of Revenue"
    fig.add_trace(go.Bar(
    x=combined_data['product_name'],
    y=combined_data['percentage_revenue'],
    name='Percentage of Total Revenue',
    text=[f'{val:.2f}%' for val in combined_data['percentage_revenue']],  # Percentage displayed on hover
    hovertemplate=(
        'Product: %{x}<br>' +
        'Percentage of Revenue: %{y:.2f}%<br>' +
        'Total Revenue: $%{customdata:.2f}'
    ),
    customdata=combined_data['product_revenue'],  # Add revenue as custom data
    textposition='outside',
    marker_color='lightcoral'
))
    
    # Update layout
    fig.update_layout(
        title="Comparison of Product Sales Volume and Revenue (Top Products)",
        xaxis_title="Product",
        yaxis_title="Percentage (%)",
        barmode='group',
        template='plotly_dark',
        xaxis=dict(categoryorder='total descending'),
        height=700
    )
    st.caption("🔄 Comparison of product sales volume and total revenue impact for top products.")
    return fig

def segment_by_spend_level(customer_data):
    """
    Segments customers based on total spending and visualizes the distribution as a bar chart.
    """
    # Calculate dynamic bins
    max_total_spent = customer_data['total_spent'].max()
    min_total_spent = customer_data['total_spent'].min()

    # Define logical base intervals for bins
    bin_intervals = [100, 500, 1000, 1500]  # Base intervals for spending
    if max_total_spent > 1500:
        bin_intervals.append(max_total_spent)  # Add max value as the upper limit

    bins = [min_total_spent] + bin_intervals  # Include the minimum as the starting bin edge
    bins = sorted(set(bins))  # Ensure bins are sorted and unique

    # Generate labels dynamically
    labels = []
    for i in range(len(bins) - 1):
        if i == len(bins) - 2:  # Last bin
            labels.append(f'{bins[i]}+')
        else:
            labels.append(f'{bins[i]}-{bins[i+1]}')

    # Segment customers based on spend levels
    customer_data['spend_level'] = pd.cut(
        customer_data['total_spent'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    # Group and prepare data for visualization
    spend_summary = customer_data.groupby('spend_level').size().reset_index(name='customer_count')

    # Create a bar chart
    fig = px.bar(
        spend_summary, 
        x='spend_level', 
        y='customer_count', 
        title='Customer Spend Level Segmentation',
        labels={'spend_level': 'Spend Level', 'customer_count': 'Customer Count'},
        text='customer_count'  # Add count labels to the bars
    )

    # Position text labels on the bars
    fig.update_layout(
        yaxis_type='log', 
        yaxis_title='Customer Count (Log Scale)'
    )
    st.caption("💰 Groups customers into spending levels.")
    return fig

def plot_refund_rate_with_threshold_label(sales_data):
    """
    Plots the Refund Rate as a gauge chart with a pastel-colored legend and a threshold label.
    Formula: (Refunded Orders / Total Orders) x 100
    """
    # Count total orders
    total_orders = sales_data['order_id'].nunique()
    
    # Count refunded orders (unique `refund_amount` greater than 0)
    refunded_orders = sales_data[sales_data['refund_amount'] > 0]['order_id'].nunique()
    
    # Calculate refund rate
    refund_rate = round((refunded_orders / total_orders) * 100, 2)
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=refund_rate,
        title={'text': "Refund Rate (%)"},
        number={'valueformat': '.2f'},  # 
        gauge={
            'axis': {'range': [0, 100]},  # Gauge range (0 to 100%)
            'bar': {'color': "#FFB6C1"},  # Pastel pink for the needle
            'steps': [
                {'range': [0, 100], 'color': "#B2DFDB"}  # Pastel red
            ],
            'threshold': {
                'line': {'color': "#4682B4", 'width': 4},  # Steel blue for the threshold line
                'thickness': 0.75,
                'value': refund_rate
            }
        }
    ))
    
    # Add a threshold label
    fig.add_annotation(
        x=0.5,  # Position near the gauge center
        y=-0.1,  # Below the gauge
        text=f"Threshold: {refund_rate:.2f}%",
        showarrow=False,
        font=dict(size=14, color="#4682B4"),  # Match threshold line color
        align="center"
    )
    
    fig.update_layout(
        title=f"Refund Rate: {refund_rate}%"
    )
    st.caption("🔄 Percentage of orders refunded based on total orders.")
    return fig

def plot_fulfilled_order_rate_all_orders(sales_data):
    """
    Plots the Fulfilled Order Rate as a gauge chart for all orders.
    Formula: (Fulfilled Orders / Total Orders) x 100
    """
    # Total orders
    total_orders = sales_data['order_id'].nunique()
    
    # Fulfilled orders (fulfillment_status == 'fulfilled')
    fulfilled_orders = sales_data[sales_data['fulfillment_status'].str.lower() == 'fulfilled']['order_id'].nunique()
    
    # Calculate fulfilled order rate
    fulfilled_rate = round((fulfilled_orders / total_orders) * 100, 2) if total_orders > 0 else 0
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=fulfilled_rate,
        title={'text': "Fulfilled Order Rate (%)"},
        number={'valueformat': '.2f'},
        gauge={
            'axis': {'range': [0, 100]},  # Gauge range (0 to 100%)
            'bar': {'color': "green"},  # Pastel greenish blue for the needle
            'steps': [
                {'range': [0, 50], 'color': "#FFCCCB"},  # Pastel red
                {'range': [50, 75], 'color': "#FFE4B5"},  # Pastel yellow
                {'range': [75, 100], 'color': "#B2DFDB"}  # Pastel greenish blue
            ],
            'threshold': {
                'line': {'color': "#4682B4", 'width': 4},  # Steel blue for the threshold line
                'thickness': 0.75,
                'value': fulfilled_rate
            }
        }
    ))
    
    # Add a threshold label
    fig.add_annotation(
        x=0.5,  # Position near the gauge center
        y=-0.1,  # Below the gauge
        text=f"Threshold: {fulfilled_rate:.2f}%",
        showarrow=False,
        font=dict(size=14, color="black"),  # Match threshold line color
        align="center"
    )
    
    fig.update_layout(
        title=f"Fulfilled Order Rate: {fulfilled_rate}%"
    )
    st.caption("✅ Displays the percentage of successfully fulfilled orders.")
    return fig

def segment_by_order_frequency(customer_data):
    """
    Segments customers based on the total number of orders and visualizes the distribution.
    """
    # Calculate dynamic bins
    max_total_orders = customer_data['total_orders'].max()
    min_total_orders = customer_data['total_orders'].min()

    # Define the number of bins or use percentiles for a more dynamic approach
    bin_intervals = [1, 5, 10, 20]  # Logical base intervals
    if max_total_orders > 20:
        bin_intervals.append(max_total_orders)  # Add max value as the upper limit

    bins = [min_total_orders] + bin_intervals  # Include the minimum as the starting bin edge
    bins = sorted(set(bins))  # Ensure bins are sorted and unique

    # Generate labels dynamically
    labels = []
    for i in range(len(bins) - 1):
        if i == len(bins) - 2:  # Last bin
            labels.append(f'{bins[i]}+ Orders')
        else:
            labels.append(f'{bins[i]}-{bins[i+1]} Orders')

    # Bin the data
    customer_data['order_frequency'] = pd.cut(
        customer_data['total_orders'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    # Create the frequency summary
    frequency_summary = customer_data.groupby('order_frequency').size().reset_index(name='customer_count')

    # Plot the results
    fig = px.bar(
        frequency_summary, 
        x='order_frequency', 
        y='customer_count', 
        title='Customer Order Frequency Segmentation', 
        text='customer_count'
    )
    st.caption("🔢 Groups customers by how frequently they place orders.")
    return fig


# Customer/ Regional & Other Analysis Definitions (Dropdown)

def visualize_customer_distribution_city(customer_data, world_cities, world_countries):
    """
    Visualizes customer distribution as a scatter plot on a map using either city or country names in the 'location' column.

    Parameters:
    - customer_data: DataFrame containing customer data with 'location' (city or country) and 'iso2' columns.
    - world_cities: DataFrame with city, country, latitude, longitude, and ISO2 code information for cities.
    - world_countries: DataFrame with country, latitude, longitude, and ISO2 code information for countries.

    Returns:
    - A Plotly scatter map visualization.
    """

    # Normalize location names and ISO2 codes for consistent matching
    customer_data['location'] = customer_data['location'].str.lower()
    customer_data['iso2'] = customer_data['iso2'].str.lower()
    world_cities['city_ascii'] = world_cities['city_ascii'].str.lower()
    world_cities['country'] = world_cities['country'].str.lower()
    world_cities['iso2'] = world_cities['iso2'].str.lower()
    world_countries['country'] = world_countries['country'].str.lower()
    world_countries['iso2'] = world_countries['iso2'].str.lower()

    # Attempt to match as cities first
    city_matches = pd.merge(
        customer_data,
        world_cities,
        left_on=['location', 'iso2'],
        right_on=['city_ascii', 'iso2'],
        how='inner'
    )

    # Calculate match percentage for cities
    city_match_percentage = len(city_matches) / len(customer_data) if len(customer_data) > 0 else 0

    # Set a threshold for city match acceptance (e.g., 50%)
    city_match_threshold = 0.5

    if city_match_percentage >= city_match_threshold:
        # If city matches exceed the threshold, use city matches
        combined_matches = city_matches
        match_type = 'city'
    else:
        # Fallback to country matches
        country_matches = pd.merge(
            customer_data,
            world_countries,
            left_on=['location', 'iso2'],
            right_on=['country', 'iso2'],
            how='inner'
        )

        if len(country_matches) > 0:
            combined_matches = country_matches
            match_type = 'country'
        else:
            print("No matching data found for the provided locations. Please check your input.")
            return

    # Aggregate customer data by location (city or country)
    location_summary = combined_matches.groupby(['location', 'lat', 'lng']).agg(
        total_customers=('customer_id', 'count'),
        total_spent=('total_spent', 'sum')
    ).reset_index()

    if location_summary.empty:
        print("No data to display after aggregation. Please check your input data.")
        return

    # Find the location with the highest total_spent
    max_spent_location = location_summary.loc[location_summary['total_spent'].idxmax()]
    map_center = {
        'lat': max_spent_location['lat'],
        'lon': max_spent_location['lng']
    }

    # Create the scatter map
    fig = px.scatter_mapbox(
        location_summary,
        lat='lat',
        lon='lng',
        size='total_customers',  # Size markers by number of customers
        color='total_spent',  # Color markers by total spending
        hover_name='location',
        hover_data={'total_customers': True, 'total_spent': True},
        mapbox_style='carto-positron',
        title=f'Customer Distribution Map ({match_type.capitalize()} Level)',
        color_continuous_scale=px.colors.sequential.Bluered,
        center=map_center,
        zoom=5  # Adjust zoom level as needed
    )
    st.caption("🌍 Geographic distribution of customers based on city or country.")
    return fig

def plot_customer_retention_rate_as_gauge(customer_data):
    """
    Plots the Customer Retention Rate as a gauge chart.
    Formula: (Repeat Customers / Total Customers) x 100
    """
    # Convert the 'returning_customer' column to numeric (1 for 'Yes', 0 for 'No')
    customer_data['returning_customer_numeric'] = customer_data['returning_customer'].apply(lambda x: 1 if x == 'yes' else 0)
    
    # Calculate total customers and repeat customers
    total_customers = customer_data.shape[0]
    repeat_customers = customer_data['returning_customer_numeric'].sum()
    
    # Calculate retention rate
    retention_rate = round((repeat_customers / total_customers) * 100, 2)
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=retention_rate,
        title={'text': "Customer Retention Rate (%)"},
        gauge={
            'axis': {'range': [0, 100]},  # Gauge range (0 to 100%)
            'bar': {'color': "green"},   # Color of the gauge bar
            'steps': [
                {'range': [0, 50], 'color': "#FFCCCB"},
                {'range': [50, 75], 'color': "#FFE4B5"},
                {'range': [75, 100], 'color': "#B2DFDB"}
            ],
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': retention_rate
            }
        }
    ))
    
    fig.update_layout(
        title=f"Customer Retention Rate: {retention_rate}%",
        height=400
    )
    st.caption("🔄 Proportion of customers who returned for additional purchases.")
    return fig

def plot_new_vs_returning_customers(customer_data):
    """
    Plots the proportion of new vs. returning customers based on the 'returning_customer' column.
    """
    # Normalize 'returning_customer' to 'Returning' or 'New'
    def classify_customer(value):
        if isinstance(value, str):  # Handle string inputs
            return 'Returning' if value.lower() == 'yes' else 'New'
        elif isinstance(value, bool):  # Handle boolean inputs
            return 'Returning' if value else 'New'
        else:  # Handle unexpected cases
            return 'New'  # Default to 'New' if value is None or unrecognized

    customer_data['Customer Type'] = customer_data['returning_customer'].apply(classify_customer)
    
    # Calculate counts for new and returning customers
    customer_summary = customer_data['Customer Type'].value_counts().reset_index()
    customer_summary.columns = ['Customer Type', 'Count']
    
    # Calculate proportions
    total_customers = customer_summary['Count'].sum()
    customer_summary['Proportion'] = customer_summary['Count'] / total_customers
    
    # Create a bar chart
    fig = px.bar(
        customer_summary,
        x='Customer Type',
        y='Count',
        text=customer_summary['Proportion'].apply(lambda x: f'{x:.1%}'),
        title='New vs. Returning Customers',
        labels={'Count': 'Number of Customers', 'Customer Type': 'Customer Type'}
    )
    
    # Position text labels on the bars
    st.caption("👥 Compares the proportion of new customers to returning customers.")
    return fig

def plot_sales_by_region(sales_data, top_n=10):
    """
    Plots total sales revenue by region (city), filtered to the top N cities based on revenue.

    Parameters:
        - sales_data: DataFrame containing sales data with 'location' and 'total_sales_revenue'.
        - top_n: Number of top cities to display (default is 10).
    """
    # Normalize the 'location' column
    sales_data['location'] = sales_data['location'].str.strip().str.lower()

    # Aggregate total sales revenue by location
    location_sales = sales_data.groupby('location', as_index=False)['product_revenue'].sum()

    # Filter for the top N cities by total sales revenue
    top_locations = location_sales.sort_values(by='product_revenue', ascending=False).head(top_n)

    # Plot sales by location with unique colors for each city
    fig = px.bar(
        top_locations,
        x='location',
        y='product_revenue',
        title=f'Top {top_n} Regions by Sales Revenue',
        labels={'location': 'Region', 'product_revenue': 'Total Revenue'},
        text='product_revenue',
        color='location',  # Assign unique colors to each city
        color_discrete_sequence=px.colors.qualitative.Set3  # Use a predefined color palette
    )
    fig.update_traces(texttemplate='$%{text:.2f}')  # Format as currency
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Region",
        yaxis_title="Total Revenue ($)",
        showlegend=False  # Hide legend if not needed
    )
    st.caption(f"📍 Displays the top {top_n} regions based on total sales revenue.")
    return fig

def plot_region_sales_growth(sales_data, top_n=10):
    """
    Plots sales growth trends for the top N regions based on total revenue.

    Parameters:
        - sales_data: DataFrame containing sales data with columns 'order_date', 'location', and 'product_revenue'.
        - top_n: Number of top regions (cities) to display (default is 10).
    """
    # Ensure 'order_date' is in datetime format
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], errors='coerce', utc=True)
    
    # Verify if the column is properly converted to datetime
    if not pd.api.types.is_datetime64_any_dtype(sales_data['order_date']):
        raise ValueError("The 'order_date' column is not in datetime format.")
    
    # Extract year and month for grouping
    sales_data['year_month'] = sales_data['order_date'].dt.to_period('M').astype(str)

    # Normalize the 'location' column
    sales_data['location'] = sales_data['location'].str.strip().str.lower()

    # Aggregate total sales revenue by region (city)
    total_region_sales = sales_data.groupby('location', as_index=False)['product_revenue'].sum()

    # Filter for the top N regions by total sales revenue
    top_regions = total_region_sales.sort_values(by='product_revenue', ascending=False).head(top_n)['location']

    # Filter the sales data to include only the top N regions
    filtered_sales_data = sales_data[sales_data['location'].isin(top_regions)]

    # Aggregate sales by region and time
    region_time_sales = filtered_sales_data.groupby(['location', 'year_month'], as_index=False)['product_revenue'].sum()

    # Calculate percentage change (growth rate) within each region
    region_time_sales['growth_rate'] = region_time_sales.groupby('location')['product_revenue'].pct_change() * 100

    # Plot sales trends for each region
    fig = px.line(
        region_time_sales,
        x='year_month',
        y='product_revenue',
        color='location',
        title=f'Sales Growth Trends for Top {top_n} Regions',
        labels={'year_month': 'Year-Month', 'product_revenue': 'Sales'},
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set3  # Use a predefined color palette
    )
    fig.update_layout(
        template='plotly_white',
        xaxis_title="Year-Month",
        yaxis_title="Sales",
        hovermode="x unified"
    )
    st.caption(f"📈 Sales growth trends for the top {top_n} regions.")
    return fig

def segment_by_location(customer_data):
    """
    Visualizes the top 10 locations by customer count.
    """
    # Normalize the 'location' column
    customer_data['location'] = customer_data['location'].str.strip().str.lower()
    location_summary = customer_data.groupby('location').size().reset_index(name='customer_count')
    top_10_locations = location_summary.nlargest(10, 'customer_count')
    fig = px.bar(
        top_10_locations,
        x='location',
        y='customer_count',
        title='Top 10 Locations by Customer Count',
        labels={'location': 'Location', 'customer_count': 'Customer Count'},
        text='customer_count'
    )
    st.caption("📌 Highlights the top 10 locations with the highest customer counts.")
    return fig
   
