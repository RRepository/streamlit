import streamlit as st
import pandas as pd
import snowflake.connector
from fpdf import FPDF
import os
from tempfile import NamedTemporaryFile

def get_snowflake_connection():
    return snowflake.connector.connect(
        user="RCHITIKIREDDY",
        password="Welcome@2024",
        account="sob76570.us-east-1",
        warehouse="COMPUTE_WH",
        database="SALES_DB_STL",
        schema="SALES_SC_STL"
    )
st.title('Sales Dashboard')
connection = get_snowflake_connection()
cursor = connection.cursor()
cursor.execute('SELECT * FROM SALES_DB_STL.SALES_SC_STL.SALES')
rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]
data = pd.DataFrame(rows, columns=columns)


df = pd.DataFrame(data)

st.title("Sales Invoice Generator")

order_number = st.number_input("Enter Order Number", min_value=1)

if order_number:
    order_data_filtered = df[df['ORDERNUMBER'] == order_number]
    

    if order_data_filtered.empty:
        st.error(f"Order {order_number} not found.")
    else:
        order_data = order_data_filtered.iloc[0]
        
        def create_invoice(order_data):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt=f"Invoice for Order {order_data['ORDERNUMBER']}", ln=True, align="C")
            
            
            pdf.set_font("Arial", size=12)
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Customer: {order_data['CUSTOMERNAME']}", ln=True)
            pdf.cell(200, 10, txt=f"Product Line: {order_data['PRODUCTLINE']}", ln=True)
            pdf.cell(200, 10, txt=f"Quantity Ordered: {order_data['QUANTITYORDERED']}", ln=True)
            pdf.cell(200, 10, txt=f"Price Each: ${order_data['PRICEEACH']}", ln=True)
            pdf.cell(200, 10, txt=f"Total Sales: ${order_data['SALES']}", ln=True)
            pdf.cell(200, 10, txt=f"Order Date: {order_data['NEW_ORDER_DATE']}", ln=True)
            
            return pdf

        pdf = create_invoice(order_data)
        
        with NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            pdf.output(temp_file.name)
            
            with open(temp_file.name, 'rb') as f:
                pdf_data = f.read()
        
        os.remove(temp_file.name)

        st.download_button(
            label="Download Invoice PDF",
            data=pdf_data,
            file_name=f"Invoice_Order_{order_number}.pdf",
            mime="application/pdf"
        )
