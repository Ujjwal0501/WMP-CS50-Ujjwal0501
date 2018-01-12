import cs50

print("o hai!", end="")

n = -1
while n < 0 :
    print("how much is owed?")
    n = cs50.get_float()

n = n * 100
count = 0

while n >= 25 :
    n -= 25
    count += 1

while n >= 10 :
    n -= 10
    count += 1

while n >= 5 :
    n -= 5
    count += 1

while n >= 1 :
    n -= 1
    count += 1

print(count)