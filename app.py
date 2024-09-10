import streamlit as st
import pandas as pd

def _extract_students_from_excel(excel_file):
        """Extracts student information from the provided Excel file."""
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            st.write(f"Error reading the Excel file: {e}")
            return []
        st.write(df)


st.title("Upload students attendance list Excel file")

uploaded_file = st.file_uploader("Attendance list Excel file", type=["xls", "xlsx"])

if uploaded_file is not None:
    st.write("file was uploaded successfully.")
    _extract_students_from_excel(uploaded_file)