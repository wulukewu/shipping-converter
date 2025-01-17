import openpyxl

def read_xlsx_and_output_txt(xlsx_path, txt_path):
    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook(xlsx_path)
    sheet = workbook.active

    # Open the text file for writing
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        content = f'Invoice No.{"*"*20}'
        txt_file.write(content + '\n')

        i = 1
        date = None
        num = None

        while i <= sheet.max_row:
            i += 1

            date_tmp = sheet.cell(row=i, column=1).value
            num_tmp = sheet.cell(row=i, column=2).value
            item = sheet.cell(row=i, column=3).value
            storage = sheet.cell(row=i, column=4).value
            unit_price = sheet.cell(row=i, column=5).value
            assembly_fee = sheet.cell(row=i, column=6).value

            if date_tmp is None:
                if item is None:
                    break
            else:
                if not (date is None and num is None):
                    content = f'進口日期:{date} 報單號碼:{num}'
                    txt_file.write(content + '\n')

                if num_tmp is None:
                    content = date_tmp
                    txt_file.write(content + '\n')
                    break

                date = date_tmp 
                num = num_tmp               

            if isinstance(unit_price, (int, float)):
                unit_price = f"{unit_price:.2f}"
            if isinstance(assembly_fee, (int, float)):
                assembly_fee = f"{assembly_fee:.2f}"

            content = f'項次:{item} 容量:{storage}\n進料單價(USD):{unit_price} 詠聯組裝費(USD):{assembly_fee}'
            txt_file.write(content + '\n')