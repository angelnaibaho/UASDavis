import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector as mysqlcon
import matplotlib.pyplot as plt

# Function to create a connection to the database
def create_connection():
    return mysqlcon.connect(
        host="kubela.id",
        user="davis2024irwan",
        passwd="wh451n9m@ch1n3",
        port=3306,
        database="aw"
    )

# Function to fetch data from the database
def fetch_data_from_db(query):
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(data)
    except mysqlcon.Error as e:
        st.error(f"Error fetching data: {e}")
        return None

def plot_histogram(data):
    pivot_data = data.pivot(index='Product Category', columns='Gender', values='Quantity')

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(20, 11))
    pivot_data.plot(kind='bar', ax=ax)

    ax.set_title("Total Quantity by Product Category and Gender", color='white')
    ax.set_xlabel('Product Category', color='white')
    ax.set_ylabel('Total Quantity', color='white')

    ax.legend(title='Gender', facecolor='black', edgecolor='white', loc='upper right')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    fig.patch.set_edgecolor('white')

    ax.tick_params(colors='white', which='both')
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

def plot_bubble_chart(data):
    sizes = data['CustomerCount'] * 20

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(data['SalesTerritoryRegion'], data['CustomerCount'], s=sizes, alpha=0.5)

    ax.set_title("Customer Count by Sales Territory Region (Bubble Plot)", color='white')
    ax.set_xlabel('Sales Territory Region', color='white')
    ax.set_ylabel('Customer Count', color='white')

    plt.xticks(rotation=90)
    plt.tight_layout()

    return fig

# Query SQL untuk mengambil data jumlah pesanan berdasarkan bulan
query_monthly_orders = """
    SELECT 
        month.EnglishMonthName,  
        COUNT(fs.OrderQuantity) AS Quantity
    FROM  
        dimtime AS month
    JOIN 
        factinternetsales AS fs ON month.TimeKey = fs.OrderDateKey 
    WHERE 
        month.CalendarYear BETWEEN 2003 AND 2004
    GROUP BY   
        month.EnglishMonthName
    ORDER BY  
        FIELD(month.EnglishMonthName,
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December');
"""

# nav sidebar
with st.sidebar:
    selected = option_menu("Angel Dashboard", ['Grafik', 'Book Scrap'],
        icons=['film', 'book', 'chart'], menu_icon="house", default_index=0)

# Grafik
if selected == 'Grafik':
    
    st.write("""# GRAFIK DATABASE ADEVENTURE WORKS""")
    
    # Fetch data for histogram
    st.write("""1. GRAFIK HISTOGRAM (COMPARISON)""")
    query_histogram = """
        SELECT 
            dpc.EnglishProductCategoryName AS `Product Category`, 
            gen.Gender AS Gender,
            COUNT(fs.OrderQuantity) AS Quantity 
        FROM 
            factinternetsales fs 
        JOIN dimproduct dp ON dp.ProductKey = fs.ProductKey 
        JOIN dimproductsubcategory dsc ON dp.ProductSubcategoryKey = dsc.ProductSubcategoryKey 
        JOIN dimproductcategory dpc ON dsc.ProductCategoryKey = dpc.ProductCategoryKey 
        JOIN dimcustomer gen ON fs.CustomerKey = gen.CustomerKey
        GROUP BY 
            dpc.EnglishProductCategoryName,
            gen.Gender
        ORDER BY 
            Quantity;
    """
    data_histogram = fetch_data_from_db(query_histogram)
    st.write("""Grafik dibawah ini menunjukkan total banyaknya penjualan kategori produk berdasarkan gender.
    Dapat dilihat bahwa produk yang memiliki penjualan terbesar yaitu pada kategori Accessoris dan yang paling banyak membeli yaitu Male sebanyak 18233 dan Female sebanyak 17859""")
    
    if data_histogram is not None:
        # Plot histogram
        fig1 = plot_histogram(data_histogram)
        st.pyplot(fig1)

        # Fetch data for bubble chart
        st.write("""2. Bubble Plot Chart""")
        query_bubble = """
            SELECT 
                dimsalesterritory.SalesTerritoryRegion,  
                COUNT(dimcustomer.CustomerKey) AS CustomerCount 
            FROM  
                dimgeography 
            JOIN dimcustomer ON dimgeography.GeographyKey = dimcustomer.GeographyKey 
            JOIN dimsalesterritory ON dimgeography.SalesTerritoryKey = dimsalesterritory.SalesTerritoryKey
            GROUP BY   
                dimgeography.SalesTerritoryKey, dimsalesterritory.SalesTerritoryRegion
            ORDER BY  
                CustomerCount;
        """
        data_bubble = fetch_data_from_db(query_bubble)
        if data_bubble is not None:
            # Plot bubble chart
            fig2 = plot_bubble_chart(data_bubble)
            st.pyplot(fig2)

        # Plot line chart for monthly orders
        try:
            data_monthly_orders = pd.read_sql(query_monthly_orders, create_connection())

            # Plotting line chart
            plt.figure(figsize=(12, 8))
            plt.plot(data_monthly_orders['EnglishMonthName'], data_monthly_orders['Quantity'], marker='o')

            # Menambahkan judul
            plt.title('Order Quantity by Month (Line Chart)')

            # Menambahkan label sumbu x dan y
            plt.xlabel('Month')
            plt.ylabel('Order Quantity')

            # Memutar label sumbu x agar tidak bertabrakan
            plt.xticks(rotation=45)

            # Menampilkan plot
            plt.tight_layout()
            st.pyplot(plt)

        except Exception as e:
            st.error(f"An error occurred: {e}")
