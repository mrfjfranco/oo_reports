import pandas as pd
import os
from datetime import datetime
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

# Define input and output directories using dynamic paths
base_dir = os.path.dirname(__file__)  # Get the directory of the current script
input_dir = os.path.join(base_dir, 'input')
output_dir = os.path.join(base_dir, 'output', 'oor')

# Ensure the input and output directories exist
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Function to load and process CSV data
def load_data():
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the input directory.")
        return None
    csv_file_path = os.path.join(input_dir, csv_files[0])
    
    try:
        # Load the data
        df = pd.read_csv(csv_file_path)
        original_dates = df[['ORDERDATE', 'DELIVERYDATE', 'ESTIMATEDSHIPDATE', 'BSW', 'ESW']].copy()

        # Convert date columns
        date_columns = ['ORDERDATE', 'DELIVERYDATE', 'ESTIMATEDSHIPDATE', 'BSW', 'ESW']
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], format='%m/%d/%y', errors='coerce')

        return df, original_dates, date_columns
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        return None

# Function to save DataFrame to Excel
def save_to_excel(dataframe, filename):
    filepath = os.path.join(output_dir, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    dataframe.to_excel(filepath, index=False)
    return f"{filename} contains {len(dataframe)} orders"

# Get current date for filenames
current_date = datetime.now().strftime('%m-%d-%y')

# Define criteria functions for different channels

# USAC Criteria
def USAC(df, original_dates, date_columns):
    criteria1_usac = df[
        (df['TFWAREHOUSE'].str.strip() == 'EX_IO') &
        (df['ITEMCLASS'].str.strip() == 'PHONE') &
        (df['ITEM'].str.contains('LL', case=False, na=False)) &
        (~df['ITEM'].str.contains('LLE', case=False, na=False))
    ]
    criteria2_usac = df[
        (df['TFWAREHOUSE'].str.strip() == 'EX_IO') &
        (df['ITEMCLASS'].str.strip() == 'SIM Card') &
        (df['ITEM'].str.contains('KT', case=False, na=False))
    ]
    combined_criteria_usac = pd.concat([criteria1_usac, criteria2_usac])

    # Restore the original date formats
    for col in date_columns:
        combined_criteria_usac[col] = original_dates[col]
    return combined_criteria_usac

# WEX Criteria
def WEX(df, original_dates, date_columns):
    criteria1_wex = df[
        (df['TFWAREHOUSE'].str.strip() == 'EX_IO') &
        (df['ITEMCLASS'].str.strip() == 'PHONE') &
        (~df['ITEM'].str.contains('LL', case=False, na=False))
    ]
    criteria2_wex = df[
        (df['TFWAREHOUSE'].str.strip() == 'EX_IO') &
        (df['ITEMCLASS'].str.strip() == 'PHONE') &
        (df['ITEM'].str.contains('LLE', case=False, na=False))
    ]
    criteria3_wex = df[
        (df['TFWAREHOUSE'].str.strip() == 'EX_IO') &
        (df['ITEMCLASS'].str.strip() != 'PHONE') &
        (df['ITEMCLASS'].str.strip() != 'SIM Card')
    ]
    combined_criteria_wex = pd.concat([criteria1_wex, criteria2_wex, criteria3_wex])

    for col in date_columns:
        combined_criteria_wex[col] = original_dates[col]
    return combined_criteria_wex

# DMEC Criteria
def DMEC(df, original_dates, date_columns):
    criteria1_dmec = df[
        (df['TFWAREHOUSE'].str.strip() == 'DMC_IO') &
        (df['ITEMCLASS'].str.strip() == 'PHONE')
    ]
    criteria2_dmec = df[
        (df['TFWAREHOUSE'].str.strip() == 'DMC_IO') &
        (df['ITEMCLASS'].str.strip() == 'Component') &
        (~df['ITEM'].str.contains('FLY', case=False, na=False))
    ]
    criteria3_dmec = df[
        (df['TFWAREHOUSE'].str.strip() == 'DMC_IO') &
        (df['ITEMCLASS'].str.strip() == 'SIM Card')
    ]
    combined_criteria_dmec = pd.concat([criteria1_dmec, criteria2_dmec, criteria3_dmec])

    # Add a helper column to flag unique ORDERNUMBERs (only for DMEC All Orders file)
    combined_criteria_dmec['UniqueFlag'] = combined_criteria_dmec.groupby('ORDERNUMBER').cumcount().apply(lambda x: 1 if x == 0 else 0)

    # Restore original date formats for DMEC
    for col in date_columns:
        combined_criteria_dmec[col] = original_dates[col]

    return combined_criteria_dmec

# CLFYP Criteria
def CLFYP(df, original_dates, date_columns):
    criteria_clfyp = df[
        (df['TFWAREHOUSE'].str.strip() == 'DP_IO') &
        (df['ITEM'].str.strip() == 'SMMTXT2311DCYTP') &
        (df['STATE'].str.strip() == 'CA')
    ]
    return criteria_clfyp

# Generalized report generation function
def generate_report(channel_criteria_func, report_type):
    data = load_data()
    if data is None:
        return
    df, original_dates, date_columns = data

    # Apply channel-specific criteria
    combined_criteria = channel_criteria_func(df, original_dates, date_columns)

    if report_type == "Open Orders":
        report_data = combined_criteria[combined_criteria['STATUS'] == 'OPEN']
    elif report_type == "BKO":
        report_data = combined_criteria[combined_criteria['STATUS'] == 'BKO']
    elif report_type == "All Orders":
        report_data = combined_criteria[combined_criteria['STATUS'].isin(['OPEN', 'BKO'])]
    else:
        return "Invalid report type selected."
        

    # Save the report to Excel
    filename = f'{channel_criteria_func.__name__} {report_type} {current_date}.xlsx'
    save_to_excel(report_data, filename)
    
    # Return the result string for the display
    return f"{filename} contains {len(report_data)} orders"

# Generate all reports for all channels
def generate_all_reports(report_type):
    result_usac = generate_report(USAC, report_type)
    result_wex =generate_report(WEX, report_type)
    result_dmec =generate_report(DMEC, report_type)
    result_clfyp =generate_report(CLFYP, report_type)
    
    # Combine all results and return
    return "\n".join([result_usac, result_wex, result_dmec, result_clfyp])
