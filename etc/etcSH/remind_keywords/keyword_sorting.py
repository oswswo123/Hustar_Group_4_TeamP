#!/usr/bin/env python
# coding: utf-8

# In[73]:


import sys

#######################################################
# 사용법
# 필수 file : all_remind_keyword.txt (비어있어도 됨)
# input file 이름 예시 : [0329]today_input.txt
#######################################################


# today_remind_keyword를 읽고, 단어 list를 return
def today_remind_input(file_name):
    today_keyword_list = list()
    
    # today remind keyword를 읽어들이기 위한 input_file_pointer
    input_file_pointer = open(file_name, "r")

    # temp_list : today keyword를 저장 할 list
    for line in input_file_pointer.readlines():
        today_keyword_list.append(line[:-1])

    # 입력 file pointer 닫기 (temp_list에 today keyword 저장 완료)
    input_file_pointer.close()
    
    return today_keyword_list


# today_remind_keyword를 output file로 출력
def today_remind_output(file_name, today_keyword_list, today_date, day_of_the_week):
    # today_remind_keyword 출력 file pointer 생성
    output_file_pointer = open(file_name, "w")

    # 날짜 및 요일 작성
    # 0401 -> 4.01
    month = int(today_date[:2])
    day = int(today_date[2:])
    
    output_file_pointer.write("\t- remind keyword ({}.{} {})\n".format(month, day, day_of_the_week))

    # keyword들에 번호 붙여서 출력
    counter = 1
    for keyword in today_keyword_list:
        output_file_pointer.write("{:02d}. ".format(counter) + keyword + "\n")
        counter += 1

    output_file_pointer.close()
    
    return


# all_remind_keyword를 읽고, keyword set을 만든 후 list sorting하여 return
def all_remind_input(file_name, today_keyword_list):
    # all_remind_keyword 읽어들이기 위한 input_file_pointer
    input_file_pointer = open(file_name, "r")

    # 단어간 중복을 제거하기 위한 all_keyword_set 생성
    all_keyword_set = set()
    for line in input_file_pointer.readlines():
        ### 현재 01 ~ 99 까지라 line[4:-1]로 실행
        ### 01 ~ 999 까지가 된다면 line[5:-1]로 변경 필요
        all_keyword_set.add(line[5:-1])

    input_file_pointer.close()
    
    # all_keyword_set에 today_keyword_list 넣기
    for word in today_keyword_list:
        all_keyword_set.add(word)

    # all_keyword_set을 sorting 하기위한 list 생성
    sorting_list = list(all_keyword_set)
    sorting_list.sort()
    
    return sorting_list


# all_remind_keyword를 output file로 출력
def all_remind_output(file_name, sorting_list):
    output_file_pointer = open(file_name, "w")

    counter = 1
    for keyword in sorting_list:
        output_file_pointer.write("{:03d}. ".format(counter) + keyword + "\n")
        counter += 1

    output_file_pointer.close()
    
    return

##########################################################################

args = sys.argv[1:]

''' 수동 테스트시 사용
# 날짜 입력 받기
today_date = input("날짜를 입력해 주세요. (ex. 0401) : ")
day_of_the_week = input("요일을 입력 해 주세요. (ex. 금) :")
'''
today_date = args[0]
day_of_the_week = args[1]

# file name 수동 조작용
# file_name = input("today remind keyword input file 이름을 입력하세요 : ")
file_name = "[{}]today_input.txt".format(today_date)
today_keyword_list = today_remind_input(file_name)

# file name 수동 조작용
# file_name = input("today remind keyword output file 이름을 입력하세요 : ")
file_name = "[{}]today_output.txt".format(today_date)
today_remind_output(file_name, today_keyword_list, today_date, day_of_the_week)

# file name 수동 조작용
# file_name = input("all remind keyword input file 이름을 입력하세요 : ")
file_name = "all_remind_keyword.txt"
sorting_list = all_remind_input(file_name, today_keyword_list)

# file name 수동 조작용
# file_name = input("all remind keyword output file 이름을 입력하세요 : ")
all_remind_output(file_name, sorting_list)


# In[ ]:




