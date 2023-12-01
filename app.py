import streamlit as st
import pandas as pd
import base64
import openpyxl
import io

def process(df):
    needval_condition = df.duplicated(subset=['Udise', 'Action Item'], keep=False) & (
      df.groupby(['Udise', 'Action Item'])['quantity'].transform('nunique') > 1
    )
    dupli_condition = df.duplicated(subset=['Udise', 'Action Item'], keep=False) & (
        df.groupby(['Udise', 'Action Item'])['quantity'].transform(lambda x: (x == 0)  | (x > 30))) | (df.duplicated(subset=['Udise', 'Action Item', 'quantity'], keep='first')
    )
    dup_zero = df.duplicated(subset=['Udise', 'Action Item']) & (
        df.groupby(['Udise', 'Action Item'])['quantity'].transform(lambda x: all((x == 0)  | (x > 30))))
  
    df['verified'] = [False]*len(df)
    df['need validation'] = [False]*len(df)
    df['isduplicate'] = [False]*len(df)
    df.loc[dupli_condition, 'isduplicate'] = True
    df.loc[dup_zero, 'isduplicate'] = False
  
  
    need_val = []
    for i in df['quantity']:
        if i > 30 or i == 0 :
            need_val.append(True)
        else:
            need_val.append(False)
  
    df['need validation'] = need_val
    df.loc[needval_condition, 'need validation'] = True
    df['verified'] = ''
    df.loc[df['isduplicate'] == False , 'verified'] = True
    df.loc[df['need validation'] == False , 'verified'] = True
    df['System_Status'] = ''
    df.loc[df['verified'] == True , 'System_Status'] = 'Verified'
    df.loc[df['need validation'] == True , 'System_Status'] = 'Need_validation'
    df.loc[df['isduplicate'] == True , 'System_Status'] = 'Duplicate'

    columns_to_drop = ['isduplicate', 'need validation', 'verified']
    df.drop(columns=columns_to_drop)
    return df

st.set_page_config(page_title="Excel Data Processing App", page_icon="📊")

st.header("Excel Data Processing App 📊")
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read the Excel file
        data = pd.read_excel(uploaded_file)

        required_columns = ['Udise', 'Action Item', 'quantity']
        if not all(column in data.columns for column in required_columns):
            st.error(f"The uploaded dataset must contain the following columns: {', '.join(required_columns)}")

        else:
            st.subheader("View Original Data") 
            st.write(data)
            
            df_processed = process(data)
    
            st.subheader("View Processed Data")
            st.write(df_processed)
            
            st.subheader("Download Processed Data")
            excel_buffer = io.BytesIO()
            df_processed.to_excel(excel_buffer, index=False, header=True)
            excel_buffer.seek(0)
            b64 = base64.b64encode(excel_buffer.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="processed_data.xlsx">Click here to download Processed Data</a>'
            st.markdown(href, unsafe_allow_html=True)
        
    except pd.errors.ParserError:
        st.error("The uploaded dataset is not in a valid format.")
        data = none
