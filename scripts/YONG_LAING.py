import openpyxl
from openpyxl.utils import get_column_letter
import xlrd
import os

def convert_xls_to_xlsx(xls_filename, xlsx_filename):
    """
    Converts an XLS file to XLSX format.
    Args:
        xls_filename (str): The path to the XLS file.
        xlsx_filename (str): The path where the XLSX file will be saved.
    """
    try:
        workbook = xlrd.open_workbook(xls_filename)
        wb = openpyxl.Workbook()
        for sheet_name in workbook.sheet_names():
            sheet = workbook.sheet_by_name(sheet_name)
            new_sheet = wb.create_sheet(title=sheet_name)
            for row in range(sheet.nrows):
                for col in range(sheet.ncols):
                    cell_value = sheet.cell_value(row, col)
                    new_sheet.cell(row=row + 1, column=col + 1, value=cell_value)
        # Remove the default sheet if it's still present
        if "Sheet" in wb.sheetnames:
            default_sheet = wb["Sheet"]
            wb.remove(default_sheet)
        wb.save(xlsx_filename)
        print(f"Successfully converted '{xls_filename}' to '{xlsx_filename}'")
    except Exception as e:
        print(f"Error converting XLS to XLSX: {e}")
        return False
    return True

def organize_data(filename):
    """
    Organizes data from 'INVOICE' sheet in an Excel file
    and writes the organized data to a new Excel file.

    Args:
    filename (str): The path to the Excel file containing 'INVOICE' sheet.
    """
    try:
        # Load the workbook
        wb = openpyxl.load_workbook(filename)

        # Get the main sheet ('INVOICE')
        if "INVOICE" not in wb.sheetnames:
            print("Sheet named 'INVOICE' not found. Please make sure it exists.")
            return
        sheet = wb["INVOICE"]

        # Create a new workbook for the organized sheet
        output_wb = openpyxl.Workbook()
        organized_sheet = output_wb.active
        organized_sheet.title = 'Organized'

        # Initialize variables
        case_1 = False
        case_2 = False
        j = 1
        i = 0

        # Loop through the rows in column A using index i
        while i <= sheet.max_row:
            i += 1
            po_number = sheet.cell(row=i, column=1).value
            desc = sheet.cell(row=i, column=2).value

            if case_1:
                if case_2:
                    if not desc:
                        break
                elif desc == 'Made In China':
                    case_2 = True
                    continue
                elif desc == 'TOTAL: ':
                    break
                elif not desc:
                    continue
            elif po_number == 'PO Number ':
                case_1 = True
                i += 1
                continue
            else:
                continue

            if not case_2:
                # Case 1: PO Number and Description
                parts = sheet.cell(row=i, column=3).value
                wo = sheet.cell(row=i, column=4).value
                brand = sheet.cell(row=i, column=5).value
                qty = sheet.cell(row=i, column=6).value
                unit_price = sheet.cell(row=i, column=7).value

                organized_sheet.cell(row=j, column=1, value=f'PO Number {po_number}')
                organized_sheet.cell(row=j, column=2, value=desc)
                organized_sheet.cell(row=j, column=3, value=f'PARTS  NO.{parts}')
                organized_sheet.cell(row=j, column=4, value=wo)
                organized_sheet.cell(row=j, column=5, value=brand)
                organized_sheet.cell(row=j, column=6, value=qty)
                organized_sheet.cell(row=j, column=7, value=unit_price)
                organized_sheet.cell(row=j, column=8, value='8523.51.00.00-0')
                organized_sheet.cell(row=j, column=9, value='06')
            
            else:
                # Case 2: Made In China
                parts = sheet.cell(row=i, column=3).value
                brand = sheet.cell(row=i, column=5).value
                qty = sheet.cell(row=i, column=6).value
                unit_price = sheet.cell(row=i, column=7).value

                organized_sheet.cell(row=j, column=2, value=desc)
                organized_sheet.cell(row=j, column=3, value=f'PARTS  NO.{parts}')
                organized_sheet.cell(row=j, column=5, value='NO BRAND')
                organized_sheet.cell(row=j, column=6, value=qty)
                organized_sheet.cell(row=j, column=7, value=unit_price)
                organized_sheet.cell(row=j, column=8, value='8523.51.00.00-0')
                organized_sheet.cell(row=j, column=9, value='82')

            qty_cell = organized_sheet.cell(row=j, column=6, value=qty)
            if isinstance(qty, (int, float)):
                qty_cell.number_format = '#,##0'
            
            unit_price_cell = organized_sheet.cell(row=j, column=7, value=unit_price)
            if isinstance(unit_price, (int, float)):
                unit_price_cell.number_format = '#,##0.0000'

            # Adjust column widths
            for col in range(1, 10):
                max_length = 0
                column = get_column_letter(col)
                for cell in organized_sheet[column]:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                organized_sheet.column_dimensions[column].width = adjusted_width

            j += 1

        # Save the organized data to a new file in the 'uploads' folder
        output_filename = os.path.join("uploads", "Organized_Data.xlsx")
        output_wb.save(output_filename)
        print(f"Organized data saved to '{output_filename}'")

    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")