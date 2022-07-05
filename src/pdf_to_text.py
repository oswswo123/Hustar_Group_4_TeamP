import PyPDF2

def convert_to_text(file_name):
    # PDF 파일 object 생성
    pdf_file_obj = open(file_name, "rb")

    # PDF Reader Object 생성
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    
    page0_obj = pdf_reader.getPage(0)
    page0_obj.extractText()
    string_list = page0_obj.extractText().split()
    
    return string_list

def main():
    file_name = "./data/test_pdf_file1.pdf"
    print(convert_to_text(file_name))

if __name__ == "__main__":
    main()