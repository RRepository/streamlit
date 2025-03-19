import streamlit as st
import pandas as pd
import snowflake.connector
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time


def get_snowflake_connection():
    return snowflake.connector.connect(
        user="RCHITIKIREDDY",
        password="Welcome@2024",
        account="sob76570.us-east-1",
        warehouse="COMPUTE_WH",
        database="SALES_DB_STL",
        schema="SALES_SC_STL"
    )




# Display the spinner
with st.spinner('Processing data...'):
        time.sleep(5)


st.title('Sales Dashboard')
connection = get_snowflake_connection()
cursor = connection.cursor()
cursor.execute('SELECT * FROM SALES_DB_STL.SALES_SC_STL.SALES')
rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]
df = pd.DataFrame(rows, columns=columns)



productline = st.sidebar.selectbox('Select a Productline', df['PRODUCTLINE'].unique())
filtered_data = df[df['PRODUCTLINE'] == productline]


import matplotlib.pyplot as plt
sales_by_status = filtered_data.groupby('STATUS')['SALES'].sum().reset_index()
sales_by_status_sorted = sales_by_status.sort_values(by='SALES', ascending=True).reset_index(drop=True)
fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the size of the plot
ax.bar(sales_by_status_sorted['STATUS'], sales_by_status_sorted['SALES'], color='skyblue')
ax.set_xlabel('Status')  
ax.set_ylabel('Sales')   
ax.set_title('Sales by Status')
plt.xticks(rotation=45)
st.subheader('Overall Sales by Status')
st.pyplot(fig)


filtered_data['NEW_ORDER_DATE'] = pd.to_datetime(df['NEW_ORDER_DATE'], errors='coerce')
filtered_data['YEAR'] = filtered_data['NEW_ORDER_DATE'].dt.year
filtered_data['YEAR'] = filtered_data['YEAR'].astype(int)
sales_by_year = filtered_data.groupby('YEAR')['SALES'].sum().reset_index()
sales_by_year_sorted = sales_by_year.sort_values(by='YEAR', ascending=True).reset_index(drop=True)
fig1, ax1 = plt.subplots(figsize=(10, 6))  # Adjust the size of the plot
ax1.bar(sales_by_year_sorted['YEAR'], sales_by_year_sorted['SALES'], color='skyblue')
ax1.set_xlabel('Year')  
ax1.set_ylabel('Sales')  
ax1.set_title('Sales by Year')
ax1.set_xticks(sales_by_year_sorted['YEAR'])
plt.xticks(rotation=45)
st.subheader('Overall Sales by Year')
st.pyplot(fig1)

sales_by_territory = filtered_data.groupby('TERRITORY')['SALES'].sum().reset_index()
sales_by_territory_sorted = sales_by_territory.sort_values(by='SALES', ascending=True).reset_index(drop=True)

fig2, ax2 = plt.subplots(figsize=(3, 3))
ax2.pie(
    sales_by_territory['SALES'],
    labels=sales_by_territory['TERRITORY'],
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.Paired.colors,
    wedgeprops={'width': 0.5},
    labeldistance=1.1,  # Adjust this if you need more space for the label
    textprops={'fontsize': 5, 'fontweight': 'normal', 'fontname': 'Arial'}  # Font settings
)
st.subheader('Overall Sales by Territory')
st.pyplot(fig2)


#pyplot

filtered_data['YEAR'] = filtered_data['NEW_ORDER_DATE'].dt.year
filtered_data['YEAR'] = filtered_data['YEAR'].astype(int)
filtered_data['YEAR'] = filtered_data['YEAR'].astype(str)
sales_by_territory = filtered_data.groupby('YEAR')['SALES'].sum().reset_index()
sales_by_territory_sorted = sales_by_territory.sort_values(by='YEAR', ascending=True).reset_index(drop=True)

# Create a Plotly Line Chart for Sales by Territory
import plotly.graph_objects as go
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=sales_by_territory_sorted['YEAR'],
    y=sales_by_territory_sorted['SALES'],
    mode='lines+markers', 
    line=dict(color='skyblue', width=2),
    marker=dict(size=8, color='blue', symbol='circle'), 
))

fig2.update_layout(
    title="Sales by Year (Line Chart)",
    xaxis_title="YEAR",
    yaxis_title="Sales",
    xaxis_tickangle=45 
)

st.subheader('Trend Analysis of Sales')
st.plotly_chart(fig2, width=800, height=500)

filtered_data['YEAR'] = filtered_data['NEW_ORDER_DATE'].dt.year
filtered_data['YEAR'] = filtered_data['YEAR'].astype(int)
filtered_data['YEAR'] = filtered_data['YEAR'].astype(str)
sales_by_territory = filtered_data.groupby('YEAR')['SALES'].sum().reset_index()
sales_by_territory_sorted = sales_by_territory.sort_values(by='YEAR', ascending=True).reset_index(drop=True)

# Concatenate the dataframes vertically (if needed)
data = pd.concat([sales_by_territory, sales_by_territory_sorted], ignore_index=True)

# Display the Line Chart
st.line_chart(data.set_index('YEAR'))

#st.multiselect("choose",["Ships","Planes", "Trains"])
#st.slider("Pick a number", 0, 100)
#st.select_slider("Pick mode of transport",["S","P", "T"])
#t.radio("Pick mode of transport",["S","P", "T"])
