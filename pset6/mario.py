import cs50

n = -1
while n < 0 or n > 23:
    print("Height: ", end="")
    n = cs50.get_int()

for i in range(n) :
    for j in range(n - i - 1) :
        print(" ", end="")
    for j in range(i + 2) :
        print("#", end="")
    print("")