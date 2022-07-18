# Source 유의사항
-------------------
### pdf_to_text.py
- input : pdf file name
- return : string list
- PDF 파일 이름을 입력받아 Text를 추출해 String List로 Return해주는 Module
-------------------
### postgreSQL.py
- PostgreSQL DB와 연동하기 위한 class 구현  (class 생성 시 DB 접속 및 cursor 설정까지 완료됨)
- 최초 객체 생성 시 **host, dbname, user, password, port** 입력  (default로 현 DB 설정해놓음)
- 객체 선언 후 쿼리문 실행은 **execute()** method로 실행 - (쿼리문 예시는 testMH 폴더의 how_to_use.py 참고)
<br>
'''bash
pip install psycopg2
'''
- psycopg2 패키지 설치해야함
-------------------
