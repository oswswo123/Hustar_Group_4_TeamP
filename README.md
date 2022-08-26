# Hustar 4조 팀프로젝트 진행 참고사항
### 8.24(수)
- Ainalyst Django file Final Upload
- Update postgreSQL.py (main문 삭제)
- Update insertDB.py (DB에 데이터 입력 시 사용)

### 8.23(화)
- train, inference 모듈화 완료

### 8.19(금)
- soft voting 구현 완료
	- 훨씬더 완화된 확률값을 얻을 수 있음
- source code들 모듈화 하여 패키지로 묶어낼 예정

### 8.17(수)
- back translation을 활용한 데이터 증축
	- pororo-en
	- googletrans-en
	- googletrans-zhcn
	- papago(예정)
- 해당 데이터들을 활용해 soft voting 기능을 구현하기 위한 준비 완료

### 8.10(수)
- cross-validation을 활용한 성능 검증 완료.
- Accuracy는 test data에 대하여 약 93~94 %
- 다만 inference 할 경우 확률이 너무 극단적으로 나오는 경향이 있음
- 이를 해결하기 위해 ensemble 기법 중 soft voting을 활용할 예정

### 8.03(수)
- pretrained model albert를 활용하여 AInalyst 학습성공
- 데이터의 극히 일부만 사용했기에 성능이 확실한지 확인 필요

### 7.20(수)
- src directory에 back_translator, text_processor 추가
- back_translator : 역번역을 통해 data augmentation을 해주는 module
- text_processor : PDF to TEXT를 비롯한 여러 텍스트 처리를 해주는 module

### 7.05(화)
- 본격적인 프로젝트 시작
- 프로젝트를 위한 Git Directory 정리
- 사용법
	- push할 때 반드시 commit log 및 README 성실하게 작성할 것. 본인은 알아봐도 다른 사람들은 모름.
	- 모든 python 함수는 모듈화 하여 작성할것. 모듈화 된 함수 및 클래스들을 src directory로 이동.
		- 모듈화 된 함수는 input과 output, 기능만을 알아도 사용할 수 있어야함. 다른 사람이 동작원리를 알지 못해도 되도록 만들것.
	- test directory 내부에서 자유롭게 실험하되, Data나 Image들은 Git에 upload 하지 말 것.
		- .gitignore 사용법을 익힐 것
	- 상기한 내용들은 Clone한 Git repository 내부에서 모든 작업을 하라는 의미. 자주 commit할 것.

### 3.29(화)
- 개별 test directory 생성
- src, ExtraLib, etc directory 생성

### 3.30(수)
- 개별 etc directory 생성
- 3.29(화), 3.30(수), 주간 remind keyword 추가

### 3.31(목)
- week remind keyword 가나다 순으로 정리
- 3.31(목) 일자 remind keyword를 week에 추가
- txt file vi로 읽어보기
