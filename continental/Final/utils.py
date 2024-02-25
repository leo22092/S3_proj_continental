import csv
import os
from pdfminer.high_level import extract_pages,extract_text,PDFPage
from pdfminer.layout import LTTextBoxHorizontal
from PyPDF2 import PdfReader, PdfWriter
from pdfminer.layout import LAParams, LTTextBox, LTText
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import PDFPageAggregator
import fitz
import re



def page_no_return(interpreter,dev,pages,pattern,pattern3,list_of_pages):
    for page in pages:
        print('--- Processing ---')
        interpreter.process_page(page)
        layout = dev.get_result()
        for lobj in layout:
            if isinstance(lobj, LTText):
                x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()

                match = re.search(pattern, text)
                match3=re.finditer(pattern3,text)

                if match:
                    print("hi")
                    starting_page_number = int(match.group(1))
                    print(f"Starting page of requirement is ,{starting_page_number}")

                for match in match3:
                    captured_text = match.group(3)
                    list_of_pages.append(int(captured_text))
                    last_page=max(list_of_pages)
    print(last_page)
    return  starting_page_number,last_page

def crop_pdf(input_pdf, start_page, end_page, output_pdf):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    for page_number, page in enumerate(extract_pages(input_pdf)):
        if start_page <= page_number + 1 <= end_page:
            pdf_writer.add_page(pdf_reader.pages[page_number])

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

def to_csv(data_dict):
    csv_file_path = 'output.csv'

    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_file_path)

    # Open the CSV file in append mode ('a') or write mode ('w') accordingly
    with open(csv_file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header only if the file is newly created
        if not file_exists:
            csv_writer.writerow(['ID', 'Type', 'Requirement'])

        # Write data rows
        for id_value, values in data_dict.items():
            # Make sure there are at least two values before unpacking
            if len(values) >= 2:
                csv_writer.writerow([id_value] + values[:2])
            else:
                continue
                # Handle cases where there are not enough values
                print(f"Skipping invalid entry for ID: {id_value}")


    print(f'Data has been written to {csv_file_path}')


def get_number_of_pages(pdf_path):
    pdf_document = fitz.open(pdf_path)
    number_of_pages = pdf_document.page_count
    pdf_document.close()
    return number_of_pages

def extract_requirements(output_pdf_path,page_no):
    id_list = ["0"]
    current_id = ["1"]
    data_dict={}
    text = extract_pages(output_pdf_path, page_numbers=[page_no], maxpages=5)

    for page_layout in text:
        for element in page_layout:

            previous_id = id_list[-1]
            if isinstance(element,LTTextBoxHorizontal):
                x, y, text = element.bbox[0], element.bbox[3], element.get_text()
                # print("________\n",text,len(text))
                pattern_id = r"\s*ID:\s*(.*)"
                pattern_type = r"\s*Type:\s*(.*)"
                pattern_rati = r"\s*Rationale:\s*(.*)"

                match_id = re.search(pattern_id, text)
                match_type = re.search(pattern_type, text)
                match_rat=re.search(pattern_rati,text)
                if match_id:
                    id_content = match_id.group(1)
                    previous_id = current_id
                    current_id=id_content
                    id_list.append(id_content)
                    print("ID Content:", id_content)
                    data_dict[current_id]=[]
                    if match_type:
                        type_content = match_type.group(1)
                        data_dict[current_id]=[type_content]
                        print("type Content:", type_content)
                        # print(data_dict)

                        # continue
                if previous_id==id_list[-1] and len(id_list)>=2 and len(text)>=35 :
                    if not match_rat:
                        requirement=text
                        # print(requirement)
                        data_dict[current_id].append(requirement)
    to_csv(data_dict)
    return data_dict
