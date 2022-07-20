import sys, os
import googletrans
import urllib
import json
import argparse

sys.path.append(os.path.dirname(__file__))
import text_processor


def back_translate_google(source_text, target_lang):
    translator = googletrans.Translator()
    
    trans_text = translator.translate(source_text, dest=target_lang)
    back_trans_text = translator.translate(trans_text.text, dest="ko")
    
    return back_trans_text.text

def back_translate_papago(source_text, target_lang):
    # 보안상 개인 naver api key 사용 바람
    json_file = open("./translator_key.json", encoding="utf-8")
    key_dict = json.loads(json_file.read())

    client_id = key_dict["client_id"]
    client_secret = key_dict["client_secret"]

    url = "https://openapi.naver.com/v1/papago/n2mt"
    
    ### 한국어 -> 외국어
    enc_text = urllib.parse.quote(source_text)
    data = f"source=ko&target={target_lang}&text=" + enc_text
    
    # 요청 header 및 parameter
    req_header = {"X-Naver-Client-Id":client_id, "X-Naver-Client-Secret":client_secret}
    req_parameter = {"source":"ko", "target":target_lang, "text":enc_text}
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode == 200):
        response_body = response.read()
        res_json = json.loads(response_body.decode("utf-8"))
        trans_text = res_json["message"]["result"]["translatedText"]
    else:
        print("error Code:" + rescode)
        sys.exit(1)
    
    ### 외국어 -> 한국어
    enc_text = urllib.parse.quote(trans_text)
    data = f"source={target_lang}&target=ko&text=" + enc_text
    
    # 요청 header 및 parameter
    req_parameter = {"source":target_lang, "target":"ko", "text":trans_text}
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode == 200):
        response_body = response.read()
        res_json = json.loads(response_body.decode("utf-8"))
        back_trans_text = res_json["message"]["result"]["translatedText"]
    else:
        print("error Code:" + rescode)
        sys.exit(1)
    
    return back_trans_text

def main():
    parser = argparse.ArgumentParser("Back Translate Method.")
    
    parser.add_argument("--file_path", required=True, help="pdf file path")
    parser.add_argument("--translator", required=True, help="Want use translator. you can use \"Google translator\" and \"Naver Papago\". Enter \"google\" if you want to use Google Translator, or \"papago\" if you want to use Naver Papago.")
    parser.add_argument("--tgt_lang", required=True, help="Target Language")
    
    args = parser.parse_args()
    
    pdf_file_path = args.file_path
    use_translator = args.translator
    target_lang = args.tgt_lang   
    
    text_data = text_processor.read_pdf_PDFMINER(pdf_file_path)
    preprocessed_text_data = text_processor.preprocessing(text_data)
    
    if use_translator == "google":
        back_trans_text = back_translate_google(preprocessed_text_data, target_lang)
    elif use_translator == "papago":
        back_trans_text = back_translate_papago(preprocessed_text_data, target_lang)
    else:
        print("Invalid Input. Exit process.")
        sys.exit(-1)
    
    print(back_trans_text)

    
if __name__ == "__main__":
    main()