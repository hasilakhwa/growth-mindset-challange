#Imports
from fileinput import filename
from typing_extensions import Buffer
import streamlit as st # type: ignore
import pandas as pd # type: ignore
import os
from io import BytesIO



#set up our app
st.set_page_config(page_title="Data sweeper", layout="wide")
st.title("Data sweeper")
st.write("Transform your file between CSV and Exel formats with built-in cleaning and visualization!") 

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
            

        elif file_ext == ".xlsx":
            df = pd.read_excel(file)

        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
                    
        

        #Display info about the file
        st.write(f"**File name:** {file.name}")
        st.write(f"**File size:** {file.size/1024} ")


        #Show 5 rows of our df
        st.write("preview the Head of the Dataframe")
        st.dataframe(df.head())

        #Option for data cleaning
        st.subheader("Data cleaning Options")
        if st.checkbox("Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df = df.drop_duplicates(inplace = True)
                    st.write("duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("missing values have been filled!")

        #Choose Specific Columns to Keep or Convert
        st.subheader("select columns to convert")
        columns = st.multiselect(f"Choose Columns for {file.name}",df.columns, default = df.columns)
        df = df[columns]


        #create some Visualizations
        st.subheader("Data Visualizations")
        if st.checkbox(f"Show visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

           

        

         # Convert the file -> CSV to Excel
        st.subheader("Conversion options")
        conversion_type = st.radio(f"convert {file.name} to:", ["CSV", "Excel"],key=file.name) 
        if st.button(f"Convert {file.name}"):
            if conversion_type == "CSV": 
                df.to_csv(Buffer, index=False)
                filename = file.name.replace(file_ext, ".csv")
                minetype = "text/csv"





            elif conversion_type == "Excel":
                df.to_excel(Buffer, index=False)
                filename = file.name.replace(file_ext, ".xlsx")
                minetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            Buffer.seek(0)


            #Download Button
            st.download_button(
                label = f"Download {filename} as {conversion_type}",
                data = Buffer,
                file_name = filename,
                mime = minetype
            )

                

st.success("All files processed successfully!")       
