import streamlit as st
import pandas as pd
import base64
import openpyxl
import io

@st.cache_resource
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
    new_df = df.drop(columns=columns_to_drop)
    return new_df

@st.cache_resource
def enhanced_process(df):
    action_items_list =  [
    'சுவரில் நீர் ஒழுகுதல் பழுதுப்பார்த்தல்',
    'சுற்றுச்சுவர் பழுதுப்பார்த்தல்',
    'தரை சீரமைப்பு செய்தல்',
    'தரைத் தள ஓடு பதித்தல்',
    'பட்டி பார்த்தல்',
    'பழுதடைந்த சுற்றுச்சுவரை அகற்றுதல்',
    'பழுதுப்பார்த்தல்',
    'புதிய இயற்பியல் ஆய்வகம்',
    'புதிய உடற்கல்வி ஆசிரியர்அறை',
    'புதிய உயர்-தொழிநுட்ப ஆய்வகம்',
    'புதிய உயிரியல் ஆய்வகம்',
    'புதிய ஒருங்கிணைந்த அறிவியல் ஆய்வகம்',
    'புதிய கணித ஆய்வகம்',
    'புதிய கணினி ஆய்வகம்',
    'புதிய கலை ஆய்வகம்',
    'புதிய கலையரங்கம்',
    'புதிய கழிவுநீர்த் தேக்கத் தொட்டி',
    'புதிய சமையலறை',
    'புதிய சமையல் அறை',
    'புதிய சுற்றுச் சுவர்',
    'புதிய சேமிப்பு அறை',
    'புதிய சேலபாட்டு அறை',
    'புதிய நிருவாக அலுவலக அறை',
    'புதிய நிலத்தடித் தொட்டி',
    'புதிய நூலகம்',
    'புதிய பதிவறை',
    'புதிய பம்ப் அறை',
    'புதிய பாதுகாப்பாளர் அறை',
    'புதிய வேதியியல் ஆய்வகம்',
    'மேற்கூரை பூசுதல்',
    'மேற்பூசசு பூசுதல்'
    ]

    needval_condition = df.duplicated(subset=['Udise', 'Action Item'], keep=False) & (
    df.groupby(['Udise', 'Action Item'])['quantity'].transform('nunique') > 1
    )
    dupli_condition = df.duplicated(subset=['Udise', 'Action Item'], keep=False) & (
        df.groupby(['Udise', 'Action Item'])['quantity'].transform(lambda x: (x == 0)  | (x > 30))) | (df.duplicated(subset=['Udise', 'Action Item', 'quantity'], keep='first')
    )
    dup_zero = df.duplicated(subset=['Udise', 'Action Item']) & (
        df.groupby(['Udise', 'Action Item'])['quantity'].transform(lambda x: all((x == 0)  | (x > 30))))
    
    veri_one = df.duplicated(subset=['Udise', 'Action Item']) & (
        df.groupby(['Udise', 'Action Item'])['quantity'].transform(lambda x: (x == 1))) & (
        df.groupby(['Udise', 'Action Item'])['Action Item'].transform(lambda x: x.isin(action_items_list)))
    
    veri_many = df.duplicated(subset=['Udise', 'Action Item']) & (
        df.groupby(['Udise', 'Action Item'])['quantity'].transform(lambda x: (x > 1))) & (
        df.groupby(['Udise', 'Action Item'])['Action Item'].transform(lambda x: x.isin(action_items_list)))
    
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
    
    df.loc[veri_one, 'verified'] = True
    df.loc[veri_one, 'need validation'] = False
    
    df.loc[veri_many, 'verified'] = False
    df.loc[veri_many, 'need validation'] = True
    
    df['System_Status'] = ''
    df.loc[df['verified'] == True , 'System_Status'] = 'Verified'
    df.loc[df['need validation'] == True , 'System_Status'] = 'Need_validation'
    df.loc[df['isduplicate'] == True , 'System_Status'] = 'Duplicate'

    def create_duplicates(df, action_item, index):
        return (
            df.duplicated(subset=['Udise', 'Action Item']) & (
                df.groupby(['Udise', 'Action Item', 'quantity'])['quantity'].transform(lambda x: (x != 0) & (x > 1)) & (
                    df.groupby(['Udise'])['Action Item'].transform(lambda x: x == action_item)
                )
            )
        )
    
    df = df.sort_values(by = 'quantity')
    for i, action_item in enumerate(action_items_list, start=1):
        dup_var = f"dup_{i}"
        dup_condition = create_duplicates(df, action_item, i)
        df.loc[dup_condition, 'System_Status'] = 'Duplicate'

    def update_status(df, action_item):
        mixed_groups = df.groupby(['Udise', 'Action Item'])

        for name, group in mixed_groups:
            if name[1] == action_item:
                zero_exists = (group['quantity'] == 0).any()
                ten_exists = (group['quantity'] > 1).any()
    
                if zero_exists and ten_exists:
                    zero_idx = group[group['quantity'] == 0].index
                    df.loc[zero_idx, 'System_Status'] = 'Need_validation'

    for action_item in action_items_list:
        update_status(df, action_item)

    # Find single entries for each Udise-Action Item combination
    single_entries = df.groupby(['Udise', 'Action Item']).filter(lambda x: len(x) == 1)
    
    # Locate the index of those single entries with 'Verified' status and quantity greater than 1
    single_entries_index = single_entries[
        (single_entries['System_Status'] == 'Verified') &
        (single_entries['quantity'] > 1) & (single_entries['quantity'] != 0)
    ].index
    
    # Update the 'System_Status' for those single entries to 'Need_validation'
    df.loc[single_entries_index, 'System_Status'] = 'Need_validation'

    columns_to_drop = ['isduplicate', 'need validation', 'verified']
    new_df = df.drop(columns=columns_to_drop)
    return new_df

st.set_page_config(page_title="Excel Data Processing App", page_icon="📊")

st.title("Excel Data Processing App 📊")
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

page = st.sidebar.radio("**Select a Page**",["Algorithm without Enhancement", "Algorithm with Enhancement based on Action Item"])

if page == "Algorithm without Enhancement":

    st.header("Algorithm without Enhancement")

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
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="processed_data_without_enhancement.xlsx">Click here to download Processed Data</a>'
                st.markdown(href, unsafe_allow_html=True)
            
        except pd.errors.ParserError:
            st.error("The uploaded dataset is not in a valid format.")
            data = none

elif page == "Algorithm with Enhancement based on Action Item":

    st.header("Algorithm with Enhancement based on Action Item")

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
                
                df_processed = enhanced_process(data)
        
                st.subheader("View Processed Data")
                st.write(df_processed)
                
                st.subheader("Download Processed Data")
                excel_buffer = io.BytesIO()
                df_processed.to_excel(excel_buffer, index=False, header=True)
                excel_buffer.seek(0)
                b64 = base64.b64encode(excel_buffer.read()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="processed_data_with_enhancement.xlsx">Click here to download Processed Data</a>'
                st.markdown(href, unsafe_allow_html=True)
            
        except pd.errors.ParserError:
            st.error("The uploaded dataset is not in a valid format.")
            data = none
