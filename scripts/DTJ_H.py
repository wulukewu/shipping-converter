import openpyxl
from openpyxl.utils import get_column_letter
import re
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

def organize_data_hm(filename):
    """
    Organizes data from 'HM' sheet in an Excel file and writes the organized data to a new Excel file.
    Args:
        filename (str): The path to the Excel file containing the 'HM' sheet.
    """
    try:
        # Load the workbook
        wb = openpyxl.load_workbook(filename)
        # Get the HM sheet
        if "HM" not in wb.sheetnames:
            print("Sheet named 'HM' not found. Please make sure it exists.")
            return
        hm_sheet = wb["HM"]
        # Create a new workbook for the organized sheet
        organized_wb = openpyxl.Workbook()
        org_sheet = organized_wb.active
        org_sheet.title = "Organized"
        # Find the last row of the HM sheet
        last_row = hm_sheet.max_row
        # Initialize flags
        found_start = False
        found_end = False
        start_row = 0
        end_row = 0
        # Loop through column A to find start and end points
        for i in range(1, last_row + 1):
             cell_value = hm_sheet.cell(row=i, column=1).value
             if not found_start:
                 if cell_value and "DESCRIPTION OF GOODS" in cell_value.upper():
                    start_row = i + 1
                    found_start = True
             elif not found_end:
                if cell_value and "PACKING AND WEIGHT LIST" in cell_value.upper():
                     end_row = i - 1
                     found_end = True
                     break
        # Check if we found both the start and end markers
        if not found_start or not found_end:
            print("Could not find start or end markers")
            return
        # Initialize j for the organized sheet row
        j = 1
        # Initialize the minUnitprice to a very high number
        min_unit_price = float('inf')
        # Skip the first row from start
        start_row += 1
        # Loop through the rows between the start and end rows in HM sheet
        for i in range(start_row, end_row + 1):
            # Get data from goods
            desc = hm_sheet.cell(row=i, column=1).value
            unit_price = hm_sheet.cell(row=i, column=6).value
            qty = hm_sheet.cell(row=i, column=7).value
            kind = hm_sheet.cell(row=i, column=10).value
            # Check if desc is blank, if it is, skip to the next iteration
            if not desc or str(desc).strip() == "":
                continue
            if desc and "free sample" in str(desc).lower():
                # The 'desc' variable contains "free sample" (case-insensitive).
                # Case 2 - free sample set
                kinds_combined = ""  # Renamed variable
                # Calculate the min price
                # Check if the min price is still the default, in that case, set it to 0
                if min_unit_price == float('inf'):
                    min_unit_price = 0
                sub_kind_count = 0
                if 'kinds' in locals() and isinstance(kinds, list) and len(kinds) > 0:
                  #Case 2-1 when kinds has more than 1 element
                  for k in range(len(kinds)):
                    # Check for "xN" multiplier in sub-kind
                    sub_kind_without_multiplier = kinds[k]
                    multiplier = 1  # default value for multiplier
                    if "x" in kinds[k].lower():
                        # Extract multiplier value
                        parts = re.split(r"x", kinds[k], flags=re.IGNORECASE) # Split case-insensitive
                        if len(parts) == 2 and parts[1].isdigit():
                             multiplier = int(parts[1])
                             sub_kind_without_multiplier = kinds[k]
                    sub_kind_count += multiplier
                    kinds_combined += f"({sub_kind_without_multiplier})-{qty}PCS" + (f"x{multiplier}" if multiplier > 1 else "") + "\n"
                else:
                 #Case 2-2 when kinds has only 1 element
                    if 'kinds' in locals() and isinstance(kinds, list) and len(kinds) > 0:
                      for k in range(len(kinds)):
                       # Check for "xN" multiplier in sub-kind
                        sub_kind_without_multiplier = kinds[k]
                        multiplier = 1  # default value for multiplier
                        if "x" in kinds[k].lower():
                          # Extract multiplier value
                            parts = re.split(r"x", kinds[k], flags=re.IGNORECASE) # Split case-insensitive
                            if len(parts) == 2 and parts[1].isdigit():
                              multiplier = int(parts[1])
                              sub_kind_without_multiplier = kinds[k]
                        sub_kind_count += multiplier
                        kinds_combined = f"({sub_kind_without_multiplier})"
                if len(kinds_combined) > 2 and 'kinds' in locals() and isinstance(kinds, list) and len(kinds) > 0 :
                    kinds_combined = kinds_combined[:-1]
                org_sheet.cell(row=j, column=2).value = kinds_combined
                if 'kinds' in locals() and isinstance(kinds, list) and len(kinds) > 0:
                  #case 2-1
                     org_sheet.cell(row=j, column=1).value = f"{desc} ({sub_kind_count}pcs/set)"
                     org_sheet.cell(row=j, column=4).value = "SET"
                else:
                   #case 2-2
                   org_sheet.cell(row=j, column=1).value = desc
                   org_sheet.cell(row=j, column=4).value = "PCS"
                org_sheet.cell(row=j, column=3).value = qty
                org_sheet.cell(row=j, column=5).value = min_unit_price
                org_sheet.cell(row=j, column=6).number_format = "@"
                org_sheet.cell(row=j, column=6).value = "04"
                org_sheet.cell(row=j, column=7).value = "F.O.C."
                org_sheet.cell(row=j, column=8).value = "NO BRAND"
                org_sheet.cell(row=j, column=9).number_format = "@"
                org_sheet.cell(row=j, column=9).value = "49119900002"
                # Clear kinds array
                if 'kinds' in locals():
                    del kinds
                min_unit_price = float('inf')
            else:
                # Case 1 - pcs
                # Add kind to kinds array
                 # Remove parentheses from the kind string
                if kind and kind.startswith("(") and kind.endswith(")"):
                    kind = kind[1:-1]
                # Split the kind by commas into the subkinds array
                sub_kinds = []
                if kind:
                   sub_kinds = kind.split(",")
                sub_kinds_combined = ""
                qty_string = f"{qty:,}PCS"
                sub_kind_count = 0
                kinds = [] # Initialize kinds list
                for sub_k in sub_kinds:
                    # Check for "xN" multiplier in sub-kind
                    sub_kind_without_multiplier = sub_k.strip()
                    multiplier = 1  # default value for multiplier
                    if "x" in sub_k.lower():
                         # Extract multiplier value
                         parts = re.split(r"x", sub_k, flags=re.IGNORECASE) # Split case-insensitive
                         if len(parts) == 2 and parts[1].isdigit():
                            multiplier = int(parts[1])
                            sub_kind_without_multiplier = sub_k.strip()
                    sub_kind_count += multiplier
                    if len(sub_kinds) > 1:
                        sub_kinds_combined += f"({sub_kind_without_multiplier})-{qty_string}" + (f"x{multiplier}" if multiplier > 1 else "") + "\n"
                    else:
                       sub_kinds_combined = f"({sub_kind_without_multiplier})"
                    kinds.append(sub_kind_without_multiplier)
                if len(sub_kinds_combined) > 2 and len(sub_kinds) > 1:
                     sub_kinds_combined = sub_kinds_combined[:-1]
                # Construct the cell A value with the (n pcs/set) part if needed
                if sub_kind_count > 1:
                    org_sheet.cell(row=j, column=1).value = f"{desc} ({sub_kind_count}pcs/set)"
                    org_sheet.cell(row=j, column=4).value = "SET"
                else:
                    org_sheet.cell(row=j, column=1).value = desc
                    org_sheet.cell(row=j, column=4).value = "PCS"
                org_sheet.cell(row=j, column=2).value = sub_kinds_combined
                org_sheet.cell(row=j, column=3).value = qty
                org_sheet.cell(row=j, column=5).value = unit_price
                # Update the min price
                if unit_price < min_unit_price:
                     min_unit_price = unit_price
                org_sheet.cell(row=j, column=6).number_format = "@"
                org_sheet.cell(row=j, column=6).value = "02"
                org_sheet.cell(row=j, column=8).value = "NO BRAND"
                org_sheet.cell(row=j, column=9).number_format = "@"
                org_sheet.cell(row=j, column=9).value = "49119900002"
            # Increment the row counter for orgSheet
            j += 1
        # Format the "Organized" sheet columns
        org_sheet.column_dimensions[get_column_letter(1)].width = 32.33
        org_sheet.column_dimensions[get_column_letter(2)].width = 30
        org_sheet.column_dimensions[get_column_letter(3)].number_format = "#,##0"
        # Autofit all rows and columns in organized sheet
        for row in org_sheet.rows:
           for cell in row:
                if cell.value:
                     org_sheet.row_dimensions[cell.row].auto_size = True
        for column_cells in org_sheet.columns:
            org_sheet.column_dimensions[column_cells[0].column_letter].auto_size = True
         # Save the organized data to a new file in the 'uploads' folder
        output_filename = os.path.join("uploads","Organized_Data.xlsx")
        organized_wb.save(output_filename)
        print(f"Organized data saved to '{output_filename}'")
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")