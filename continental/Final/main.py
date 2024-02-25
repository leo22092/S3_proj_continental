
from utils import *
# from page_no import *


pattern = r"4\s*Requirements\s*\.+\s*([0-9]+)"
pattern3= r"(\d+\.\d+)\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)*)\s+\.+\s+(\d+)"
list_of_pages=[]

fp = open('CMIV-Mod3-20200630102222-final_v1.0.pdf', 'rb')
manager = PDFResourceManager()
laparams = LAParams()
dev = PDFPageAggregator(manager, laparams=laparams)
interpreter = PDFPageInterpreter(manager, dev)
pages = PDFPage.get_pages(fp,pagenos=[4,5])

# returning page numbers of requirement
start_page,end_page=page_no_return(interpreter,dev,pages,pattern,pattern3,list_of_pages)

# Cropping requirement to output.pdf
crop_pdf('CMIV-Mod3-20200630102222-final_v1.0.pdf', start_page, end_page, 'output.pdf')
# Getting no of pages
no_of_pages=get_number_of_pages('output.pdf')
# For each page extract requirement and store in csv
for i in range(no_of_pages):
    print("Page_no : ",i)
    extract_requirements('output.pdf',int(i))

