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
    fig, ax = plt.subplots(figsize=(10, 6))
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

# Sidebar with navigation
with st.sidebar:
    selected = option_menu("Angel Dashboard", ['Grafik', 'Book Scrap'],
                           icons=['film', 'book', 'chart'], menu_icon="house", default_index=0)

# Main content
if selected == 'Grafik':
    # Year selection above the "GRAFIK" heading
    year = st.selectbox("Select Year", options=[2012, 2013, 2014, 2015], index=0)

    st.write("""# GRAFIK""")

    query = f"""
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
    WHERE 
        YEAR(fs.OrderDate) = {year}
    GROUP BY 
        dpc.EnglishProductCategoryName,
        gen.Gender
    ORDER BY 
        Quantity;
    """
    data = fetch_data_from_db(query)
    if data is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = plot_histogram(data)
            st.pyplot(fig1)

        with col2:
            query_bubble = f"""
            SELECT 
                dimsalesterritory.SalesTerritoryRegion,  
                COUNT(dimcustomer.CustomerKey) AS CustomerCount 
            FROM  
                dimgeography 
            JOIN dimcustomer ON dimgeography.GeographyKey = dimcustomer.GeographyKey 
            JOIN dimsalesterritory ON dimgeography.SalesTerritoryKey = dimsalesterritory.SalesTerritoryKey
            WHERE 
                YEAR(dimcustomer.DateFirstPurchase) = {year}
            GROUP BY   
                dimgeography.SalesTerritoryKey, dimsalesterritory.SalesTerritoryRegion
            ORDER BY  
                CustomerCount;
            """
            data_bubble = fetch_data_from_db(query_bubble)
            if data_bubble is not None:
                fig2 = plot_bubble_chart(data_bubble)
                st.pyplot(fig2)