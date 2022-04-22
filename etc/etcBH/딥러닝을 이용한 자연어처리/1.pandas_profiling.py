# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 22:45:37 2022

@author: 이병화
"""

import pandas as pd
import pandas_profiling


data = pd.read_csv('spam.csv',encoding='latin1')
# 윈도우 바탕화면에서 작업한 저자의 경우에는
# data = pd.read_csv(r'C:\Users\USER\Desktop\spam.csv',encoding='latin1')

print(data[:5])

pr = data.profile_report() # 프로파일링 결과 리포트를 pr에 저장
data.profile_report() # 바로 결과 보기

pr.to_file('./pr_report.html') # pr_report.html 파일로 저장

pr