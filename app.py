import os
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error


def _extract_students_from_excel(excel_file):
    """Extracts student information from the provided Excel file."""
    try:
        df = pd.read_excel(excel_file)
        return df
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return pd.DataFrame()  


def combine_dataframes(df1, df2):
    """Combines two dataframes."""
    combined_df = pd.concat([df1, df2], axis=1)
    return combined_df


def insert_students_in_bulk(df, table_name='clientes_vehiculos'):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            
            insert_query = f"""
            INSERT INTO {table_name} (ID_Cliente, Nombre, Apellido, Correo_Electronico, Telefono, Direccion, Ciudad, ID_Vehiculo, Marca, Serie, Modelo, KM, Estado, Motor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            
            data = df.to_records(index=False).tolist()

            
            cursor.executemany(insert_query, data)

            
            connection.commit()

            st.write(f"{cursor.rowcount} rows inserted successfully.")

    except Error as e:
        st.write(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


st.title("Upload students attendance list Excel files")


uploaded_file1 = st.file_uploader("Upload Attendance list Excel file 1", type=["xls", "xlsx"])
uploaded_file2 = st.file_uploader("Upload Attendance list Excel file 2", type=["xls", "xlsx"])


df1 = pd.DataFrame()
df2 = pd.DataFrame()

if uploaded_file1 is not None:
    st.write("File 1 was uploaded successfully.")
    df1 = _extract_students_from_excel(uploaded_file1)

if uploaded_file2 is not None:
    st.write("File 2 was uploaded successfully.")
    df2 = _extract_students_from_excel(uploaded_file2)


if not df1.empty and not df2.empty:
    combined_df = combine_dataframes(df1, df2)
    st.write("The dataframes have been combined successfully.")
    st.dataframe(combined_df)  

    
    if st.button("Insert into Database"):
        insert_students_in_bulk(combined_df)  
else:
    st.write("Please upload both Excel files to combine.")

