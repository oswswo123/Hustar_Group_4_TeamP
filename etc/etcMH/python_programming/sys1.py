import sys

print(sys.argv)
with open(sys.argv[1], 'r') as fr:
    with open(sys.argv[2], 'w') as fw:
        for line in fr:
            fw.write(line)