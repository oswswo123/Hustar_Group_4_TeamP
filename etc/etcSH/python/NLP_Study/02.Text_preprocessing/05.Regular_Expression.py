# %% 정규 표현식 (Regular Expression)

import re

# . : 한 개의 임의의 문자
r = re.compile("a.c")
print(r.search("kkk"))
print(r.search("abc"))
print(r.search("akc"))

# %% 
# ? : ? 앞의 문자가 존재할 수도 있고 존재하지 않을 수도 있음
r = re.compile("ab?c")
print(r.search("abbc"))
print(r.search("abc"))
print(r.search("ac"))
# %%
# * : * 바로 앞의 문자가 0개 이상일 경우를 나타냄. 앞의 문자는 존재하지 않을 수도 있으며, 여러 개 일 수도 있음
r = re.compile("ab*c")
print(r.search("a"))
print(r.search("ac"))
print(r.search("abc"))
print(r.search("abbbbbbbbc"))
# %%
# + : + 바로 앞의 문자가 1개 이상일 경우를 나타냄. 앞에 문자가 하나 이상 반드시 존재
r = re.compile("ab+c")
print(r.search("ac"))
print(r.search("abc"))
print(r.search("abbbbbbbc"))
# %%
# ^ : 시작되는 문자열을 지정
r = re.compile("^ab")
print(r.search("bbc"))
print(r.search("zab"))
print(r.search("abz"))
# %%
# {숫자} : 문자에 해당 기호를 붙이면, 해당 문자를 숫자만큼 반복한 것을 의미
r = re.compile("ab{2}c")
print(r.search("ac"))
print(r.search("abc"))
print(r.search("abbbbbbc"))
print(r.search("abbc"))
# %%
# {숫자1, 숫자2} : 문자에 해당 기호를 붙이면, 숫자1 이상 숫자2 이하 반복
r = re.compile("ab{2,8}c")
print(r.search("ac"))
print(r.search("abc"))
print(r.search("abbbbbbbbbbbbbbbbbbbbbbbbbbbc"))
print(r.search("abbc"))
# %%
# {숫자,} : 해당 문자를 숫자 이상 만큼 반복
r = re.compile("a{2,}bc")
print(r.search("bc"))
print(r.search("aa"))
print(r.search("aabc"))
print(r.search("aaaaaaaaaabc"))
# %%
# [ ] : [ ] 안에 문자들을 넣으면 그 문자들 중 한 개의 문자와 매치
r = re.compile("[abc]") # [abc]는 [a-c]와 같음
print(r.search("zzz"))
print(r.search("a"))
print(r.search("aaaaaaaaa"))
print(r.search("baaac"))
# %%
# [^문자] : [^문자]는 ^기호 뒤에 붙은 문자들을 제외한 모든 문자들을 매치
r = re.compile("[^abc]")
print(r.search("a"))
print(r.search("ab"))
print(r.search("b"))
print(r.search("d"))
print(r.search("1"))