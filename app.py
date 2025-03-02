# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO, StringIO  # Corrected import

# Set up app
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform your file between CSV and Excel formats with built-in cleaning and visualization!")

# Upload files
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the uploaded file
        if file_ext == ".csv":
            df = pd.read_csv(file)

        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")

        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file details
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show first 5 rows
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df = df.drop_duplicates()  # Corrected inplace issue
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        # Select Columns to Convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("Data Visualizations")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File Conversion
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):

            # ✅ Correct buffer initialization
            if conversion_type == "CSV":
                buffer = StringIO()
                df.to_csv(buffer, index=False)
                data = buffer.getvalue()
                filename = file.name.replace(file_ext, ".csv")
                minetype = "text/csv"

            elif conversion_type == "Excel":
                buffer = BytesIO()
                df.to_excel(buffer, index=False, engine="openpyxl")
                buffer.seek(0)  # Reset buffer
                data = buffer
                filename = file.name.replace(file_ext, ".xlsx")
                minetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            # ✅ Streamlit Download Button (Fixed binary data issue)
            st.download_button(
                label=f"Download {filename}",
                data=data,
                file_name=filename,
                mime=minetype
            )

st.success("All files processed successfully! ✅")

