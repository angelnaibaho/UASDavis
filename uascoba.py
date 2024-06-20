import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import mysql.connector as mysqlcon
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Function to create a connection to the database
def create_connection():
    return mysql.connector.connect(
        host="kubela.id",
        user="davis2024irwan",
        passwd="wh451n9m@ch1n3",
        port=3306,  
        database="aw"
    )

def plot_histogram(data):
    # Pivot data
    pivot_data = data.pivot(index='Product Category', columns='Gender', values='Quantity')

    # Mengubah gaya plot menjadi dark_background
    plt.style.use('dark_background')

    # Plotting column chart (histogram)
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='bar', ax=ax)

    # Adding Title to the Plot
    ax.set_title("Total Quantity by Product Category and Gender", color='white')

    # Setting the X and Y labels
    ax.set_xlabel('Product Category', color='white')
    ax.set_ylabel('Total Quantity', color='white')

    # Adding the legends
    ax.legend(title='Gender', facecolor='black', edgecolor='white', loc='upper right')
    ax.set_facecolor('black')  # Set background color of the plot area
    fig.patch.set_facecolor('black')  # Set background color of the figure
    fig.patch.set_edgecolor('white')  # Set edge color of the figure

    # Customize tick colors
    ax.tick_params(colors='white', which='both')  # Change color of ticks

    plt.xticks(rotation=45)  # Rotate x-axis labels if necessary
    plt.tight_layout()       # Adjust layout to make room for x-axis labels

    return fig

def plot_bubble_chart(data):
    # Calculate bubble sizes based on CustomerCount
    sizes = data['CustomerCount'] * 20  # Adjust scaling factor as needed

    # Plotting the bubble plot
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(data['SalesTerritoryRegion'], data['CustomerCount'], s=sizes, alpha=0.5)

    # Adding Title to the Plot
    ax.set_title("Customer Count by Sales Territory Region (Bubble Plot)", color='white')

    # Setting the X and Y labels
    ax.set_xlabel('Sales Territory Region', color='white')
    ax.set_ylabel('Customer Count', color='white')

    # Rotate x-axis labels if necessary
    plt.xticks(rotation=90)
    plt.tight_layout()  # Adjust layout to make room for x-axis labels

    return fig

# nav sidebar
with st.sidebar:
    selected = option_menu("Angel Dashboard", ['Grafik', 'Book Scrap'], 
        icons=['film', 'book', 'chart'], menu_icon="house", default_index=0)

# Grafik
if selected == 'Grafik':
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
        Quantity;"""
    data = fetch_data_from_db(query)
    if data is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = plot_histogram(data)
            st.pyplot(fig1)

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
                st.pyplot(fig2)
