def print_pattern(x):
    for i in range(1, x + 1): 
        print("*" * i)
    for i in range(x - 1, 0, -1):  
        print("*" * i)

x = int(input("Enter a number: "))
print_pattern(x)

