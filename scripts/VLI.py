import openpyxl
from openpyxl.utils import get_column_letter
import pandas as pd
import textract
import re
import os

def read_doc_file(doc_path):
    """
    Reads the content of a .doc file.
    Args:
        doc_path (str): The path to the .doc file.
    Returns:
        str: The extracted text content.
    """
    try:
        text = textract.process(doc_path)
        return text.decode('utf-8')
    except Exception as e:
        print(f"Error reading .doc file: {e}")
        return ""

def extract_table_content(content):
    """
    Extracts the table content from the text.
    Args:
        content (str): The text content.
    Returns:
        str: The extracted table content.
    """
    try:
        start_marker = "VLI CHIPSET(IC)"
        end_marker = "Total"
        
        start_pos = content.find(start_marker)
        end_pos = content.find(end_marker, start_pos)
        
        if start_pos == -1 or end_pos == -1:
            print("Markers not found in the content.")
            return ""
        
        table_content = content[start_pos + len(start_marker):end_pos].strip()
        
        lines = table_content.split('\n')
        filtered_lines = [line for line in lines if '-' * 10 not in line]
        
        return '\n'.join(filtered_lines)
    except Exception as e:
        print(f"Error extracting table content: {e}")
        return ""

def split_elements(line):
    """
    Splits a line into elements based on long spaces.
    Args:
        line (str): The line to split.
    Returns:
        list: The split elements.
    """
    try:
        elements = re.split(r'\s{2,}', line.strip())
        combined_elements = []
        i = 0
        while i < len(elements):
            if i < len(elements) - 1 and re.match(r'\d+(\.\d+)?x\d+(\.\d+)?m', elements[i + 1]):
                combined_elements.append(elements[i] + ' ' + elements[i + 1])
                i += 2
            else:
                combined_elements.append(elements[i])
                i += 1
        return combined_elements
    except Exception as e:
        print(f"Error splitting elements: {e}")
        return []

def save_to_excel(data, filename):
    """
    Saves the extracted data to an Excel file.
    Args:
        data (str): The extracted data.
        filename (str): The path to the Excel file.
    """
    try:
        rows = data.split('\n\n')
        all_elements = []
        for row in rows:
            elements = []
            for line in row.split('\n'):
                elements.extend(split_elements(line))
            all_elements.append(elements)
        
        formatted_rows = [row[:10] for row in all_elements if len(row) >= 10]
        
        df = pd.DataFrame(formatted_rows)
        df.to_excel(filename, index=False, header=False)
    except Exception as e:
        print(f"Error saving to Excel: {e}")

def organize_data(filename):
    """
    Organizes data from the extracted table in an Excel file
    and writes the organized data to a new Excel file.
    Args:
        filename (str): The path to the Excel file containing the extracted table.
    """
    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active

        organized_wb = openpyxl.Workbook()
        organized_sheet = organized_wb.active
        organized_sheet.title = "Organized"

        i = 0
        j = 0

        while i <= sheet.max_row:
            i += 1
            j += 1
            part_no = sheet.cell(row=i, column=1).value
            if part_no == 'Bill to:':
                continue
            elif part_no is None:
                break

            desc_1 = sheet.cell(row=i, column=2).value
            qty = int(sheet.cell(row=i, column=3).value)
            unit_price = float(sheet.cell(row=i, column=4).value)
            amount = sheet.cell(row=i, column=5).value
            po_no = sheet.cell(row=i, column=6).value
            desc_2 = sheet.cell(row=i, column=7).value
            qty_unit = sheet.cell(row=i, column=8).value
            unit_price_unit = sheet.cell(row=i, column=9).value
            amount_unit = sheet.cell(row=i, column=10).value

            organized_sheet.cell(row=j, column=1, value=f'Part No.{part_no}')
            organized_sheet.cell(row=j, column=2, value=f'Po. No.{po_no}')
            organized_sheet.cell(row=j, column=3, value=desc_1)
            organized_sheet.cell(row=j, column=4, value=desc_2)
            organized_sheet.cell(row=j, column=5, value=qty)
            organized_sheet.cell(row=j, column=6, value=qty_unit)
            organized_sheet.cell(row=j, column=7, value=unit_price)
            organized_sheet.cell(row=j, column=8, value='VLI')
            organized_sheet.cell(row=j, column=9, value='85423900228')
            organized_sheet.cell(row=j, column=10, value='02')

            qty_cell = organized_sheet.cell(row=j, column=5, value=qty)
            if isinstance(qty, (int, float)):
                qty_cell.number_format = '#,##0'
            
            unit_price_cell = organized_sheet.cell(row=j, column=7, value=unit_price)
            if isinstance(unit_price, (int, float)):
                unit_price_cell.number_format = '#,##0.0000'

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

        output_filename = os.path.join("uploads", "Organized_Data.xlsx")
        organized_wb.save(output_filename)
        print(f"Organized data saved to '{output_filename}'")
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")