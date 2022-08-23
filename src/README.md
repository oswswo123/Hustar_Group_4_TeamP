# Source 유의사항
-------------------
### text_processor.py
- PDF to Text를 비롯한 Text관련 처리를 담당하는 module
- 요구 패키지 : pdfminer
- read_pdf_PDFMINER(pdf_file_path)
	- pdf_file_path를 입력받아 해당 경로의 pdf파일을 str으로 return
- preprocessing(data)
	- string data를 입력받아 전처리를 시행. 특수문자, 영어, 숫자 제거 및 띄워쓰기 맞춤 시행
-------------------
### postgreSQL.py
- PostgreSQL DB와 연동하기 위한 class 구현
- 최초 객체 생성 시 **host, dbname, user, password, port** 입력 (default로 현 DB 설정해놓음)
- 객체 선언 후 쿼리문 실행은 **execute()** method로 실행
  - (쿼리문 예시는 testMH 폴더의 how_to_use.py 참고)  
<pre><code> pip install psycopg2 </code></pre>
- psycopg2 패키지 설치해야함
-------------------
### back_translator.py
- Document Data augmentation을 위한 back translator module
- 요구 패키지 : googletrans, urllib, json
- 주의사항 : googletrans는 "pip install googletrans==4.0.0-rc1"으로 설치할 것
- back_translate_google(source_text, target_lang)
	- google 번역기를 활용하여 back translation을 실행하는 method
	- target_lang의 언어로 번역되었다가, 다시 한글로 번역된 결과 return
- back_translate_papago(source_text, target_lang)
	- Naver Papago를 활용하여 back translation을 실행하는 method
	- target_lang의 언어로 번역되었다가, 다시 한글로 번역된 결과 return
-------------------
### data_control.py
- Data를 load하고, split하고, loader로 바꾸는 등 학습을 위한 데이터를 관리하는 module
- 요구 패키지 : torch, sklearn
-------------------
### etc_modules.py
- metric이나 결과물의 save와 관련된 처리들을 하는 module
- 요구 패키지 : torch
-------------------
### k_fold_train.py
- model을 train시키기 위한 package
- 필요한 parameter는 train_config.json에 작성하여 실행
-------------------
### inference.py
- train된 model을 활용해 inference하기 위한 package
- 필요한 parameter는 inference_config.json에 작성하여 실행
-------------------
