def add(a,b):
    return a+b

def sub(a,b):
    return a-b

if __name__ == '__main__':
    numbers = input("Enter two integers: ")

    a,b = numbers.split()
    a,b = int(a), int(b)

    print(f"{a} + {b} = {add(a,b)}")
    print(f"{a} + {b} = {sub(a,b)}")