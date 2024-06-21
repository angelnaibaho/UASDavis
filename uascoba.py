import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector as mysqlcon
import matplotlib.pyplot as plt
from gtts import gTTS
import translators as ts  # Pastikan library ini telah terinstal dengan benar

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
    
    # Tambahkan tombol untuk memainkan TTS dalam bahasa Indonesia
    if st.button("Jalankan dengan Indonesia"):
        text = """
        Grafik di bawah ini menampilkan total penjualan berdasarkan kategori produk dan gender selama periode empat tahun (2001-2004). 
        Dapat dilihat bahwa kategori produk dengan penjualan tertinggi adalah Accessoris, dengan pria membeli sebanyak 18,233 unit dan wanita sebanyak 17,859 unit. 
        Di sisi lain, kategori produk dengan penjualan terendah adalah Clothing, dengan pria membeli 7,525 unit dan wanita membeli 7,680 unit. 
        Perhatian lebih lanjut mungkin perlu diberikan pada kategori produk yang memiliki penjualan terendah untuk meningkatkan performa di masa mendatang.
        """
        language_code = 'id'
        hasil = ts.translate_text(text, to_language=language_code, translator='google')
        tts = gTTS(text=hasil, lang=language_code)
        tts.save('output_id.mp3')  # Simpan output sebagai file audio
        audio_file = open('output_id.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

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
        st.write("""3. Line Chart of Order Quantity by Month (2003-2004)""")
        query_monthly_orders = """
            SELECT 
                month.EnglishMonthName,  
                COUNT(fs.OrderQuantity) AS OrderQuantity
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
        data_monthly_orders = fetch_data_from_db(query_monthly_orders)
        if data_monthly_orders is not None:
            # Plotting line chart
            plt.figure(figsize=(12, 8))
            plt.plot(data_monthly_orders['EnglishMonthName'], data_monthly_orders['OrderQuantity'], marker='o')

            # Adding title
            plt.title('Order Quantity by Month (Line Chart)')

            # Adding labels for x and y axis
            plt.xlabel('Month')
            plt.ylabel('Order Quantity')

            # Rotating x-axis labels to avoid overlap
            plt.xticks(rotation=45)

            # Display plot
            plt.tight_layout()
            st.pyplot(plt)
