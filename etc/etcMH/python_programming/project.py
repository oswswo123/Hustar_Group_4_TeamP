# File Name: project.py
# File Contents: 성적 관리 프로그램 구현
# Programmed by Minho Kim 22.04.04.

import sys
import os

def initStudents(student, sID, name, score):
    avg, grade = calculate(score)
    student[sID] = [name, score[0], score[1], avg, grade]

    
def calculate(score):
    avg = sum(score)/len(score)
    if avg >= 90:
        grade = 'A'
    elif avg >= 80:
        grade = 'B'
    elif avg >= 70:
        grade = 'C'
    elif avg >= 60:
        grade = 'D'
    else:
        grade = 'F'

    return avg, grade


def show(student):
    if student:
        student = dict(sorted(student.items(), key= lambda s: s[1][3], reverse=True))
        print("Student_ID           Name     Midterm    Final    Average    Grade")
        print("--------------------------------------------------------------------")
        for key, s in student.items():
            print(f"{key:8}  {s[0]:>15}  {s[1]:>8}  {s[2]:>8}  {s[3]:>8}   {s[4]:>6}")


def search(student, sID):
    if sID in student.keys():
        return {sID: student[sID]}


def searchgrade(student, grade):
    right_grade = ['A','B','C','D','F']
    if grade not in right_grade:
        return 0
    
    std_dic = dict()
    for key, s in student.items():
        if grade in s:
            std_dic[key] = s
    
    if std_dic:
        return std_dic
    else:
        print("NO RESULTS.")
        return 0

    
def changescore(student, sID):
    if not search(student, sID):
        print("NO SUCH PERSON.")
        return

    exam = input("Mid/Final? ").lower()
    if exam != 'mid' and exam != 'final':
        return
    
    score = int(input("Input new score: "))
    if score < 0 or score > 100:
        return
    
    def change(student, sID, score):
        initStudents(student, sID, student[sID][0], score)
        print("Score changed.")
        print(f"{sID:8}  {student[sID][0]:>15}  {student[sID][1]:>8}  {student[sID][2]:>8}  {student[sID][3]:>8}   {student[sID][4]:>6}")
    
    show({sID:student[sID]})
    if exam == 'mid':
        score = [score, student[sID][2]]
        change(student, sID, score)
        
    if exam == 'final':
        score = [student[sID][1], score]
        change(student, sID, score)


def add(student, sID):
    if search(student, sID):
        print("ALREADY EXISTS.")
        return
    
    name = input("Name: ")
    mid, final = int(input("Midterm Score: ")), int(input("Final Score: "))
    if (mid < 0 or mid > 100) or (final < 0 or final > 100):
        print("!!Wrong range Score!!")
        return
        
    initStudents(student, sID, name, [mid, final])
    print("Student added.")


def remove(student):
    if not student:
        print("List is empty")
        return
    
    sID = input("Student ID: ")
    if not search(student, sID):
        print("NO SUCH PERSON.")
        return
    
    student.pop(sID)
    print("Student removed")


def quit(student):
    save = input("Save data? [yes/no] ").lower()
    if save == 'no':
        return
    
    fname = input("File name: ")
    student = dict(sorted(student.items(), key= lambda s: s[1][3], reverse=True))
    with open(fname, 'w') as fw:
        for key, s in student.items():
            data = '\t'.join([key] + list(map(str, s))) + '\n'
            fw.write(data)


def main():
    try:
        fname = sys.argv[1]
    except:
        fname = 'students.txt'
    
    # fname = 'students.txt'

    if not os.path.exists(fname):
        print("ERROR!!:: File does not exist.")
        return
    
        
    with open(fname, 'r') as fr:
        Students = dict()
        
        for line in fr:
            s_id, name1, name2, mid, final = line.split()
            name = ' '.join([name1, name2])
            score = [int(mid), int(final)]
            initStudents(Students, s_id, name, score)

        show(Students)
        while True:
            command = input("# ")

            if command.lower() == 'show':
                show(Students)
            elif command.lower() == 'search':
                sID = input("Student ID: ")
                dst = search(Students, sID)
                if dst:
                    show(dst)
                else:
                    print("NO SUCH PERSON.")
            elif command.lower() == 'searchgrade':
                grade = input("Grade to Search: ").upper()
                dst = searchgrade(Students, grade)
                show(dst)
            elif command.lower() == 'changescore':
                sID = input("Student ID: ")
                changescore(Students, sID)
            elif command.lower() == 'add':
                sID = input("Student ID: ")
                add(Students, sID)
            elif command.lower() == 'remove':
                remove(Students)
            elif command.lower() == 'quit':
                quit(Students)
                break
            else:
                continue


if __name__ == '__main__':
    main()