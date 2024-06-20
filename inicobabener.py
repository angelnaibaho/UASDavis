import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector as mysqlcon
import plotly.express as px

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
    pivot_data = data.pivot(index='Product Category', columns='Gender', values='Quantity').reset_index()
    fig = px.bar(pivot_data, 
                 x='Product Category', 
                 y=pivot_data.columns[1:], 
                 barmode='group',
                 title="Total Quantity by Product Category and Gender")
    fig.update_layout(xaxis_title='Product Category', yaxis_title='Total Quantity')
    return fig

def plot_bubble_chart(data):
    fig = px.scatter(data, 
                     x='SalesTerritoryRegion', 
                     y='CustomerCount', 
                     size='CustomerCount', 
                     hover_name='SalesTerritoryRegion', 
                     title="Customer Count by Sales Territory Region (Bubble Plot)",
                     size_max=60)
    fig.update_layout(xaxis_title='Sales Territory Region', yaxis_title='Customer Count')
    return fig

# nav sidebar
with st.sidebar:
    selected = option_menu("Angel Dashboard", ['Grafik', 'Book Scrap'],
        icons=['film', 'book', 'chart'], menu_icon="house", default_index=0)

# Grafik
if selected == 'Grafik':
    # # Year selection above the "GRAFIK" heading
    # year = st.selectbox("Select Year", options=[2001, 2002, 2003, 2004], index=0)
    
    st.write("""# GRAFIK""")
    query = """
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
    data = fetch_data_from_db(query)
    if data is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = plot_histogram(data)
            st.plotly_chart(fig1)

        with col2:
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
                fig2 = plot_bubble_chart(data_bubble)
                st.plotly_chart(fig2)
