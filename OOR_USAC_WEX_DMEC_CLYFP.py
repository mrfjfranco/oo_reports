import pandas as pd
import os
from datetime import datetime
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

# Define input and output directories
input_dir = 'input'
output_dir = 'output'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Find the first CSV file in the input directory
csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
if not csv_files:
    print("No CSV files found in the input directory.")
    exit()
csv_file_path = os.path.join(input_dir, csv_files[0])

try:
    # Load the data without parsing dates initially
    df = pd.read_csv(csv_file_path)

    # Save the original date formats
    original_dates = df[['ORDERDATE', 'DELIVERYDATE', 'ESTIMATEDSHIPDATE', 'BSW', 'ESW']].copy()

    # Convert date columns to datetime format for processing
    date_columns = ['ORDERDATE', 'DELIVERYDATE', 'ESTIMATEDSHIPDATE', 'BSW', 'ESW']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], format='%m/%d/%y', errors='coerce')

except FileNotFoundError:
    print(f"File not found: {csv_file_path}")
    exit()

# Apply USAC criteria
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

# Format date columns back to mm/dd/yy for USAC
for col in date_columns:
    combined_criteria_usac[col] = original_dates[col]

# Apply WEX criteria
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

criteria4_wex = df[
    (df['TFWAREHOUSE'].str.strip() == 'EX_IO') &
    (df['ITEMCLASS'].str.strip() == 'SIM Card') &
    (df['ITEM'].str.contains('KT', case=False, na=False)) &
    (~df['ITEM'].str.startswith('GP', na=False)) &
    (~df['ITEM'].str.startswith('SL', na=False))
]

criteria5_wex = df[
    (df['TFWAREHOUSE'].str.strip() == 'EX_IO') &
    (df['ITEMCLASS'].str.strip() == 'SIM Card') &
    (df['ITEM'].str.contains('sim', case=False, na=False))
]

combined_criteria_wex = pd.concat([criteria1_wex, criteria2_wex, criteria3_wex, criteria4_wex, criteria5_wex])

# Format date columns back to mm/dd/yy for WEX
for col in date_columns:
    combined_criteria_wex[col] = original_dates[col]

# Apply DMEC criteria
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


# Apply CLFY criteria
criteria_clfy = df[
    (df['TFWAREHOUSE'].str.strip() == 'DP_IO') &
    (df['ITEM'].str.strip() == 'SMMTXT2311DCYTP') &
    (df['STATE'].str.strip() == 'CA')
]

# Get current date for filenames
current_date = datetime.now().strftime('%m-%d-%y')

# Function to save dataframe to excel
def save_to_excel(dataframe, filename):
    filepath = os.path.join(output_dir, filename)
    if os.path.exists(filepath):
        os.remove(filepath)  # Remove the file if it already exists
    dataframe.to_excel(filepath, index=False)
    print(f"{filename} contains {len(dataframe)} orders")

# Filter and save files for USAC


file1_usac = combined_criteria_usac[combined_criteria_usac['STATUS'] == 'OPEN']
save_to_excel(file1_usac, f'USAC Daily Open Orders {current_date}.xlsx')

file2_usac = combined_criteria_usac[combined_criteria_usac['STATUS'] == 'BKO']
save_to_excel(file2_usac, f'USAC BKO {current_date}.xlsx')

file3_usac = combined_criteria_usac[combined_criteria_usac['STATUS'].isin(['OPEN', 'BKO'])]
save_to_excel(file3_usac, f'USAC All Orders {current_date}.xlsx')

# Filter and save files for WEX
file1_wex = combined_criteria_wex[combined_criteria_wex['STATUS'] == 'OPEN']
save_to_excel(file1_wex, f'WEX Daily Open Orders {current_date}.xlsx')

file2_wex = combined_criteria_wex[combined_criteria_wex['STATUS'] == 'BKO']
save_to_excel(file2_wex, f'WEX BKO {current_date}.xlsx')

file3_wex = combined_criteria_wex[combined_criteria_wex['STATUS'].isin(['OPEN', 'BKO', 'HOLD'])]
save_to_excel(file3_wex, f'WEX All Orders {current_date}.xlsx')

# Filter and save files for DMEC
file1_dmec = combined_criteria_dmec[combined_criteria_dmec['STATUS'] == 'OPEN'].drop(columns=['UniqueFlag'])
save_to_excel(file1_dmec, f'DMEC Daily Open Orders {current_date}.xlsx')

file2_dmec = combined_criteria_dmec[combined_criteria_dmec['STATUS'] == 'BKO'].drop(columns=['UniqueFlag'])
save_to_excel(file2_dmec, f'DMEC BKO {current_date}.xlsx')

file3_dmec = combined_criteria_dmec[combined_criteria_dmec['STATUS'].isin(['OPEN', 'BKO', 'HOLD'])]
save_to_excel(file3_dmec, f'DMEC All Orders {current_date}.xlsx')

# Filter and save files for CLFYP
file1_clfy = criteria_clfy[criteria_clfy['STATUS'] == 'OPEN']
save_to_excel(file1_clfy, f'CLFY Daily Open Orders {current_date}.xlsx')

file2_clfy = criteria_clfy[criteria_clfy['STATUS'] == 'BKO']
save_to_excel(file2_clfy, f'CLFY BKO {current_date}.xlsx')

file3_clfy = criteria_clfy[criteria_clfy['STATUS'].isin(['OPEN', 'BKO'])]
save_to_excel(file3_clfy, f'CLFY All Orders {current_date}.xlsx')




print("Files have been created successfully in the output folder.")
