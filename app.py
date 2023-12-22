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
    "சுற்றுச்சுவர் பழுதுப்பார்த்தல்",
    "பழுதடைந்த சுற்றுச்சுவரை அகற்றுதல்",
    "புதிய இயற்பியல் ஆய்வகம்",
    "புதிய உடற்கல்வி ஆசிரியர் அறை",
    "புதிய உயர்-தொழிநுட்ப ஆய்வகம்",
    "புதிய உயிரியல் ஆய்வகம்",
    "புதிய கணித ஆய்வகம்",
    "புதிய கணினி ஆய்வகம்",
    "புதிய கலை ஆய்வகம்",
    "புதிய சமையல் அறை",
    "புதிய கலையரங்கம்",
    "புதிய கழிவுநீர்த் தேக்கத் தொட்டி",
    "புதிய சமையலறை",
    "புதிய சுற்றுச் சுவர்",
    "புதிய சேமிப்பு அறை",
    "புதிய சேலபாட்டு அறை",
    "புதிய நிருவாக அலுவலக அறை",
    "புதிய நிலத்தடித் தொட்டி",
    "புதிய நூலகம்",
    "புதிய பதிவறை",
    "புதிய பம்ப் அறை",
    "புதிய பாதுகாப்பாளர் அறை",
    "புதிய வேதியியல் ஆய்வகம்",
    ]

    single_entries = df.groupby(['Udise', 'Action Item']).filter(lambda x: len(x) == 1)

    single_entries_index_zero30 = single_entries[
        (single_entries['quantity'] == 0) |
        (single_entries['quantity'] > 30)
        ].index
    
    df.loc[single_entries_index_zero30, 'System_Status'] = 'Need validation'
    
    single_entries_index_nonlist_verified = single_entries[
        (single_entries['quantity'] > 0) & (single_entries['quantity'] < 30) &  ~single_entries['Action Item'].isin(action_items_list)
    ].index
    
    df.loc[single_entries_index_nonlist_verified, 'System_Status'] = 'Verified'
    
    single_entries_index_inlist_verified = single_entries[
        (single_entries['quantity'] == 1) &  single_entries['Action Item'].isin(action_items_list)
    ].index
    
    df.loc[single_entries_index_inlist_verified, 'System_Status'] = 'Verified'
    
    single_entries_index_inlist_needval = single_entries[
        (single_entries['quantity'] > 1) &  single_entries['Action Item'].isin(action_items_list)
    ].index
    
    df.loc[single_entries_index_inlist_needval, 'System_Status'] = 'Need Validation'

    grouped_entries = df.groupby(['Udise', 'Action Item']).filter(lambda x: len(x) > 1)

    grouped_entries_index_nonlist_verified = grouped_entries[
        (grouped_entries['quantity'] > 0) & (grouped_entries['quantity'] < 30) &  ~grouped_entries['Action Item'].isin(action_items_list)
    ].index
    
    df.loc[grouped_entries_index_nonlist_verified, 'System_Status'] = 'Verified'
    
    grouped_entries_index_inlist_verified = grouped_entries[
        (grouped_entries['quantity'] == 1) &  grouped_entries['Action Item'].isin(action_items_list)
    ].index
    
    df.loc[grouped_entries_index_inlist_verified, 'System_Status'] = 'Verified'
    
    needval_condition = (
        df.duplicated(subset=['Udise', 'Action Item'], keep=False) &
        (df.groupby(['Udise', 'Action Item'])['quantity'].transform('nunique') > 1)
    
    )
    
    df.loc[needval_condition, 'System_Status'] = 'Need validation'
    
    dupli_condition = df.duplicated(subset=['Udise', 'Action Item','quantity'],  keep='first')
    
    df.loc[dupli_condition, 'System_Status'] = 'Duplicate'
    
    grouped_entries_index_inlist_duplicate = grouped_entries[
        (grouped_entries['quantity'] > 1) &  grouped_entries['Action Item'].isin(action_items_list)
    ].index
    
    df.loc[grouped_entries_index_inlist_duplicate, 'System_Status'] = 'Duplicate'
    
    grouped_entries_index_zero30 = grouped_entries[
        (grouped_entries['quantity'] == 0) |
        (grouped_entries['quantity'] > 30)
        ].index
    
    df.loc[grouped_entries_index_zero30, 'System_Status'] = 'Duplicate'
    
    df = df.sort_values(['quantity'])
    def update_status(df, action_item):
        if df.empty:
            return
        mixed_groups = df.groupby(['Udise', 'Action Item'])
    
        for name, group in mixed_groups:
            if name[1] in action_items_list and len(group) > 1:  #name[1] == action_item and
                zero_exists = (group['quantity'] == 0).any()
                greater30_exists = (group['quantity'] > 30).any()
    
                if zero_exists or greater30_exists:
                    non_zero_group = group[group['quantity'] != 0]
                    zero_group = group[group['quantity'] == 0]
    
                    if not non_zero_group.empty:
                        min_quantity_index = non_zero_group['quantity'].idxmin()
                        if df.loc[min_quantity_index, 'quantity'] > 1:
                            #print("nozer",min_quantity_index)
                            df.loc[min_quantity_index, 'System_Status'] = 'Need validation'
                        elif df.loc[min_quantity_index, 'quantity'] == 1:
                          #print("one",min_quantity_index)
                          df.loc[min_quantity_index, 'System_Status'] = 'Verified'
    
            if name[1] not in action_items_list and ((group['quantity'] == 0).all() or (group['quantity'] > 30).all()):
                    if not group.empty  :
                        min_quantity_index = group['quantity'].idxmin()
                        # print("what?")
                        if df.loc[min_quantity_index, 'quantity'] > 1:
                            # print("nozer",min_quantity_index)
                            df.loc[min_quantity_index, 'System_Status'] = 'Need validation'
    
            #if name[1] in action_items_list and len(group) > 1 and (group['quantity'] == 1).sum() == 1 and (group['quantity'] != 0).any() and (group['quantity'] < 30).any() :
            #  qualifying_rows = group[group['quantity'] == 1]
            #  if not qualifying_rows.empty:
            #        index_with_one = qualifying_rows.index[0]
            #        print("one 1", index_with_one)
            #        df.loc[index_with_one, 'System_Status'] = 'Need validation'
    
            if name[1] not in action_items_list and len(group) > 1 and (group['quantity'] > 1).any() and ((group['quantity'] == 0).any() or (group['quantity'] > 30).any()) :
              qualifying_rows = group[(group['quantity'] > 1)]
              unique_values_in_range = group[(group['quantity'] >= 0) & (group['quantity'] <= 30)]['quantity'].drop_duplicates().tolist()
              if not len(unique_values_in_range) == 0:
    
                            unique_value_index = group[(group['quantity'] >= 0) & (group['quantity'] <= 30) & (group['quantity'].isin(unique_values_in_range))].index[0]
                            if len(unique_values_in_range) == 1:
    
                                # print("veri",unique_value_index)
                                df.loc[unique_value_index, 'System_Status'] = 'Verified'
                    #if ( ((group['quantity'] > 0) & (group['quantity'] < 30)).sum() == 1):
                    #  filtered_group = group[(group['quantity'] > 0) & (group['quantity'] < 30)]
                    ##  if not filtered_group.empty and len(filtered_group) == 1:
                    #      index_value = filtered_group.index[0]
                    #      print("veri man:",index_with_more_one )
                    #      df.loc[index_with_more_one, 'System_Status'] = 'Verified'
                        #index_with_more_one = group[(group['quantity'] > 1) & (group['quantity'] != 0) & (group['quantity'] > 30)].index[0]
                        #print("ver man", index_with_more_one)
                        #df.loc[index_with_more_one, 'System_Status'] = 'Verified'
    
    # Assuming action_items_list is defined somewhere
    for action_item in action_items_list:
        update_status(df, action_item)
    
    # Filter groups where there's a mix of values within range [0, 30] along with zero
    mixed_value_groups = df.groupby(['Udise', 'Action Item']).filter(
        lambda group: ((group['quantity'].between(0, 31)).sum() > 0) and (group['quantity'].isin([0, 30])).any()
    )
    
    # Iterate through these groups to identify unique values within the range [1, 30] and mark them as 'Verified'
    for group_index, group in mixed_value_groups.groupby(['Udise', 'Action Item']):
        unique_values_in_range = group.loc[group['quantity'].between(0,31), 'quantity'].drop_duplicates()
        if len(unique_values_in_range) == 1:
            unique_value_index = unique_values_in_range.index[0]
            #print(unique_values_in_range)
            df.loc[unique_value_index, 'System_Status'] = 'Verified'

    # Filter groups where all values consist of 0 and values greater than 30
    special_groups = df.groupby(['Udise', 'Action Item']).filter(
        lambda group: (group['quantity'].eq(0) | group['quantity'].gt(30)).all()
    )
    
    # Iterate through these groups and mark them as 'Special'
    for group_index, group in special_groups.groupby(['Udise', 'Action Item']):
        first_index = group.index[0]
        #print(first_index)
        df.loc[first_index, 'System_Status'] = 'Need validation'

    same_value_groups = df.groupby(['Udise', 'Action Item'])['quantity'].transform(lambda group: group.nunique() == 1)

    # Iterate through these groups and mark the first index in each group as 'Need validation'
    for group_index, group in df[same_value_groups].groupby(['Udise', 'Action Item']):
        action_item_value = group['Action Item'].iloc[0]
    
        if action_item_value in action_items_list and ~(group['quantity'] == 1).any():
            first_index = group.index[0]
            df.loc[first_index, 'System_Status'] = 'Need validation'
        # elif action_item_value not in action_items_list:
        #     first_index = group.index[0]
        #     df.loc[first_index, 'System_Status'] = 'Need validation'
    
    return df

st.set_page_config(page_title="Excel Data Processing App", page_icon="📊")

st.title("Excel Data Processing App 📊")
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

page = st.sidebar.radio("**Select a Page**",["Algorithm with Enhancement based on Action Item", "Algorithm without Enhancement"])

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
