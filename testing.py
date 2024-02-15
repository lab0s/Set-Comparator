a = input('Please input first value: ')

try:
    a = int(a)
except ValueError:
    print('First value must be positive integer.')
    exit()


b = input('Please input second value: ')

try:
    b = int(b)
except ValueError:
    print('Second value must be positive integer.')
    exit()



print(a)
print(b)