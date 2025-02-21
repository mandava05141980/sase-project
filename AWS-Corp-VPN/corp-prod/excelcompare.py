import pandas as pd

def compare_excel_csv(file_excel, file_csv):
    # Read specific columns from Excel sheet and CSV file into Pandas DataFrames
    cols_excel = ['account_id', 'ip', 'vpc']
    cols_csv = ['name', 'cidr', 'account_id']
    df_excel = pd.read_excel(file_excel, usecols=cols_excel)
    df_csv = pd.read_csv(file_csv, usecols=cols_csv)

    # Find rows that are in one sheet but not the other
    not_in_csv = df_excel[~df_excel.isin(df_csv)].dropna()
    not_in_excel = df_csv[~df_csv.isin(df_excel)].dropna()

    return not_in_csv, not_in_excel

if __name__ == "__main__":
    file_excel = r"C:\Lakshmi\Autodesk\KT\Python\Autodesk-Projects\sase-project\AWS-Corp-VPN\corp-prod\Divvycloud.xlsx"  # Path to the Excel file
    file_csv = r"C:\Lakshmi\Autodesk\KT\Python\Autodesk-Projects\sase-project\AWS-Corp-VPN\corp-prod\privatenetwork.csv"  # Path to the CSV file

    not_in_csv, not_in_excel = compare_excel_csv(file_excel, file_csv)

    print("Rows in Excel sheet but not in CSV file:")
    print(not_in_csv)

    print("\nRows in CSV file but not in Excel sheet:")
    print(not_in_excel)
