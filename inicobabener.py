import streamlit as st
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

# Function to fetch data from the database based on selected year
def fetch_data_from_db(selected_year):
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query to fetch data based on selected year
        query = f"""
        SELECT 
            dpc.EnglishProductCategoryName AS `Product Category`, 
            gen.Gender AS Gender,
            COUNT(fs.OrderQuantity) AS Quantity 
        FROM 
            factinternetsales fs 
        JOIN dimtime dt ON fs.OrderDateKey = dt.TimeKey
        JOIN dimproduct dp ON dp.ProductKey = fs.ProductKey 
        JOIN dimproductsubcategory dsc ON dp.ProductSubcategoryKey = dsc.ProductSubcategoryKey 
        JOIN dimproductcategory dpc ON dsc.ProductCategoryKey = dpc.ProductCategoryKey 
        JOIN dimcustomer gen ON fs.CustomerKey = gen.CustomerKey
        WHERE 
            dt.CalendarYear = {2001}  -- Filter based on selected year
        GROUP BY 
            dpc.EnglishProductCategoryName,
            gen.Gender
        ORDER BY 
            Quantity;
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return pd.DataFrame(data)
    
    except mysqlcon.Error as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to plot histogram based on fetched data
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

# Streamlit app code
def main():
    st.title("Sales Dashboard")
    
    # Year selection using selectbox
    selected_year = st.selectbox("Select Year", options=[2001, 2002, 2003, 2004])

    # If Grafik is selected
    if st.sidebar.option_menu("Angel Dashboard", ['Grafik', 'Book Scrap'], icons=['film', 'book', 'chart'], menu_icon="house", default_index=0) == 'Grafik':
        st.write("""# GRAFIK""")
        
        # Fetch data based on selected year
        data = fetch_data_from_db(selected_year)
        
        # Display the data in columns
        if data is not None:
            col1, col2 = st.columns(2)

            with col1:
                # Plot histogram
                fig1 = plot_histogram(data)
                st.pyplot(fig1)

            # You can add more plots or visualizations here

# Main function to run the Streamlit app
if __name__ == "__main__":
    main()
