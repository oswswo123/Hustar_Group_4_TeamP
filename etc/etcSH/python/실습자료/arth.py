def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def main():
    numbers = input("Enter two integers: ")

    a, b = numbers.split()
    a = int(a)
    b = int(b)

    print("%d + %d = %2d" % (a, b, add(a, b)))
    print("%d - %d = %2d" % (a, b, sub(a, b)))
    return

if __name__ == "__main__":
    main()