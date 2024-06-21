import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector as mysqlcon
import matplotlib.pyplot as plt
import plotly.express as px
from gtts import gTTS
import translators as ts  
# nav sidebar
with st.sidebar:
    selected = option_menu("Angel Dashboard", ['Grafik AW', 'Movie'],
                           icons=['grafik', 'film'], menu_icon="house", default_index=0)

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


# Grafik
if selected == 'Grafik AW':
    
    st.write("""Anna Vita Angelina Naibaho - 21082010135""")
    st.write("""# GRAFIK DATABASE ADEVENTURE WORKS""")
    
    # Fetch data for histogram
    st.write("""1. Column Histogram (Comparison)""")
    text = """
        Grafik di bawah ini menampilkan banyaknya penjualan berdasarkan kategori produk dan gender selama periode tiga tahun (2001-2004). 
        Chart "Total Quantity by Product Category and Gender" menggunakan column chart (histogram) yang merupakan bagian dari jenis chart bagan distribusi untuk menampilkan jumlah total pesanan berdasarkan kategori produk dan gender pelanggan. Sumbu X menunjukkan kategori produk, sedangkan sumbu Y menunjukkan jumlah total pesanan. Legenda menampilkan gender pelanggan, dengan setiap batang berwarna berbeda untuk "Male" (berwarna kuning) dan "Female" (berwarna hijau).

        Dapat dilihat bahwa kategori produk dengan penjualan tertinggi adalah Accessoris, dengan pria membeli sebanyak 18,233 unit dan wanita sebanyak 17,859 unit. 
        Di sisi lain, kategori produk dengan penjualan terendah adalah Clothing, dengan pria membeli 7,525 unit dan wanita membeli 7,680 unit. 
        Perhatian lebih lanjut mungkin perlu diberikan pada kategori produk yang memiliki penjualan terendah untuk meningkatkan performa di masa mendatang.
        """
    st.markdown(text)
    
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
    if st.button("Jalankan Text Grafik Comparison"):
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
        st.write("""2. Bubble Plot Chart (Relationship)""")
        text2 = """
        Grafik di bawah ini menunjukkan jumlah pelanggan selama tiga tahun terakhir (2001-2004). Setiap titik pada plot mewakili satu wilayah penjualan, di mana posisi horizontal menunjukkan wilayah tersebut dan posisi vertikal menunjukkan jumlah pelanggan di wilayah tersebut. Ukuran bulatan (bubble) pada setiap titik mencerminkan jumlah pelanggan di wilayah tersebut, dengan bulatan yang lebih besar menunjukkan wilayah dengan lebih banyak pelanggan.

        Grafik ini membantu untuk melihat sebaran pelanggan di berbagai wilayah penjualan, serta memudahkan dalam mengidentifikasi wilayah-wilayah dengan jumlah pelanggan tertinggi. Dapat disimpulkan bahwa wilayah Southwest menonjol sebagai wilayah dengan jumlah pelanggan terbanyak dalam periode tersebut.
        """
        st.markdown(text2)

        # Tambahkan tombol untuk memainkan TTS dalam bahasa Indonesia
        if st.button("Jalankan Text Grafik Relationship"):
            language_code = 'id'
            hasil2 = ts.translate_text(text2, to_language=language_code, translator='google')
            tts = gTTS(text=hasil2, lang=language_code)
            tts.save('output_id.mp3')  # Simpan output sebagai file audio
            audio_file = open('output_id.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

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
        st.write("""3. Line Histogram (Distribution)""")
        text3 = """
        Grafik di bawah ini menunjukkan banyaknya pembelian selama satu setengah tahun terakhir (2003-2004) berdasarkan bulannya. Grafik ini memberikan gambaran visual tentang jumlah pesanan yang diproses setiap bulannya dalam periode tersebut. Dengan melihat grafik ini, kita dapat dengan jelas mengidentifikasi bulan-bulan dengan jumlah pembelian tertinggi. 

        Dapat dilihat bahwa bulan yang menonjol sebagai bulan dengan jumlah pembelian tertinggi adalah bulan Juni, dengan total pesanan mencapai 5866 unit. Informasi ini bermanfaat untuk mengevaluasi performa penjualan dari waktu ke waktu dan untuk merencanakan strategi pemasaran serta pengelolaan persediaan produk yang lebih efektif. Grafik ini memanfaatkan data historis untuk memberikan wawasan tentang tren pembelian bulanan, membantu dalam mengidentifikasi pola dan faktor-faktor yang mempengaruhi permintaan konsumen. 
        """
        st.markdown(text3)

        # Tambahkan tombol untuk memainkan TTS dalam bahasa Indonesia
        if st.button("Jalankan Text Grafik Distribusi"):
            language_code = 'id'
            hasil3 = ts.translate_text(text3, to_language=language_code, translator='google')
            tts = gTTS(text=hasil3, lang=language_code)
            tts.save('output_id.mp3')  # Simpan output sebagai file audio
            audio_file = open('output_id.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

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


        # Plot Donut Chart
        st.write("""4. Donut Chart (Composition)""")
        text4 = """
        Grafik di bawah ini menunjukkan penjualan total berdasarkan grup wilayah penjualan dalam persen selama tiga tahun (2001-2004). menampilkan proporsi penjualan total berdasarkan grup wilayah penjualan. Setiap bagian dari pie chart mewakili persentase penjualan yang disumbangkan oleh masing-masing grup wilayah penjualan. Label pada setiap bagian menunjukkan nama wilayah berdasarkan benua penjualan, sementara persentase penjualan ditampilkan di sekitar bagian pie. 
        
        Dengan informasi ini, perusahaan dapat memahami seberapa besar peran masing-masing wilayah dalam pencapaian target penjualan dan mengarahkan strategi pemasaran dan penjualan lebih lanjut sesuai dengan temuan ini.
        """
        st.markdown(text4)

        # Tambahkan tombol untuk memainkan TTS dalam bahasa Indonesia
        if st.button("Jalankan Text Grafik Composition"):
            language_code = 'id'
            hasil4 = ts.translate_text(text4, to_language=language_code, translator='google')
            tts = gTTS(text=hasil4, lang=language_code)
            tts.save('output_id.mp3')  # Simpan output sebagai file audio
            audio_file = open('output_id.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

        # Fetch data for pie chart
        query_pie = """
            SELECT 
                dt.SalesTerritoryGroup,
                SUM(fs.SalesAmount) AS TotalPenjualan 
            FROM 
                factinternetsales fs 
            JOIN dimsalesterritory dt ON dt.SalesTerritoryKey = fs.SalesTerritoryKey 
            GROUP BY 
                dt.SalesTerritoryGroup
            ORDER BY 
                TotalPenjualan DESC;
        """
        data_pie = fetch_data_from_db(query_pie)
    
        if data_pie is not None:
            # Plot pie chart (donut chart)
            plt.figure(figsize=(8, 8))
            plt.pie(data_pie['TotalPenjualan'], labels=data_pie['SalesTerritoryGroup'], autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3))
            plt.title('Total Penjualan by Sales Territory Group')
            plt.axis('equal')
            
            # Menampilkan plot di Streamlit
            st.pyplot(plt)

if (selected == 'Movie'):
    st.write("""# Movie Scrapping""")
    st.write("""Scrapping from Warner Bros. (US)""")

    # Membaca data dari file CSV
    df = pd.read_csv("imdb_scrap.csv")

    text5 = """
    Grafik di bawah ini merupakan grafik bar horizontal yang menunjukkan perbandingan rating film berdasarkan nama film. Tujuannya adalah untuk memberikan gambaran mengenai seberapa baik penilaian film-film tersebut.
    """
    st.markdown(text5)

    # Tambahkan tombol untuk memainkan TTS dalam bahasa Indonesia
    if st.button("Jalankan Text Grafik Bar"):
        language_code = 'id'
        hasil5 = ts.translate_text(text5, to_language=language_code, translator='google')
        tts = gTTS(text=hasil5, lang=language_code)
        tts.save('output_id.mp3')  # Simpan output sebagai file audio
        audio_file = open('output_id.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

    # Ubah scatter plot menjadi bar chart dengan orientasi horizontal
    fig = px.bar(df, x='Rating', y='Name', orientation='h')

    # Konfigurasi tampilan bar chart
    fig.update_layout(
        title='Horizontal Bar Chart of Film Ratings',
        xaxis_title='Rating',
        yaxis_title='Film Titles'
    )

    # Menampilkan bar chart di Streamlit
    st.plotly_chart(fig)

    st.write("""2. Column Histogram""")

    # Membaca data dari file CSV
    df = pd.read_csv("imdb_scrap.csv")
    text6 = """
    Grafik di bawah ini merupakan Column Histogram yang menunjukkan distribusi durasi film. Grafik histogram ini menunjukkan bahwa durasi film umumnya berkisar antara lebih dari 110 dan kurang dari 120 menit. Distribusi durasi film secara keseluruhan relatif merata, dengan sedikit film yang memiliki durasi di bawah 90 menit atau di atas 130 menit. Grafik ini membantu menganalisis bagaimana durasi film terdistribusi di seluruh dataset.
    """
    st.markdown(text6)

    # Tambahkan tombol untuk memainkan TTS dalam bahasa Indonesia
    if st.button("Jalankan Text Column Histogram"):
        language_code = 'id'
        hasil6 = ts.translate_text(text6, to_language=language_code, translator='google')
        tts = gTTS(text=hasil6, lang=language_code)
        tts.save('output_id.mp3')  # Simpan output sebagai file audio
        audio_file = open('output_id.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    
    # Membuat histogram garis
    fig = px.histogram(df, x='Durasi(Menit)', histnorm='percent', nbins=20)

    # Konfigurasi tampilan histogram garis
    fig.update_layout(
        title='Line Histogram of Film Durations',
        xaxis_title='Duration (Minutes)',
        yaxis_title='Percentage',
    )

    # Menampilkan histogram garis di Streamlit
    st.plotly_chart(fig)

    st.write("""3. Donut Chart""")

     # Membaca data dari file CSV
    df = pd.read_csv("imdb_scrap.csv")
    text7 = """
    Grafik di bawah ini merupakan Donut Chart yang menunjukkan distribusi durasi film dalam bentuk persentase. Donut chart ini menunjukkan bahwa rating PG dan PG-13 adalah rating yang paling umum untuk film. Persentase film dengan rating R, G, dan Not Rated relatif kecil.
    """
    st.markdown(text7)

    # Tambahkan tombol untuk memainkan TTS dalam bahasa Indonesia
    if st.button("Jalankan Text Donut Chart"):
        language_code = 'id'
        hasil7 = ts.translate_text(text7, to_language=language_code, translator='google')
        tts = gTTS(text=hasil7, lang=language_code)
        tts.save('output_id.mp3')  # Simpan output sebagai file audio
        audio_file = open('output_id.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

    # Membaca data dari file CSV
    df = pd.read_csv("imdb_scrap.csv")
    
    # Menghitung jumlah film per rating
    rating_counts = df['Rating'].value_counts().reset_index()
    rating_counts.columns = ['Rating', 'Count']

    # Ubah menjadi donut chart
    fig = px.pie(rating_counts, names='Rating', values='Count', hole=0.4)

    # Konfigurasi tampilan donut chart
    fig.update_layout(
        title='Donut Chart of Film Ratings'
    )

    # Menampilkan donut chart di Streamlit
    st.plotly_chart(fig)


    st.write("""4. Scatter Plot""")

    text8 = """
    Grafik scatter plot ini menunjukkan bahwa opening week (minggu pertama film dirilis) merupakan salah satu faktor yang dapat memengaruhi gross world film. Hal ini terlihat dari tren positif yang menunjukkan bahwa semakin tinggi opening week, semakin tinggi pula gross world film.
    """
    st.markdown(text8)

    # Tambahkan tombol untuk memainkan TTS dalam bahasa Indonesia
    if st.button("Jalankan Text Scatter Plot"):
        language_code = 'id'
        hasil8 = ts.translate_text(text8, to_language=language_code, translator='google')
        tts = gTTS(text=hasil8, lang=language_code)
        tts.save('output_id.mp3')  # Simpan output sebagai file audio
        audio_file = open('output_id.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    # Membaca data dari file CSV
    df = pd.read_csv("imdb_scrap.csv")
    
    # Ubah menjadi scatter plot
    fig = px.scatter(df, x='Opening_Week', y='Gross_World')

    # Konfigurasi tampilan scatter plot
    fig.update_layout(
        title='Scatter Plot of Opening Week vs Gross World',
        xaxis_title='Opening Week',
        yaxis_title='Gross World'
    )

    # Menampilkan scatter plot di Streamlit
    st.plotly_chart(fig)
