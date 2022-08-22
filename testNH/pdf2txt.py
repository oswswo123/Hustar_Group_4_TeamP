from pdfminer.high_level import extract_text

def text(pdffile):
    txtfile = pdffile.replace("pdf","txt")
    text = extract_text(pdffile)
    with open(txtfile, 'w') as f:
        f.writelines(text)

for idx in range(1, 476):
    try :
        file_name = f"strongbuy{idx}.pdf"
        print(file_name)
        text(file_name)

    except:
        print(f"no file {idx}")
        pass