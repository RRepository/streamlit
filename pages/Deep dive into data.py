import streamlit as st
import pandas as pd
import snowflake.connector

# Function to create a connection to Snowflake
def get_snowflake_connection():
    return snowflake.connector.connect(
        user="RCHITIKIREDDY",
        password="Welcome@2024",
        account="sob76570.us-east-1",
        warehouse="COMPUTE_WH",
        database="SALES_DB_STL",
        schema="SALES_SC_STL"
    )

# Function to get available databases from Snowflake
def get_databases():
    try:
        query = "SHOW DATABASES"
        connection = get_snowflake_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        databases = [row[1] for row in cursor.fetchall()]
        cursor.close()
        return databases
    except Exception as e:
        st.error(f"Error fetching databases: {e}")
        return []

# Function to get available schemas from Snowflake
def get_schemas(database):
    try:
        query = f"SHOW SCHEMAS IN DATABASE {database}"
        connection = get_snowflake_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        schemas = [row[1] for row in cursor.fetchall()]
        cursor.close()
        return schemas
    except Exception as e:
        st.error(f"Error fetching schemas: {e}")
        return []

# Function to get available tables from a schema in Snowflake
def get_tables(schema):
    try:
        query = f"SHOW TABLES IN SCHEMA {schema}"
        connection = get_snowflake_connection()
        cursor = connection.cursor()        
        cursor.execute(query)
        tables = [row[1] for row in cursor.fetchall()]
        cursor.close()
        return tables
    except Exception as e:
        st.error(f"Error fetching tables: {e}")
        return []

# Function to get the data from a specific table in Snowflake
def get_table_data(schema, table):
    try:
        query = f"SELECT * FROM {schema}.{table} LIMIT 100"
        connection = get_snowflake_connection()
        cursor = connection.cursor()        
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=columns)
        return df
    except Exception as e:
        st.error(f"Error fetching data from table {table}: {e}")
        return pd.DataFrame()

# Main function to run the app
def main():
    st.title("Snowflake Database Viewer")

    # Create connection to Snowflake
    connection = get_snowflake_connection()

    # Step 1: Select a database
    databases = get_databases()
    if databases:
        selected_database = st.selectbox("Select a database", databases)

        # Step 2: Select a schema from the selected database
        schemas = get_schemas(selected_database)
        if schemas:
            selected_schema = st.selectbox("Select a schema", schemas)

            # Step 3: Select a table from the selected schema
            tables = get_tables(selected_schema)
            if tables:
                selected_table = st.selectbox("Select a table", tables)

                # Step 4: Display data from the selected table
                if selected_table:
                    df = get_table_data(selected_schema, selected_table)
                    if not df.empty:
                        st.write(f"Data from table: {selected_table}")
                        st.dataframe(df)
                    else:
                        st.error(f"No data found in the table {selected_table}")
            else:
                st.error(f"No tables found in the schema {selected_schema}")
        else:
            st.error(f"No schemas found in the database {selected_database}")
    else:
        st.error("No databases found")

if __name__ == "__main__":
    main()
