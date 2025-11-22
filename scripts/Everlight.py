import tabula
import pandas as pd
import os

def organize_data(filepath):
    # Read PDF into a list of DataFrame
    # This will extract all tables from the PDF
    tables = tabula.read_pdf(filepath, pages='all', multiple_tables=True)

    # Check if any tables were found
    if tables:
        print(f"Found {len(tables)} tables.")
        # For simplicity, we process only the first table found.
        df = tables[0]

        # Clean column names
        df.columns = df.columns.str.replace('\r', '', regex=False)
        
        # remove the , in the QTY(EA) column
        df['QTY(EA)'] = df['QTY(EA)'].str.replace(',', '', regex=False)

        processed_df = pd.DataFrame({
            'Part Number': df['EVERLIGHTP/N'],
            'P.O. Number': 'P.O.NO.' + df['PO'],
            'Quantity': df['QTY(EA)'],
            'Unit': 'EAC',
            'Price': df['KPCS PRICE'],
            'Brand': 'EVERLIGHT',
            'HS Code': df['稅則'],
            'Country Code': '0' + df['統計方式'].astype(str)
        })

        # Format 'Quantity' column with thousands separator
        processed_df['Quantity'] = pd.to_numeric(processed_df['Quantity'], errors='coerce').fillna(0).astype(int)
        processed_df['Quantity'] = processed_df['Quantity'].apply(lambda x: f"{x:,}")

        # Format 'Price' column to two decimal places
        processed_df['Price'] = pd.to_numeric(processed_df['Price'], errors='coerce').fillna(0)
        processed_df['Price'] = processed_df['Price'].apply(lambda x: f"{x:.2f}")

        # Convert 'HS Code' to string to ensure it's treated as text in Excel
        processed_df['HS Code'] = processed_df['HS Code'].astype(str)

        # Save to XLSX without header and with specified sheet name
        xlsx_output_path = 'uploads/Organized_Data.xlsx'
        processed_df.to_excel(xlsx_output_path, index=False, header=False, sheet_name='Organized')

        # Auto-adjust columns' width
        from openpyxl import load_workbook
        workbook = load_workbook(xlsx_output_path)
        worksheet = workbook['Organized']
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter # Get the column letter
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column].width = adjusted_width
        
        workbook.save(xlsx_output_path)

        print(f"--- Processed data saved to {xlsx_output_path} ---")

    else:
        print("No tables found in the PDF.")
        return None
